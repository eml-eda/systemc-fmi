from fmi3_modules.fmi3_getters import getters_modules
from fmi3_modules.fmi3_others import other_modules
from fmi3_modules.fmi3_setters import setter_modules


def generate_all_modules(config: dict):
    """Generate and write code for all FMI3 modules"""
    generate_all_getters(config=config)
    generate_all_others(config=config)
    generate_all_setters(config=config)

def generate_all_getters(config: dict):
    """Generate and write code for all FMI3 getters"""
    for module in getters_modules:
        filename = module.generate(config=config)
        filename = module.write_to_file(path="src")
        if filename:
            print(f"Generated {filename}")
        else:
            print(f"Failed to generate {module.__class__.__name__}")

def generate_all_others(config: dict):
    """Generate and write code for all FMI3 others"""
    for module in other_modules:
        filename = module.generate(config=config)
        filename = module.write_to_file(path="src")
        if filename:
            print(f"Generated {filename}")
        else:
            print(f"Failed to generate {module.__class__.__name__}")

def generate_all_setters(config: dict):
    """Generate and write code for all FMI3 setters"""
    for module in setter_modules:
        filename = module.generate(config=config)
        filename = module.write_to_file(path="src")
        if filename:
            print(f"Generated {filename}")
        else:
            print(f"Failed to generate {module.__class__.__name__}")


def debug_single_module():
    """Generate and write code for a single FMI3 module"""

    # from fmi3.fmi3DoStep import fmi3DoStep
    # from fmi3.fmi3GetFloat32 import fmi3GetFloat32
    from fmi3.fmi3InstantiateCoSimulation import fmi3InstantiateCoSimulation
    # module = fmi3DoStep(
    #     struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    # )

    # module = fmi3GetFloat32(
    #     struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    # )

    module = fmi3InstantiateCoSimulation(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    )
    filename = module.generate()
    filename = module.write_to_file(path="src")
    if filename:
        print(f"Generated {filename}")
    else:
        print(f"Failed to generate {module.__class__.__name__}")



if __name__ == "__main__":
    print("Generating FMI3 module implementations...")
    generate_all_modules()
    # debug_single_module()
    
    # generate_all_getters()
    # generate_all_others()
    # generate_all_setters()
    print("Done!")
