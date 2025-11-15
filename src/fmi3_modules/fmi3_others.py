from fmi3.base_fmi3_module import BaseFMI3Module
from fmi3.fmi3ActivateModelPartition import fmi3ActivateModelPartition
from fmi3.fmi3CompletedIntegratorStep import fmi3CompletedIntegratorStep
from fmi3.fmi3DeserializeFMUState import fmi3DeserializeFMUState
from fmi3.fmi3DoStep import fmi3DoStep
from fmi3.fmi3EnterConfigurationMode import fmi3EnterConfigurationMode
from fmi3.fmi3EnterContinuousTimeMode import fmi3EnterContinuousTimeMode
from fmi3.fmi3EnterEventMode import fmi3EnterEventMode
from fmi3.fmi3EnterInitializationMode import fmi3EnterInitializationMode
from fmi3.fmi3EnterStepMode import fmi3EnterStepMode
from fmi3.fmi3EvaluateDiscreteStates import fmi3EvaluateDiscreteStates
from fmi3.fmi3ExitConfigurationMode import fmi3ExitConfigurationMode
from fmi3.fmi3ExitInitializationMode import fmi3ExitInitializationMode
from fmi3.fmi3FreeInstance import fmi3FreeInstance
from fmi3.fmi3FreeFMUState import fmi3FreeFMUState
from fmi3.fmi3InstantiateCoSimulation import fmi3InstantiateCoSimulation
from fmi3.fmi3InstantiateModelExchange import fmi3InstantiateModelExchange
from fmi3.fmi3InstantiateScheduledExecution import fmi3InstantiateScheduledExecution
from fmi3.fmi3Reset import fmi3Reset
from fmi3.fmi3SerializeFMUState import fmi3SerializeFMUState
from fmi3.fmi3SerializedFMUStateSize import fmi3SerializedFMUStateSize
from fmi3.fmi3Terminate import fmi3Terminate
from fmi3.fmi3UpdateDiscreteStates import fmi3UpdateDiscreteStates
from fmi3.fmi3_main import fmi3Main
from typing import List

other_modules: List[BaseFMI3Module] = [
    fmi3ActivateModelPartition(),
    fmi3CompletedIntegratorStep(),
    fmi3DeserializeFMUState(),
    fmi3DoStep(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3EnterConfigurationMode(),
    fmi3EnterContinuousTimeMode(),
    fmi3EnterEventMode(),
    fmi3EnterInitializationMode(),
    fmi3EnterStepMode(),
    fmi3EvaluateDiscreteStates(),
    fmi3ExitConfigurationMode(),
    fmi3ExitInitializationMode(),
    fmi3FreeInstance(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3FreeFMUState(),
    fmi3InstantiateCoSimulation(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3InstantiateModelExchange(),
    fmi3InstantiateScheduledExecution(),
    fmi3Reset(),
    fmi3SerializeFMUState(),
    fmi3SerializedFMUStateSize(),
    fmi3Terminate(),
    fmi3UpdateDiscreteStates(),
    fmi3Main(),
]
