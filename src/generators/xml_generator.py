import re
import uuid
from dataclasses import dataclass
from typing import List
import xml.etree.ElementTree as ET
from xml.dom import minidom
import yaml


@dataclass
class SystemCPort:
    direction: str  # 'in' or 'out'
    data_type: str
    name: str
    width: int = None


@dataclass
class TLMPayloadField:
    direction: str  # 'in', 'out'
    data_type: str
    name: str
    width: int = None


class SystemCParser:
    def __init__(self):
        self.module_name = ""
        self.ports = []

    def parse_systemc_file(self, content: str, module_name: str):
        # Extract module name
        module_match = re.search(r"SC_MODULE\((.*?)\)", content)
        if module_match:
            # Check that the module name is the same as the module_match.group(1)
            if module_name != module_match.group(1):
                # Print the line that matches the regex
                raise ValueError(
                    f"Extracting the module name from {module_match.group(0)}. The extracted module name is {module_match.group(1)} but the provided module name is {module_name}. Keep the module name consistent."
                )
            self.module_name = module_match.group(1)

        # Find all port declarations
        port_pattern = r"sc_(in|out)\s*<\s*([\w<>]+)\s*>\s*([\w,\s]+);"
        port_declarations = re.finditer(port_pattern, content)

        for decl in port_declarations:
            direction, data_type, names = decl.groups()

            # Split multiple port declarations (e.g., "OP1,OP2")
            port_names = [name.strip() for name in names.split(",")]

            # Extract bit width if present
            width = None
            if "<" in data_type:
                width_match = re.search(r"uint<(\d+)>", data_type)
                if width_match:
                    width = int(width_match.group(1))
                    data_type = "uint"

            # Create a port object for each name in the declaration
            for name in port_names:
                self.ports.append(
                    SystemCPort(
                        direction=direction, data_type=data_type, name=name, width=width
                    )
                )


class TLMParser:
    def __init__(self):
        self.module_name = "Top"
        self.ports = []

    def parse_payload_file(
        self, content: str, payload_name: str
    ) -> List[TLMPayloadField]:
        """Parse a TLM payload structure from a header file."""
        # Find the struct or typedef struct definition
        struct_pattern = r"typedef\s+struct\s+{([\s\S]*?)}\s*" + payload_name + ";"
        struct_match = re.search(struct_pattern, content)
        if not struct_match:
            # Try alternative pattern without typedef
            struct_pattern = r"struct\s+" + payload_name + "\s+{([\s\S]*?)};"
            struct_match = re.search(struct_pattern, content)

        if struct_match:
            struct_body = struct_match.group(1)

            # Extract fields - updated pattern to ignore direction declarations
            field_pattern = r"(\w+)\s+(\w+)(?:\s*\[\s*(\d+)\s*\])?;"
            field_matches = re.finditer(field_pattern, struct_body)

            # First collect all fields
            field_data = {}
            for match in field_matches:
                data_type, name, array_size = match.groups()
                # Skip direction fields (fields ending with "_dir")
                if name.endswith("_dir"):
                    continue
                width = int(array_size) if array_size else None
                field_data[name] = {
                    "data_type": data_type,
                    "width": width,
                    "direction": None,
                }

            # Now look for direction information
            dir_pattern = r"PortDirection\s+(\w+)_dir\s*=\s*(PORT_\w+);"
            dir_matches = re.finditer(dir_pattern, struct_body)

            for match in dir_matches:
                field_name, direction = match.groups()
                if field_name in field_data:
                    # Convert PORT_INPUT to 'in', PORT_OUTPUT to 'out', etc.
                    direction_map = {
                        "PORT_INPUT": "in",
                        "PORT_OUTPUT": "out",
                    }
                    field_data[field_name]["direction"] = direction_map.get(
                        direction, "unknown"
                    )

            # Convert to TLMPayloadField objects
            self.ports = []
            for name, data in field_data.items():
                self.ports.append(
                    TLMPayloadField(
                        name=name,
                        data_type=data["data_type"],
                        width=data["width"],
                        direction=data["direction"],
                    )
                )

        return self.ports  # Return the payload fields


