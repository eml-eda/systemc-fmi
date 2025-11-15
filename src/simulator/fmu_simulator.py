from fmpy import read_model_description, extract
from fmpy.fmi3 import FMU3Slave
import os
import argparse
from typing import Dict, Any, Callable, List, Optional


class FMUSimulator:
    def __init__(
        self,
        fmu_path: str,
        stop_time: float = 10.0,
        step_size: float = 0.1,
        log_enabled: bool = True,
    ):
        self.fmu_path = fmu_path
        self.start_time = 0.0
        self.stop_time = stop_time
        self.step_size = step_size
        self.log_enabled = log_enabled
        self.fmu_filepath = os.path.join(os.getcwd(), fmu_path)
        self.rows = []
        self.vrs = {}
        self.variable_info = {}
        self.input_schedules = {}  # Dictionary to store input schedules
        self.interrupt_handlers = {}  # Dictionary to store interrupt handlers
        self.interrupt_conditions = {}  # Dictionary to store interrupt conditions

    def log(self, message: str) -> None:
        if self.log_enabled:
            print(message)

    def setup_model(self) -> bool:
        if not os.path.exists(self.fmu_filepath):
            raise FileNotFoundError(f"FMU file not found: {self.fmu_filepath}")

        self.model_description = read_model_description(self.fmu_filepath)

        # Collect variable information
        for variable in self.model_description.modelVariables:
            self.vrs[variable.name] = variable.valueReference
            self.variable_info[variable.name] = {
                "type": variable.type,
                "causality": variable.causality,
                "variability": variable.variability,
                "start": getattr(variable, "start", None),
                "initial": getattr(variable, "initial", None),
            }

        # Extract the FMU
        self.unzipdir = extract(self.fmu_filepath)
        return True

    def initialize_fmu(self) -> bool:
        try:
            self.fmu = FMU3Slave(
                guid=self.model_description.guid,
                unzipDirectory=self.unzipdir,
                modelIdentifier=self.model_description.coSimulation.modelIdentifier,
                instanceName="instance",
            )
            self.fmu.instantiate()
            self.fmu.enterInitializationMode()

            # Set initial values from model description
            for var_name, info in self.variable_info.items():
                if info["initial"] == "exact" and info["start"] is not None:
                    if info["type"] == "Boolean":
                        self.fmu.setBoolean([self.vrs[var_name]], [bool(info["start"])])
                    elif info["type"] == "UInt8":
                        self.fmu.setUInt8([self.vrs[var_name]], [int(info["start"])])
                    elif info["type"] == "UInt16":
                        self.fmu.setUInt16([self.vrs[var_name]], [int(info["start"])])
                    elif info["type"] == "UInt32":
                        self.fmu.setUInt32([self.vrs[var_name]], [int(info["start"])])
                    elif info["type"] == "UInt64":
                        self.fmu.setUInt64([self.vrs[var_name]], [int(info["start"])])
                    elif info["type"] == "Int8":
                        self.fmu.setInt8([self.vrs[var_name]], [int(info["start"])])
                    elif info["type"] == "Int16":
                        self.fmu.setInt16([self.vrs[var_name]], [int(info["start"])])
                    elif info["type"] == "Int32":
                        self.fmu.setInt32([self.vrs[var_name]], [int(info["start"])])
                    elif info["type"] == "Int64":
                        self.fmu.setInt64([self.vrs[var_name]], [int(info["start"])])
                    elif info["type"] == "Float32":
                        self.fmu.setFloat32([self.vrs[var_name]], [float(info["start"])])
                    elif info["type"] == "Float64":
                        self.fmu.setFloat64([self.vrs[var_name]], [float(info["start"])])
                    elif info["type"] == "Boolean":
                        self.fmu.setBoolean([self.vrs[var_name]], [bool(info["start"])])
                    else:
                        raise ValueError(f"Unsupported variable type: {info['type']}")

            self.fmu.exitInitializationMode()
            return True
        except Exception as e:
            raise Exception(f"Error initializing FMU: {e}")

    def set_variable(self, name: str, value: Any) -> None:
        try:
            var_type = self.variable_info[name]["type"]
            if var_type == "Boolean":
                self.fmu.setBoolean([self.vrs[name]], [bool(value)])
            elif var_type == "UInt8":
                self.fmu.setUInt8([self.vrs[name]], [int(value)])
            elif var_type == "UInt16":
                self.fmu.setUInt16([self.vrs[name]], [int(value)])
            elif var_type == "UInt32":
                self.fmu.setUInt32([self.vrs[name]], [int(value)])
            elif var_type == "UInt64":
                self.fmu.setUInt64([self.vrs[name]], [int(value)])
            elif var_type == "Int8":
                self.fmu.setInt8([self.vrs[name]], [int(value)])
            elif var_type == "Int16":
                self.fmu.setInt16([self.vrs[name]], [int(value)])
            elif var_type == "Int32":
                self.fmu.setInt32([self.vrs[name]], [int(value)])
            elif var_type == "Int64":
                self.fmu.setInt64([self.vrs[name]], [int(value)])
            elif var_type == "Float32":
                self.fmu.setFloat32([self.vrs[name]], [float(value)])
            elif var_type == "Float64":
                self.fmu.setFloat64([self.vrs[name]], [float(value)])
            else:
                raise ValueError(f"Unsupported variable type: {var_type}")
        except Exception as e:
            raise Exception(f"Error setting variable {name}: {e}")

    def get_variable(self, name: str) -> Any:
        try:
            var_type = self.variable_info[name]["type"]
            if var_type == "Boolean":
                return self.fmu.getBoolean([self.vrs[name]])[0]
            elif var_type == "UInt8":
                return self.fmu.getUInt8([self.vrs[name]])[0]
            elif var_type == "UInt16":
                return self.fmu.getUInt16([self.vrs[name]])[0]
            elif var_type == "UInt32":
                return self.fmu.getUInt32([self.vrs[name]])[0]
            elif var_type == "UInt64":
                return self.fmu.getUInt64([self.vrs[name]])[0]
            elif var_type == "Int8":
                return self.fmu.getInt8([self.vrs[name]])[0]
            elif var_type == "Int16":
                return self.fmu.getInt16([self.vrs[name]])[0]
            elif var_type == "Int32":
                return self.fmu.getInt32([self.vrs[name]])[0]
            elif var_type == "Int64":
                return self.fmu.getInt64([self.vrs[name]])[0]
            elif var_type == "Float32":
                return self.fmu.getFloat32([self.vrs[name]])[0]
            elif var_type == "Float64":
                return self.fmu.getFloat64([self.vrs[name]])[0]
            else:
                raise ValueError(f"Unsupported variable type: {var_type}")
            # Add other types as needed
        except Exception as e:
            raise Exception(f"Error getting variable {name}: {e}")

    def set_input_schedule(
        self, variable_name: str, schedule: Dict[float, Any]
    ) -> None:
        """
        Set a schedule of values for an input variable.
        Args:
            variable_name: Name of the input variable
            schedule: Dictionary mapping time points to values
        """
        if variable_name not in self.variable_info:
            raise ValueError(f"Variable {variable_name} not found in model")
        if self.variable_info[variable_name]["causality"] != "input":
            raise ValueError(f"Variable {variable_name} is not an input variable")

        if 0.0 not in schedule:
            schedule[0.0] = self.variable_info[variable_name]["start"]
        self.input_schedules[variable_name] = schedule

    def register_interrupt(
        self, name: str, condition: Dict[str, Any], handler: Optional[str] = None
    ) -> None:
        """
        Register an interrupt condition and its handler.
        
        Args:
            name: Name of the interrupt
            condition: Dictionary containing condition details (variable name and expected value)
            handler: Name of the handler function (ISR) to call when interrupt is triggered
        """
        self.interrupt_conditions[name] = condition
        if handler:
            self.interrupt_handlers[name] = handler

    def check_interrupts(self) -> List[str]:
        """
        Check if any registered interrupts are triggered.
        
        Returns:
            List[str]: List of triggered interrupt names
        """
        triggered: List[str] = []
        
        # Initialize previous values dict if it doesn't exist
        if not hasattr(self, 'prev_values'):
            self.prev_values: Dict[str, Any] = {}
        
        for int_name, condition in self.interrupt_conditions.items():
            var_name: str = int_name  # By default, interrupt name is the variable name
            expected_value: Any = condition.get("value")
            # If the variable exists in the model
            if var_name in self.variable_info:
                current_value: Any = self.get_variable(name=var_name)
                
                # Initialize previous value if not already present
                if var_name not in self.prev_values:
                    self.prev_values[var_name] = current_value
                
                # Handle edge detection
                if expected_value == "posedge":
                    # Positive edge detection (transition from 0 to 1)
                    if self.prev_values[var_name] == 0 and current_value == 1:
                        triggered.append(int_name)
                elif expected_value == "negedge":
                    # Negative edge detection (transition from 1 to 0)
                    if self.prev_values[var_name] == 1 and current_value == 0:
                        triggered.append(int_name)
                # Handle regular value comparison
                elif current_value == expected_value:
                    triggered.append(int_name)
                
                # Update previous value for next comparison
                self.prev_values[var_name] = current_value
                    
        return triggered
    
    def run_simulation(self):
        time = self.start_time
        csv_data = ["Time," + ",".join(self.input_schedules.keys()) + "," + 
                    ",".join([var_name for var_name, info in self.variable_info.items() 
                             if info["causality"] == "output"])]

        # Print header
        print("\n=== Starting Simulation ===")
        print("Time step size:", self.step_size)
        print("Stop time:", self.stop_time)
        print("=============================\n")

        while time < self.stop_time:
            current_time = time
            row_values = [f"{current_time}"]

            # Print time step header
            print(f"\n=== Time: {current_time} ===")

            # Set and display inputs based on schedules
            print("Inputs:")
            for var_name, schedule in self.input_schedules.items():
                applicable_times = [t for t in schedule.keys() if t <= current_time]
                value = None
                if applicable_times:
                    latest_time = max(applicable_times)
                    value = schedule[latest_time]
                    self.set_variable(var_name, value)
                    print(f"  {var_name}: {value}")
                row_values.append(str(value) if value is not None else "")

            # Get and display outputs
            print("Outputs:")
            for var_name, info in self.variable_info.items():
                if info["causality"] == "output":
                    value = self.get_variable(var_name)
                    print(f"  {var_name}: {value}")
                    row_values.append(str(value))

            # Add row to CSV data
            csv_data.append(",".join(row_values))

            time += self.step_size
            
            # Check for interrupts after the step
            triggered_interrupts = self.check_interrupts()
            if triggered_interrupts:
                for interrupt in triggered_interrupts:
                    handler = self.interrupt_handlers.get(interrupt)
                    if handler:
                        handler()

            # Perform simulation step
            self.fmu.doStep(
                currentCommunicationPoint=current_time,
                communicationStepSize=self.step_size,
            )



        print("\n=== Simulation Complete ===")
        self.fmu.terminate()
        self.fmu.freeInstance()
        
        # Return CSV-like data as a string
        return "\n".join(csv_data)
