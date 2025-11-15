import shutil
import subprocess
import sys
from pathlib import Path
from .build_template import get_build_script_template_bash, get_build_script_template_cmake


def generate_build_script_bash(fmu_name, modules_folder, fmi_version="3.0"):
    """
    Generate the build.sh script from the template.
    
    Args:
        fmu_name: Name of the FMU to build
        fmu_version: Version of the FMU
        systemc_home: Path to SystemC installation (uses env var if None)
    
    Returns:
        Path to the generated build script
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src"
    build_script = src_dir / "build.sh"
    
    # Get template and replace variables
    script_content = get_build_script_template_bash().format(
        fmu_name=fmu_name,
        fmu_version=fmi_version,
        modules_folder=modules_folder
    )

    # Write the build script
    with open(build_script, 'w') as f:
        f.write(script_content)
    
    # Make the script executable
    # build_script.chmod(build_script.stat().st_mode | 0o755)
    
    print(f"Build script generated at {build_script}")
    return build_script

def generate_build_script_cmake(fmu_name, modules_folder, fmi_version="3.0"):
    """
    Generate the CMakeLists.txt script from the template.
    
    Args:
        fmu_name: Name of the FMU to build
        fmu_version: Version of the FMU
        systemc_home: Path to SystemC installation (uses env var if None)
    
    Returns:
        Path to the generated build script
    """
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src"
    build_script = src_dir / "CMakeLists.txt"
    
    # Get template and replace variables
    script_content = get_build_script_template_cmake().format(
        fmu_name=fmu_name,
        fmu_version=fmi_version,
        modules_folder=modules_folder
    )

    # Write the build script
    with open(build_script, 'w') as f:
        f.write(script_content)
    
    print(f"Build script generated at {build_script}")
    return build_script

def run_build_script_bash():
    # Get the project root directory (assuming we're in src/compile)
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src"
    build_script = src_dir / "build.sh"

    # Ensure the build script exists and is executable
    if not build_script.exists():
        print(f"Error: Build script not found at {build_script}")
        return False
    
    # Make the script executable
    # build_script.chmod(build_script.stat().st_mode | 0o755)

    try:
        # Run the build script from src directory
        process = subprocess.Popen(
            ["bash", str(build_script)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=src_dir,
            universal_newlines=True
        )

        # Print output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # Get the return code
        return_code = process.poll()

        # Print any errors
        if return_code != 0:
            _, stderr = process.communicate()
            print(f"Build failed with error:\n{stderr}", file=sys.stderr)
            return False

        return True

    except Exception as e:
        print(f"Error running build script: {e}", file=sys.stderr)
        return False
    
def run_build_script_cmake():
    # Get the project root directory (assuming we're in src/compile)
    project_root = Path(__file__).parent.parent.parent
    src_dir = project_root / "src"
    build_dir = src_dir / "build"
    build_script = src_dir / "CMakeLists.txt"

    # Ensure the build script exists
    if not build_script.exists():
        print(f"Error: CMakeLists.txt not found at {build_script}")
        return False
    
    # Delete build directory if it exists
    if build_dir.exists():
        print("Deleting existing build directory...")
        for item in build_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    # Create build directory
    build_dir.mkdir(exist_ok=True)
    
    try:
        # Step 1: Configure CMake
        print("Configuring CMake...")
        process = subprocess.Popen(
            ["cmake", ".."],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=build_dir,
            universal_newlines=True
        )

        # Print output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # Get the return code
        return_code = process.poll()

        # Print any errors
        if return_code != 0:
            _, stderr = process.communicate()
            print(f"CMake configuration failed with error:\n{stderr}", file=sys.stderr)
            return False

        # Step 2: Build the project
        print("\nBuilding project...")
        process = subprocess.Popen(
            ["cmake", "--build", "."],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=build_dir,
            universal_newlines=True
        )

        # Print output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # Get the return code
        return_code = process.poll()

        # Print any errors
        if return_code != 0:
            _, stderr = process.communicate()
            print(f"Build failed with error:\n{stderr}", file=sys.stderr)
            return False

        print("Build completed successfully!")
        return True

    except Exception as e:
        print(f"Error running build script: {e}", file=sys.stderr)
        return False