from fmi3.base_fmi3_module import BaseFMI3Module
import re
import xml.etree.ElementTree as ET


class fmi3SetString(BaseFMI3Module):
    def __init__(self, struct_file_path=None, xml_file_path=None):
        template = """
{enum_definitions}

    fmi3Status fmi3SetString(   fmi3Instance instance,
                                const fmi3ValueReference valueReferences[],
                                size_t nValueReferences,
                                const fmi3String values[],
                                size_t nValues)    {{
    
    {custom_code}
    return fmi3OK;
}}
"""
        self.xml_file_path = xml_file_path
        self.struct_file_path = struct_file_path
        if not self.struct_file_path:
            super().__init__(template)
        else:
            super().__init__(template, includes=["struct.h"])

    def generate(self, config: dict):
        if not self.struct_file_path:
            # Return standard template with empty custom code
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
            # Generate enum definitions
            enum_definitions = self.generate_enum_definitions(xml_vr)

            custom_code = self.generate_custom_code(
                variables=variables, xml_vr=xml_vr, struct_name=struct_name
            )
        else:
            enum_definitions = ""
            custom_code = ""
            
        self.template = self.template.format(
            custom_code=custom_code, enum_definitions=enum_definitions
        )
        return self.format_code(style="LLVM")

    def generate_enum_definitions(self, xml_vr):
        """Generate enum definitions for value references"""
        enum_lines = []
        enum_lines.append("// Auto-generated value references enum")
        enum_lines.append("enum ValueReferences_enum {")
        for var_name, value_ref in xml_vr.items():
            enum_lines.append(f"    VR_{var_name.upper()} = {value_ref},")
        enum_lines.append("};")
        return "\n".join(enum_lines)

    def parse_struct(self, struct_content):
        # Find String variables and their signals
        string_vars = []
        var_pattern = r"fmi3String\s+(\w+);"

        variables = [
            match.group(1) for match in re.finditer(var_pattern, struct_content)
        ]

        return variables

    def get_struct_name(self, struct_content):
        struct_pattern = r"struct\s+(\w+)"
        match = re.search(struct_pattern, struct_content)
        return match.group(1)

    def generate_custom_code(self, variables, xml_vr, struct_name):
        custom_code = ""
        custom_code += f"{struct_name} *fmu = ({struct_name} *)instance;\n"

        # Generate the for loop to set the values using enum values
        custom_code += "for (size_t i = 0; i < nValueReferences; i++) {\n"
        custom_code += "    switch (valueReferences[i]) {\n"
        for var in variables:
            if var not in xml_vr:
                raise Exception(f"Variable {var} not found in XML file")
            custom_code += f"        case VR_{var.upper()}:\n"
            custom_code += f"            fmu->{var} = values[i];\n"
            custom_code += f"            fmu->s_{var}.write(values[i]);\n"
            custom_code += "            break;\n"
        custom_code += "        default:\n"
        custom_code += "            return fmi3Error;\n"
        custom_code += "    }\n"
        custom_code += "}\n"

        return custom_code

    def parse_xml(self, xml_path):
        """
        Parse modelDescription.xml to extract String variables and their value references.
        Returns a dictionary of {variable_name: value_reference}
        """
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Dictionary to store variable name and value reference
            string_vars = {}

            # Find all String elements
            for var in root.findall(".//String"):
                name = var.get("name")
                value_ref = var.get("valueReference")
                if name and value_ref:
                    string_vars[name] = int(value_ref)

            return string_vars
        except Exception as e:
            raise Exception(f"Error parsing XML file: {e}")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3SetString(struct_file_path="prova_struct.h", xml_file_path="modelDescription.xml")
    print(generator.generate())
