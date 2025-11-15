import subprocess
import tempfile
import os
from typing import List
import xml.etree.ElementTree as ET
import re


class BaseFMI3Module:
    def __init__(
        self,
        template: str,
        includes: List[str] = None,
        defines: List[str] = None,
        struct_file_path=None,
        xml_file_path=None,
    ):
        """Initialize the FMI3 module with template and includes.

        Args:
            template (str): The main template code
            includes (List[str], optional): List of header files to include. Defaults to None.
            defines (List[str], optional): List of preprocessor definitions. Defaults to None.
            struct_file_path (str, optional): Path to struct file. Defaults to None.
            xml_file_path (str, optional): Path to XML file. Defaults to None.
        """
        self.xml_file_path = xml_file_path
        self.struct_file_path = struct_file_path

        # Default includes
        self.includes = ["fmi3Functions.h"]

        # Add additional includes if provided
        if includes:
            self.includes.extend(includes)

        # Generate include statements
        include_statements = "\n".join(
            [f'#include "{include}"' for include in self.includes]
        )

        # Generate define statements
        define_statements = ""
        if defines:
            define_statements = (
                "\n".join([f"#define {define}" for define in defines]) + "\n\n"
            )

        # Combine includes, defines, and template
        self.template = f"{include_statements}\n\n{define_statements}{template}"

    def generate_unused_macros(self, params):
        """Generate UNUSED macro calls for each parameter"""
        return "\n        ".join([f"UNUSED({param});" for param in params])

    def format_code(self, style: str = "LLVM", spaces: int = 4):
        """Format the generated code using clang-format

        Args:
            style (str): The formatting style to use (LLVM, Google, Chromium, Mozilla, WebKit)
            spaces (int): Number of spaces for indentation. Defaults to 4.

        Returns:
            str: The formatted code
        """
        # Create style configuration with custom indentation
        style_config = {
            "BasedOnStyle": style,
            "IndentWidth": spaces,
            "TabWidth": spaces,
            "UseTab": "Never",
        }
        style_str = str(style_config).replace("'", '"')  # Convert to JSON-like string

        with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp") as tmp:
            # Write the code to a temporary file
            tmp.write(self.template)
            tmp.flush()

            # Run clang-format with custom style
            try:
                result = subprocess.run(
                    ["clang-format", f"--style={style_str}", tmp.name],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return result.stdout
            except subprocess.CalledProcessError as e:
                print(f"Error formatting code: {e}")
                return self.template
            except FileNotFoundError:
                print("clang-format not found. Please install it first.")
                return self.template

    def write_to_file(self, path: str = None):
        """Write the generated code to file

        Writes the formatted code to a .cpp file named after the class.
        The code is formatted using clang-format before writing.

        Returns:
            str: Path to the written file
        """
        # Get class name and create filename
        class_name = self.__class__.__name__
        filename = f"{path}/{class_name}.cpp" if path else f"{class_name}.cpp"

        if not os.path.exists(path):
            os.makedirs(path)

        # Format the code before writing
        formatted_code = self.format_code()

        try:
            with open(filename, "w") as f:
                f.write(formatted_code)
            return filename
        except IOError as e:
            print(f"Error writing to file {filename}: {e}")
            return None

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
            # enum_definitions = self.generate_enum_definitions(xml_vr)
            custom_code = self.generate_custom_code(
                variables=variables, xml_vr=xml_vr, struct_name=struct_name
            )
        else:
            # enum_definitions = ""
            custom_code = ""

        self.template = self.template % {
            "custom_code": custom_code,
            # "enum_definitions": enum_definitions,
        }

        return self.format_code(style="LLVM")