class FMIGenerator:
    def __init__(self, parser: SystemCParser | TLMParser, config: dict):
        self.parser = parser
        self.config = config

    def generate_xml(self) -> str:
        default_experiment_config = self.config["fmi_config"]["DefaultExperiment"]
        cosimulation_config = self.config["fmi_config"]["CoSimulation"]
        log_categories_config = self.config["fmi_config"]["LogCategories"]

        # Create root element
        root = ET.Element("fmiModelDescription")
        root.set("fmiVersion", self.config["fmi_config"]["fmiVersion"])
        root.set("modelName", self.parser.module_name)
        root.set("instantiationToken", str(uuid.uuid4()))

        # Add CoSimulation element
        cosimulation = ET.SubElement(root, "CoSimulation")
        cosimulation.set("modelIdentifier", self.parser.module_name)
        cosimulation.set(
            "canGetAndSetFMUState", str(cosimulation_config["canGetAndSetFMUState"])
        )
        cosimulation.set(
            "canSerializeFMUState", str(cosimulation_config["canSerializeFMUState"])
        )
        cosimulation.set(
            "canHandleVariableCommunicationStepSize",
            str(cosimulation_config["canHandleVariableCommunicationStepSize"]),
        )
        cosimulation.set(
            "providesIntermediateUpdate",
            str(cosimulation_config["providesIntermediateUpdate"]),
        )
        cosimulation.set(
            "canReturnEarlyAfterIntermediateUpdate",
            str(cosimulation_config["canReturnEarlyAfterIntermediateUpdate"]),
        )
        cosimulation.set(
            "fixedInternalStepSize", str(cosimulation_config["fixedInternalStepSize"])
        )
        cosimulation.set("hasEventMode", str(cosimulation_config["hasEventMode"]))

        # Add LogCategories
        log_cats = ET.SubElement(root, "LogCategories")
        for log_category in log_categories_config:
            category = ET.SubElement(log_cats, "Category")
            category.set("name", log_category["name"])
            category.set("description", log_category["description"])

        # Add DefaultExperiment
        exp = ET.SubElement(root, "DefaultExperiment")
        exp.set("startTime", str(default_experiment_config["startTime"]))
        exp.set("stopTime", str(default_experiment_config["stopTime"]))
        exp.set("stepSize", str(default_experiment_config["stepSize"]))

        # Add ModelVariables
        vars_elem = ET.SubElement(root, "ModelVariables")

        # Add time variable
        time_var = ET.SubElement(vars_elem, "Float64")
        time_var.set("name", "time")
        time_var.set("valueReference", "0")
        time_var.set("causality", "independent")
        time_var.set("variability", "continuous")
        time_var.set("description", "Simulation time")

        # Add port variables
        port: SystemCPort
        for i, port in enumerate(self.parser.ports, 1):
            # Determine variable type based on data type and width
            if port.data_type == "bool":
                var_type = "Boolean"
            elif port.data_type == "uint":
                if port.width is not None:
                    if port.width <= 8:
                        var_type = "UInt8"
                    elif port.width <= 16:
                        var_type = "UInt16"
                    elif port.width <= 32:
                        var_type = "UInt32"
                    elif port.width <= 64:
                        var_type = "UInt64"
                    else:
                        raise ValueError(f"Unsupported width for uint: {port.width}")
                else:
                    var_type = "UInt32"
            elif port.data_type == "int":
                if port.width is not None:
                    if port.width <= 8:
                        var_type = "Int8"
                    elif port.width <= 16:
                        var_type = "Int16"
                    elif port.width <= 32:
                        var_type = "Int32"
                    elif port.width <= 64:
                        var_type = "Int64"
                    else:
                        raise ValueError(f"Unsupported width for int: {port.width}")
                else:
                    var_type = "Int32"
            elif port.data_type == "float":
                var_type = "Float32"
            elif port.data_type == "double":
                var_type = "Float64"
            else:
                raise ValueError(f"Unsupported data type: {port.data_type}")

            var = ET.SubElement(vars_elem, var_type)
            var.set("name", port.name)
            var.set("valueReference", str(i))
            var.set("causality", "input" if port.direction == "in" else "output")
            var.set("variability", "discrete")
            var.set("description", f"{port.name}")

            if port.direction == "in":
                var.set("initial", "exact")
                if port.data_type == "bool":
                    var.set("start", "false")
                elif port.data_type == "uint":
                    var.set("start", "0")
                elif port.data_type == "int":
                    var.set("start", "0")
                elif port.data_type == "float":
                    var.set("start", "0.0")
                elif port.data_type == "double":
                    var.set("start", "0.0")

        # Add ModelStructure
        structure = ET.SubElement(root, "ModelStructure")
        value_refs = []
        # Add outputs to structure
        output_ports = [p for p in self.parser.ports if p.direction == "out"]
        for port in output_ports:
            output = ET.SubElement(structure, "Output")
            # Find the valueReference for this output
            for i, p in enumerate(self.parser.ports, 1):
                if p == port:
                    value_ref = str(i)
                    output.set("valueReference", value_ref)
                    value_refs.append(value_ref)
                    break
        for value_ref in value_refs:
            # Add InitialUnknown with the same valueReference as its output
            unknown = ET.SubElement(structure, "InitialUnknown")
            unknown.set("valueReference", value_ref)

        # Define a comment to be inserted at the beginning of the XML
        comment = minidom.Document().createComment(
            "This XML is automatically generated by a python script. Do not modify it manually."
        )

        # Pretty print the XML
        xml_str = ET.tostring(root, encoding="unicode")

        dom = minidom.parseString(xml_str)

        # Insert the comment at the beginning of the XML
        dom.insertBefore(comment, dom.documentElement)
        return dom.toprettyxml(indent="  ")

    def __get_systemc_top_level_module_header_file_name(self) -> str:
        """Extract the header file name from the full file path of the SystemC top-level module.

        :returns: The file name of the SystemC top-level module header file without the path.
        :rtype: str

        :note: This method assumes that the "systemc_top_level_module_header_file_path" key
               exists in the configuration dictionary and contains a valid file path.
               It uses standard path manipulation by splitting on '/' characters and
               taking the last element, which works on Unix-like systems and Windows
               when using forward slashes in paths.

        :example:
            If self.config["systemc_top_level_module_header_file_path"] is
            "/path/to/module_name.h", this method will return "module_name.h"
        """
        return self.config["rtl"]["systemc_top_level_module_header_file_path"].split(
            "/"
        )[-1]

    def __get_tlm_top_level_module_payload_file_name(self) -> str:
        return self.config["tlm"]["tlm_top_level_module_header_file_path"].split("/")[
            -1
        ]

    def generate_struct(self) -> str:
        struct_name = self.parser.module_name.upper() + "_SYSC"
        struct_lines = [
            f'#include "fmi3Functions.h"',
            f'#include "{self.__get_systemc_top_level_module_header_file_name()}"',
            "",
            f"struct {struct_name} {{",
            "    // Variables of the FMU",
        ]
        # Add the time variable
        struct_lines.append("    fmi3Float64 time;")

        port: SystemCPort
        for port in self.parser.ports:
            if port.data_type == "bool":
                c_type = "fmi3Boolean"
            elif port.data_type == "uint":
                if port.width is not None:
                    if port.width <= 8:
                        c_type = "fmi3UInt8"
                    elif port.width <= 16:
                        c_type = "fmi3UInt16"
                    elif port.width <= 32:
                        c_type = "fmi3UInt32"
                    elif port.width <= 64:
                        c_type = "fmi3UInt64"
                    else:
                        raise ValueError(f"Unsupported width for uint: {port.width}")
                else:
                    c_type = "fmi3UInt32"
            elif port.data_type == "int":
                if port.width is not None:
                    if port.width <= 8:
                        c_type = "fmi3Int8"
                    elif port.width <= 16:
                        c_type = "fmi3Int16"
                    elif port.width <= 32:
                        c_type = "fmi3Int32"
                    elif port.width <= 64:
                        c_type = "fmi3Int64"
                    else:
                        raise ValueError(f"Unsupported width for int: {port.width}")
                else:
                    c_type = "fmi3Int32"
            elif port.data_type == "float":
                c_type = "fmi3Float32"
            elif port.data_type == "double":
                c_type = "fmi3Float64"
            else:
                raise ValueError(f"Unsupported data type: {port.data_type}")

            struct_lines.append(f"    {c_type} {port.name};")

        struct_lines.append("\n    // SystemC variables")
        struct_lines.append("    sc_time current_time;")
        struct_lines.append(
            f"    {self.parser.module_name} *new_{self.parser.module_name};"
        )
        struct_lines.append("\n    // signals declaration")

        port: SystemCPort
        for port in self.parser.ports:
            if port.data_type == "bool":
                struct_lines.append(f"    sc_signal<bool> s_{port.name};")
            elif port.data_type == "uint":
                struct_lines.append(
                    f"    sc_signal<sc_uint<{port.width}>> s_{port.name};"
                )
            elif port.data_type == "int":
                if port.width is not None:
                    struct_lines.append(
                        f"    sc_signal<sc_int<{port.width}>> s_{port.name};"
                    )
                else:
                    struct_lines.append(f"    sc_signal<int> s_{port.name};")
            elif port.data_type == "float":
                struct_lines.append(f"    sc_signal<float> s_{port.name};")
            elif port.data_type == "double":
                struct_lines.append(f"    sc_signal<double> s_{port.name};")
            else:
                raise ValueError(f"Unsupported data type: {port.data_type}")

        struct_lines.append("};")
        return "\n".join(struct_lines)

    def generate_struct_tlm(self) -> str:
        struct_name = self.parser.module_name.upper() + "_SYSC"
        struct_lines = [
            f'#include "fmi3Functions.h"',
            f'#include "{self.__get_tlm_top_level_module_payload_file_name()}"',
            "",
            f"struct {struct_name} {{",
            "    // Variables of the FMU",
        ]

        for port in self.parser.ports:
            if port.data_type == "bool":
                c_type = "fmi3Boolean"
            elif port.data_type == "uint":
                if port.width is not None:
                    if port.width <= 8:
                        c_type = "fmi3UInt8"
                    elif port.width <= 16:
                        c_type = "fmi3UInt16"
                    elif port.width <= 32:
                        c_type = "fmi3UInt32"
                    elif port.width <= 64:
                        c_type = "fmi3UInt64"
                    else:
                        raise ValueError(f"Unsupported width for uint: {port.width}")
                else:
                    c_type = "fmi3UInt32"
            elif port.data_type == "int":
                if port.width is not None:
                    if port.width <= 8:
                        c_type = "fmi3Int8"
                    elif port.width <= 16:
                        c_type = "fmi3Int16"
                    elif port.width <= 32:
                        c_type = "fmi3Int32"
                    elif port.width <= 64:
                        c_type = "fmi3Int64"
                    else:
                        raise ValueError(f"Unsupported width for int: {port.width}")
                else:
                    c_type = "fmi3Int32"
            elif port.data_type == "float":
                c_type = "fmi3Float32"
            elif port.data_type == "double":
                c_type = "fmi3Float64"
            else:
                raise ValueError(f"Unsupported data type: {port.data_type}")

            struct_lines.append(f"    {c_type} {port.name};")

        struct_lines.append("\n    // SystemC variables")
        struct_lines.append("    sc_time current_time;")
        struct_lines.append(
            f"    {self.parser.module_name} *new_{self.parser.module_name};"
        )

        struct_lines.append("};")
        return "\n".join(struct_lines)


