def get_build_script_template_bash():
    """
    Returns the template for build.sh
    """
    return """#!/bin/bash

# Variables
FMU_NAME="{fmu_name}"
FMU_VERSION="{fmu_version}"
SYSTEMC_HOME=${{SYSTEMC_HOME:-/usr/local/systemc}}

# Detect OS
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "Detected Windows"
    OS="windows"
    PLATFORM="win64"
    EXT=".dll"
    CC=${{CC:-g++}}
    LIB_PATH="$SYSTEMC_HOME/lib"
    PATH_SEP=";"
else
    echo "Detected Linux"
    OS="linux"
    PLATFORM="x86_64-linux"
    EXT=".so"
    CC=${{CC:-g++}}
    LIB_PATH="$SYSTEMC_HOME/lib-linux64"
    PATH_SEP=":"
fi

# Set the library path
if [ "$OS" == "windows" ]; then
    export PATH="$LIB_PATH:$PATH"
else
    export LD_LIBRARY_PATH="$LIB_PATH$PATH_SEP$LD_LIBRARY_PATH"
fi

# Clean the binaries folders
rm -rf binaries/$PLATFORM/*
mkdir -p binaries/$PLATFORM

# Compile the FMU shared library
$CC -std=c++14 -shared -fPIC \\
    -I$SYSTEMC_HOME/include \\
    -I./include \\
    -I./src/ \\
    -I./{modules_folder}/ \\
    -L$LIB_PATH \\
    -o binaries/$PLATFORM/${{FMU_NAME}}${{EXT}} \\
    src/*.cpp \\
    {modules_folder}/*.cpp \\
    -lsystemc -lpthread

# Check compilation success
if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi

# Check the shared library dependencies
if [ "$OS" == "windows" ]; then
    objdump -p binaries/$PLATFORM/${{FMU_NAME}}${{EXT}} | grep "DLL"
else
    ldd binaries/$PLATFORM/${{FMU_NAME}}${{EXT}}
fi

if [ $? -ne 0 ]; then
    echo "Dependency check failed"
    exit 1
fi

# Zip the FMU
zip -r ${{FMU_NAME}}.fmu modelDescription.xml binaries/ resources/
if [ $? -ne 0 ]; then
    echo "FMU zipping failed"
    exit 1
fi

# Cleanup
rm -rf binaries/

echo "FMU creation complete: ${{FMU_NAME}}_v${{FMU_VERSION}}.fmu"
"""


def get_build_script_template_cmake():
    """
    Returns the template for CMakeLists.txt
    """
    return """cmake_minimum_required(VERSION 3.10)
project(SystemC_FMI VERSION 1.0)

# Set FMU properties
set(FMU_NAME "{fmu_name}" CACHE STRING "Name of the FMU")
set(FMU_VERSION "{fmu_version}" CACHE STRING "Version of the FMU")

# Find SystemC
if(NOT DEFINED SYSTEMC_HOME)
    if(DEFINED ENV{{SYSTEMC_HOME}})
        set(SYSTEMC_HOME $ENV{{SYSTEMC_HOME}})
    else()
        set(SYSTEMC_HOME "/usr/local/systemc" CACHE PATH "Path to SystemC installation")
    endif()
endif()

# Set platform-specific variables
if(WIN32)
    set(PLATFORM "win64")
    set(LIB_SUFFIX ".dll")
    set(SYSTEMC_LIB_DIR "${{SYSTEMC_HOME}}/lib")
else()
    set(PLATFORM "x86_64-linux")
    set(LIB_SUFFIX ".so")
    set(SYSTEMC_LIB_DIR "${{SYSTEMC_HOME}}/lib-linux64")
endif()

# Configure output directories
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/binaries/${{PLATFORM}})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{CMAKE_BINARY_DIR}}/binaries/${{PLATFORM}})

# Include directories
include_directories(
    ${{SYSTEMC_HOME}}/include
    ${{CMAKE_SOURCE_DIR}}/include
    ${{CMAKE_SOURCE_DIR}}/src
    ${{CMAKE_SOURCE_DIR}}/{modules_folder}
)

# Link directories
link_directories(${{SYSTEMC_LIB_DIR}})

# Collect source files
file(GLOB SOURCES 
    ${{CMAKE_SOURCE_DIR}}/src/*.cpp
    ${{CMAKE_SOURCE_DIR}}/{modules_folder}/*.cpp
)

# Create shared library
add_library(${{FMU_NAME}} SHARED ${{SOURCES}})
set_target_properties(${{FMU_NAME}} PROPERTIES
    CXX_STANDARD 14
    CXX_STANDARD_REQUIRED ON
    PREFIX ""
)

# Link with SystemC
target_link_libraries(${{FMU_NAME}} systemc pthread)

# Custom target to create FMU
add_custom_target(fmu ALL
    COMMAND ${{CMAKE_COMMAND}} -E make_directory ${{CMAKE_BINARY_DIR}}/fmu/binaries/${{PLATFORM}}
    COMMAND ${{CMAKE_COMMAND}} -E copy $<TARGET_FILE:${{FMU_NAME}}> ${{CMAKE_BINARY_DIR}}/fmu/binaries/${{PLATFORM}}/
    COMMAND ${{CMAKE_COMMAND}} -E copy ${{CMAKE_SOURCE_DIR}}/modelDescription.xml ${{CMAKE_BINARY_DIR}}/fmu/
    COMMAND ${{CMAKE_COMMAND}} -E make_directory ${{CMAKE_BINARY_DIR}}/fmu/resources
    COMMAND ${{CMAKE_COMMAND}} -E chdir ${{CMAKE_BINARY_DIR}}/fmu zip -r ${{CMAKE_SOURCE_DIR}}/${{FMU_NAME}}.fmu modelDescription.xml binaries/ resources/
    DEPENDS ${{FMU_NAME}}
    COMMENT "Creating FMU archive"
)
"""