from fmi3.base_fmi3_module import BaseFMI3Module
import re
import xml.etree.ElementTree as ET


class fmi3DoStep(BaseFMI3Module):
    def __init__(self, struct_file_path=None, xml_file_path=None):
        template = """fmi3Status fmi3DoStep(  fmi3Instance instance,
                                fmi3Float64 currentCommunicationPoint,
                                fmi3Float64 communicationStepSize,
                                fmi3Boolean noSetFMUStatePriorToCurrentPoint,
                                fmi3Boolean* eventHandlingNeeded,
                                fmi3Boolean* terminateSimulation,
                                fmi3Boolean* earlyReturn,
                                fmi3Float64* lastSuccessfulTime)  {{
    
    {custom_code}
    return fmi3OK;
}}
"""
        self.xml_file_path = xml_file_path
        self.struct_file_path = struct_file_path
        if not self.struct_file_path:
            super().__init__(template)
        else:
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
                variables=variables, struct_name=struct_name, config=config
            )
        elif config["type"] == "tlm":
            custom_code = self.generate_custom_code_tlm(variables=variables, struct_name=struct_name, config=config)
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

    def generate_custom_code(self, variables, struct_name, config):
        custom_code = ""
        custom_code += f"{struct_name} *fmu = ({struct_name} *)instance;\n\n"
        custom_code += f"sc_time step_size(communicationStepSize, SC_SEC);\n"
        custom_code += f"sc_time next_time = fmu->current_time + step_size;\n"
        custom_code += "fmu -> current_time = next_time;\n"
        custom_code += "sc_start(step_size);\n\n"

        # Remove "current_time" from variables
        variables.remove("current_time")
        variables.remove("time")

        systemc_module_name: str = variables[-1]
        variables.remove(systemc_module_name)
        for variable in variables:
            custom_code += (
                f"fmu->{variable} = fmu->{systemc_module_name}->{variable}.read();\n"
            )
        return custom_code
    
    def generate_custom_code_tlm(self, variables, struct_name, config):
        custom_code = ""
        custom_code += f"{struct_name} *fmu = ({struct_name} *)instance;\n\n"
        custom_code += f"sc_time step_size(communicationStepSize, SC_SEC);\n"
        custom_code += f"sc_time next_time = fmu->current_time + step_size;\n\n"
        custom_code += f"{config['tlm']['tlm_top_level_module_payload_struct_name']} payload;\n"
        
        # Remove "current_time" from variables
        variables.remove("current_time")
        tlm_top_module_name: str = variables[-1]
        variables.remove(tlm_top_module_name)
        for variable in variables:
            custom_code += f"payload.{variable} = fmu->{variable};\n"
        
        custom_code += f"\n{config['tlm']['tlm_top_level_module_payload_struct_name']} result = fmu->{tlm_top_module_name}->send_data(payload);\n"

        for variable in variables:
            custom_code += f"fmu->{variable} = result.{variable};\n"

        custom_code += "\nfmu -> current_time = next_time;\n\n"
        
        return custom_code



if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3DoStep(struct_file_path="prova_struct.h")
    print(generator.generate())