def generate_fmi_xml(systemc_content: str, config: dict) -> str:
    parser = SystemCParser()
    parser.parse_systemc_file(
        content=systemc_content,
        module_name=config["rtl"]["systemc_top_level_module_name"],
    )

    generator = FMIGenerator(parser=parser, config=config)
    return generator.generate_xml()


def generate_fmi_xml_tlm(tlm_content: str, config: dict) -> str:
    parser = TLMParser()
    parser.parse_payload_file(
        content=tlm_content,
        payload_name=config["tlm"]["tlm_top_level_module_payload_struct_name"],
    )

    generator = FMIGenerator(parser=parser, config=config)
    return generator.generate_xml()


def generate_struct(systemc_content: str, config: dict) -> str:
    parser = SystemCParser()
    parser.parse_systemc_file(
        content=systemc_content,
        module_name=config["rtl"]["systemc_top_level_module_name"],
    )

    generator = FMIGenerator(parser=parser, config=config)
    return generator.generate_struct()


def generate_struct_tlm(tlm_content: str, config: dict) -> str:
    parser = TLMParser()
    parser.parse_payload_file(
        content=tlm_content,
        payload_name=config["tlm"]["tlm_top_level_module_payload_struct_name"],
    )

    generator = FMIGenerator(parser=parser, config=config)
    return generator.generate_struct_tlm()


def write_to_file(content: str, output_file: str):
    with open(output_file, "w") as file:
        file.write(content)


# Example usage
if __name__ == "__main__":

    config_file_path: str = "config.yaml"
    with open(config_file_path, "r") as stream:
        try:
            config: dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    systemc_modules_folder = config["systemc_modules_folder"]
    systemc_top_level_module_source_file_path = config[
        "systemc_top_level_module_source_file_path"
    ]
    systemc_top_level_module_header_file_path = config[
        "systemc_top_level_module_header_file_path"
    ]

    with open(systemc_top_level_module_header_file_path, "r") as file:
        systemc_header = file.read()

    xml_output = generate_fmi_xml(systemc_content=systemc_header, config=config)
    write_to_file(xml_output, config["xml_output_file_path"])

    struct_output = generate_struct(systemc_content=systemc_header, config=config)
    write_to_file(struct_output, config["struct_output_file_path"])
