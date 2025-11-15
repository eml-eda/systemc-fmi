from fmi3.base_fmi3_module import BaseFMI3Module
import re
import xml.etree.ElementTree as ET


class BaseFMI3Getter(BaseFMI3Module):
    def __init__(self, var_type: str, struct_file_path=None, xml_file_path=None):
        template = r"""
%(enum_definitions)s

    fmi3Status fmi3Get%(type)s(  fmi3Instance instance,
                                const fmi3ValueReference valueReferences[],
                                size_t nValueReferences,
                                fmi3%(type)s values[],
                                size_t nValues) {
    
    %(custom_code)s
    return fmi3OK;
}
"""
        template = template % {
            "type": var_type,
            "enum_definitions": "%(enum_definitions)s",
            "custom_code": "%(custom_code)s",
        }

        self.var_type = var_type

        super().__init__(
            template=template,
            includes=["struct.h"] if struct_file_path else None,
            struct_file_path=struct_file_path,
            xml_file_path=xml_file_path,
        )

    def parse_struct(self, struct_content):
        """Find variables of specified type in struct content"""
        var_pattern = rf"fmi3{self.var_type}\s+(\w+);"
        return [match.group(1) for match in re.finditer(var_pattern, struct_content)]

    def get_struct_name(self, struct_content):
        struct_pattern = r"struct\s+(\w+)"
        match = re.search(struct_pattern, struct_content)
        return match.group(1)

    def parse_xml(self, xml_path):
        """Parse modelDescription.xml to extract variables of specified type"""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            vars_dict = {}
            for var in root.findall(f".//{self.var_type}"):
                name = var.get("name")
                value_ref = var.get("valueReference")
                if name and value_ref:
                    vars_dict[name] = int(value_ref)
            return vars_dict
        except Exception as e:
            raise Exception(f"Error parsing XML file: {e}")

    def generate_enum_definitions(self, xml_vr):
        """Generate enum definitions for value references"""
        enum_lines = []
        enum_lines.append("// Auto-generated value references enum")
        enum_lines.append("enum ValueReferences_enum {")
        for var_name, value_ref in xml_vr.items():
            enum_lines.append(f"    VR_{var_name.upper()} = {value_ref},")
        enum_lines.append("};")
        return "\n".join(enum_lines)

    def generate_custom_code(self, variables, xml_vr, struct_name):
        """Generate the custom code for getter"""
        custom_code = f"{struct_name} *fmu = ({struct_name} *)instance;\n\n"
        custom_code += "for (size_t i = 0; i < nValueReferences; i++) {\n"
        custom_code += "    switch (valueReferences[i]) {\n"

        for var in variables:
            if var not in xml_vr:
                raise Exception(f"Variable {var} not found in XML file")
            custom_code += f"        case VR_{var.upper()}:\n"
            custom_code += f"            values[i] = fmu->{var};\n"
            custom_code += "            break;\n"

        custom_code += "        default:\n"
        custom_code += "            return fmi3Error;\n"
        custom_code += "    }\n"
        custom_code += "}\n"

        return custom_code

    def generate(self, config: dict):
        if not self.struct_file_path:
            self.template = self.template.format(custom_code="", enum_definitions="")
            return self.format_code(style="LLVM")
        try:
            with open(self.struct_file_path, "r") as f:
                struct_content = f.read()
        except Exception as e:
            raise Exception(f"Error reading struct file: {e}")

        variables = self.parse_struct(struct_content)
        struct_name = self.get_struct_name(struct_content)
        xml_vr = self.parse_xml(self.xml_file_path)

        if len(variables) > 0:
            enum_definitions = self.generate_enum_definitions(xml_vr)
            custom_code = self.generate_custom_code(
                variables=variables, xml_vr=xml_vr, struct_name=struct_name
            )
        else:
            enum_definitions = ""
            custom_code = ""

        self.template = self.template % {
            "custom_code": custom_code,
            "enum_definitions": enum_definitions,
        }
