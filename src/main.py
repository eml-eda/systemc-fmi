import argparse
from simulator.fmu_simulator import FMUSimulator
import yaml
from generators.xml_generator import generate_fmi_xml, generate_fmi_xml_tlm, generate_struct, generate_struct_tlm, write_to_file
from generators.generate_fmi3_code import generate_all_modules
from compile_fmu.compile_fmu import run_build_script_bash, generate_build_script_bash, run_build_script_cmake, generate_build_script_cmake
import sys

def isr_zero():
    print("[ZERO] Interrupt handled")

def isr_carry():
    print("[CARRY] Interrupt handled")

def isr_result():
    print("[RESULT] Interrupt handled")

def load_stimuli(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def simulate_fmu(fmu_path: str, stop_time: float, step_size: float, stimuli_path: str):
    simulator = FMUSimulator(
        fmu_path=fmu_path,
        stop_time=stop_time,
        step_size=step_size,
    )

    simulator.setup_model()
    simulator.initialize_fmu()

    # Load and set input schedules from stimuli file
    stimuli = load_stimuli(stimuli_path)
    for signal, schedule in stimuli.items():
        if "clk" in signal.lower():
            period = stimuli[signal]["period"]
            schedule = {}
            time = 0
            while time < stop_time:
                schedule[time] = 0
                time += period/2
                schedule[time] = 1
                time += period/2
        if signal.lower() != "interrupt":
            simulator.set_input_schedule(signal, schedule)
        else:
            for interrupt, condition in stimuli[signal].items():
                simulator.register_interrupt(name=interrupt, condition=condition, handler=eval(condition["isr"]))

    csv_output = simulator.run_simulation()
    return csv_output


def generate_xml_struct(config: dict):

    if config["type"] == "rtl":
        systemc_modules_folder = config["rtl"]["systemc_modules_folder"]
        systemc_top_level_module_source_file_path = config["rtl"][
            "systemc_top_level_module_source_file_path"
        ]
        systemc_top_level_module_header_file_path = config["rtl"][
            "systemc_top_level_module_header_file_path"
        ]

        with open(systemc_top_level_module_header_file_path, "r") as file:
            systemc_header = file.read()

        xml_output = generate_fmi_xml(systemc_content=systemc_header, config=config)
        write_to_file(xml_output, config["xml_output_file_path"])

        struct_output = generate_struct(systemc_content=systemc_header, config=config)
        write_to_file(struct_output, config["struct_output_file_path"])
    elif config["type"] == "tlm":
        tlm_modules_folder = config["tlm"]["tlm_modules_folder"]
        tlm_top_level_module_payload_file_path = config["tlm"][
            "tlm_top_level_module_payload_file_path"
        ]

        with open(tlm_top_level_module_payload_file_path, "r") as file:
            tlm_payload = file.read()

        xml_output = generate_fmi_xml_tlm(tlm_content=tlm_payload, config=config)
        write_to_file(xml_output, config["xml_output_file_path"])

        struct_output = generate_struct_tlm(tlm_content=tlm_payload, config=config)
        write_to_file(struct_output, config["struct_output_file_path"])



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fmu_path", type=str, required=False, help="FMU folder path")
    parser.add_argument(
        "--stop_time", type=float, default=5.0, help="Simulation stop time"
    )
    parser.add_argument(
        "--step_size", type=float, default=0.05, help="Simulation step size"
    )
    parser.add_argument(
        "--stimuli_path",
        type=str,
        default="stimuli.yaml",
        required=False,
        help="Path to stimuli file",
    )
    parser.add_argument(
        "--config_file_path",
        type=str,
        default="config.yaml",
        required=False,
        help="Path to config file",
    )
    args = parser.parse_args()

    with open(args.config_file_path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    generate_xml_struct(config=config)
    generate_all_modules(config=config)

    if config["type"] == "rtl":
        if "compile" in config and "type" in config["compile"]:
            if config["compile"]["type"] == "bash":
                generate_build_script_bash(
                    fmu_name=config["rtl"]["systemc_top_level_module_name"],
                    fmi_version=config["fmi_config"]["fmiVersion"],
                    modules_folder=config["rtl"]["systemc_modules_folder"],
                )
            elif config["compile"]["type"] == "cmake":
                generate_build_script_cmake(
                    fmu_name=config["rtl"]["systemc_top_level_module_name"],
                    fmi_version=config["fmi_config"]["fmiVersion"],
                    modules_folder=config["rtl"]["systemc_modules_folder"],
                )
            else:
                print("Invalid compile type")
                sys.exit(1)
        else:
            generate_build_script_bash(
                fmu_name=config["rtl"]["systemc_top_level_module_name"],
                fmi_version=config["fmi_config"]["fmiVersion"],
                modules_folder=config["rtl"]["systemc_modules_folder"],
            )
    elif config["type"] == "tlm":
        if "compile" in config and "type" in config["compile"]:
            if config["compile"]["type"] == "bash":
                generate_build_script_bash(
                    fmu_name=config["tlm"]["tlm_top_level_module_name"],
                    fmi_version=config["fmi_config"]["fmiVersion"],
                    modules_folder=config["tlm"]["tlm_modules_folder"],
                )
            elif config["compile"]["type"] == "cmake":
                generate_build_script_cmake(
                    fmu_name=config["tlm"]["tlm_top_level_module_name"],
                    fmi_version=config["fmi_config"]["fmiVersion"],
                    modules_folder=config["tlm"]["tlm_modules_folder"],
                )
            else:
                print("Invalid compile type")
                sys.exit(1)
        else:
            generate_build_script_bash(
                fmu_name=config["tlm"]["tlm_top_level_module_name"],
                fmi_version=config["fmi_config"]["fmiVersion"],
                modules_folder=config["tlm"]["tlm_modules_folder"],
            )

    if "compile" in config and "type" in config["compile"]:
        if config["compile"]["type"] == "bash":
            if not run_build_script_bash():
                sys.exit(1)
        elif config["compile"]["type"] == "cmake":
            if not run_build_script_cmake():
                sys.exit(1)
        else:
            print("Invalid compile type")
            sys.exit(1)
    else:
        if not run_build_script_bash():
            sys.exit(1)


    csv_output = simulate_fmu(
        fmu_path=args.fmu_path,
        stop_time=args.stop_time,
        step_size=args.step_size,
        stimuli_path=args.stimuli_path,
    )
    
    with open("output.csv", "w") as file:
        file.write(csv_output)
    
    return csv_output


if __name__ == "__main__":
    main()
