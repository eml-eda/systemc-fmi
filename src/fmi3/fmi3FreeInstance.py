from fmi3.base_fmi3_module import BaseFMI3Module
import re
import xml.etree.ElementTree as ET


class fmi3FreeInstance(BaseFMI3Module):
    def __init__(self, struct_file_path=None, xml_file_path=None):
        template = """
        void fmi3FreeInstance(fmi3Instance instance) {{
        {custom_code}
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
            self.template = self.template.format(custom_code="")
            return self.format_code(style="LLVM")
        try:
            with open(self.struct_file_path, "r") as f:
                struct_content = f.read()
        except Exception as e:
            raise Exception(f"Error reading struct file: {e}")

        struct_name = self.get_struct_name(struct_content)

        custom_code = self.generate_custom_code(struct_name=struct_name)
        self.template = self.template.format(custom_code=custom_code)
        return self.format_code(style="LLVM")

    def get_struct_name(self, struct_content):
        struct_pattern = r"struct\s+(\w+)"
        match = re.search(struct_pattern, struct_content)
        return match.group(1)

    def generate_custom_code(self, struct_name):
        custom_code = ""
        custom_code += f"{struct_name} *fmu = ({struct_name} *)instance;\n"

        # Free the instance
        custom_code += f"delete fmu;\n"

        return custom_code


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3FreeInstance(struct_file_path="prova_struct.h")
    print(generator.generate())
