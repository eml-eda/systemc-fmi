from fmi3.base_fmi3_module import BaseFMI3Module
import re
import xml.etree.ElementTree as ET


class fmi3InstantiateCoSimulation(BaseFMI3Module):
    def __init__(self, struct_file_path=None, xml_file_path=None):
        template = """
fmi3Instance fmi3InstantiateCoSimulation(
    fmi3String instanceName,
    fmi3String instantiationToken,
    fmi3String resourcePath,
    fmi3Boolean visible,
    fmi3Boolean loggingOn,
    fmi3Boolean eventModeUsed,
    fmi3Boolean earlyReturnAllowed,
    const fmi3ValueReference requiredIntermediateVariables[],
    size_t nRequiredIntermediateVariables,
    fmi3InstanceEnvironment instanceEnvironment,
    fmi3LogMessageCallback logMessage,
    fmi3IntermediateUpdateCallback intermediateUpdate) {{
    
    {custom_code}
    return (fmi3Instance *)fmu;
}}
"""
        self.xml_file_path = xml_file_path
        self.struct_file_path = struct_file_path
        super().__init__(
            template=template,
            includes=["struct.h"],
            struct_file_path=struct_file_path,
            xml_file_path=xml_file_path,
        )

    def generate(self, config: dict):
        if not self.struct_file_path:
            # Return standard template with empty custom code
            self.template = self.template.format(custom_code="")
            return self.format_code(style="LLVM")
        try:
            with open(self.struct_file_path, "r") as f:
                struct_content = f.read()
        except Exception as e:
            raise Exception(f"Error reading struct file: {e}")
        variables = self.parse_struct(struct_content)
        struct_name = self.get_struct_name(struct_content)
        if config["type"] == "rtl":
            custom_code = self.generate_custom_code(
                variables=variables, struct_name=struct_name
            )
        else:
            custom_code = self.generate_custom_code_tlm(
                variables=variables, struct_name=struct_name
            )
        self.template = self.template.format(custom_code=custom_code)
        return self.format_code(style="LLVM")

    def parse_struct(self, struct_content):
        variables = []
        lines = struct_content.split("\n")

        # Pattern to match variable declarations including pointers
        variable_pattern = r"(?:(\w+(?:<[\w<>:]+>)?)\s+)?\*?\s*(\w+);"

        for line in lines:
            # Stop when we reach signals declaration
            if "signals declaration" in line or "s_" in line:
                break

            # Skip comments and empty lines
            if line.strip().startswith("//") or not line.strip():
                continue

            matches = re.findall(variable_pattern, line)
            for _, variable_name in matches:
                if variable_name:  # Ensure we don't add empty matches
                    variables.append(variable_name)

        return variables

    def get_struct_name(self, struct_content):
        struct_pattern = r"struct\s+(\w+)"
        match = re.search(struct_pattern, struct_content)
        return match.group(1)

    def generate_custom_code(self, variables, struct_name):
        custom_code = ""
        custom_code += f"{struct_name} *fmu = new {struct_name}();\n"

        # Reverse the list
        variables = variables[::-1]
        variables.remove("time")

        systemc_module_name: str = "_".join(variables[0].split("_")[1:])
        for variable in variables:
            if variable == variables[0]:
                custom_code += f'fmu->{variable} = new {systemc_module_name}("{systemc_module_name}");\n'
            elif variable == "current_time":
                custom_code += f"fmu->{variable} = sc_time(0, SC_SEC);\n"
            else:
                custom_code += f"fmu->{variables[0]}->{variable}(fmu->s_{variable});\n"
        return custom_code

    def generate_custom_code_tlm(self, variables, struct_name):
        custom_code = ""
        custom_code += f"{struct_name} *fmu = new {struct_name}();\n"
        # Reverse the list
        variables = variables[::-1]
        tlm_module_name: str = "_".join(variables[0].split("_")[1:])
        custom_code += (
            f'fmu->{variables[0]} = new {tlm_module_name}("{tlm_module_name}");\n'
        )
        custom_code += f"fmu->current_time = sc_time(0, SC_NS);\n"
        return custom_code


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3InstantiateCoSimulation(struct_file_path="prova_struct.h")
    print(generator.generate())
