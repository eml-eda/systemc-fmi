from fmi3.base_fmi3_getter import BaseFMI3Getter
from fmi3.fmi3GetAdjointDerivative import fmi3GetAdjointDerivative
from fmi3.fmi3GetBinary import fmi3GetBinary
from fmi3.fmi3GetBoolean import fmi3GetBoolean
from fmi3.fmi3GetClock import fmi3GetClock
from fmi3.fmi3GetContinuousStateDerivatives import fmi3GetContinuousStateDerivatives
from fmi3.fmi3GetContinuousStates import fmi3GetContinuousStates
from fmi3.fmi3GetDirectionalDerivative import fmi3GetDirectionalDerivative
from fmi3.fmi3GetEventIndicators import fmi3GetEventIndicators
from fmi3.fmi3GetFloat32 import fmi3GetFloat32
from fmi3.fmi3GetFloat64 import fmi3GetFloat64
from fmi3.fmi3GetFMUState import fmi3GetFMUState
from fmi3.fmi3GetInt16 import fmi3GetInt16
from fmi3.fmi3GetInt32 import fmi3GetInt32
from fmi3.fmi3GetInt64 import fmi3GetInt64
from fmi3.fmi3GetInt8 import fmi3GetInt8
from fmi3.fmi3GetIntervalDecimal import fmi3GetIntervalDecimal
from fmi3.fmi3GetIntervalFraction import fmi3GetIntervalFraction
from fmi3.fmi3GetNominalsOfContinuousStates import fmi3GetNominalsOfContinuousStates
from fmi3.fmi3GetNumberOfContinuousStates import fmi3GetNumberOfContinuousStates
from fmi3.fmi3GetNumberOfEventIndicators import fmi3GetNumberOfEventIndicators
from fmi3.fmi3GetNumberOfVariableDependencies import fmi3GetNumberOfVariableDependencies
from fmi3.fmi3GetOutputDerivatives import fmi3GetOutputDerivatives
from fmi3.fmi3GetShiftDecimal import fmi3GetShiftDecimal
from fmi3.fmi3GetShiftFraction import fmi3GetShiftFraction
from fmi3.fmi3GetString import fmi3GetString
from fmi3.fmi3GetUInt16 import fmi3GetUInt16
from fmi3.fmi3GetUInt32 import fmi3GetUInt32
from fmi3.fmi3GetUInt64 import fmi3GetUInt64
from fmi3.fmi3GetUInt8 import fmi3GetUInt8
from fmi3.fmi3GetVariableDependencies import fmi3GetVariableDependencies
from fmi3.fmi3GetVersion import fmi3GetVersion
from typing import List

getters_modules: List[BaseFMI3Getter] = [
    fmi3GetAdjointDerivative(),
    fmi3GetBinary(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetBoolean(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetClock(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetContinuousStateDerivatives(),
    fmi3GetContinuousStates(),
    fmi3GetDirectionalDerivative(),
    fmi3GetEventIndicators(),
    fmi3GetFloat32(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetFloat64(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetFMUState(),
    fmi3GetInt16(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetInt32(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetInt64(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetInt8(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetIntervalDecimal(),
    fmi3GetIntervalFraction(),
    fmi3GetNominalsOfContinuousStates(),
    fmi3GetNumberOfContinuousStates(),
    fmi3GetNumberOfEventIndicators(),
    fmi3GetNumberOfVariableDependencies(),
    fmi3GetOutputDerivatives(),
    fmi3GetShiftDecimal(),
    fmi3GetShiftFraction(),
    fmi3GetString(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetUInt16(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetUInt32(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetUInt64(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetUInt8(
        struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"
    ),
    fmi3GetVariableDependencies(),
    fmi3GetVersion(),
]
