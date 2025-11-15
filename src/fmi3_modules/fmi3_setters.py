from fmi3.base_fmi3_setter import BaseFMI3Setter
from fmi3.fmi3SetBinary import fmi3SetBinary
from fmi3.fmi3SetBoolean import fmi3SetBoolean
from fmi3.fmi3SetClock import fmi3SetClock
from fmi3.fmi3SetContinuousStates import fmi3SetContinuousStates
from fmi3.fmi3SetDebugLogging import fmi3SetDebugLogging
from fmi3.fmi3SetFloat32 import fmi3SetFloat32
from fmi3.fmi3SetFloat64 import fmi3SetFloat64
from fmi3.fmi3SetInt16 import fmi3SetInt16
from fmi3.fmi3SetInt32 import fmi3SetInt32
from fmi3.fmi3SetInt64 import fmi3SetInt64
from fmi3.fmi3SetInt8 import fmi3SetInt8
from fmi3.fmi3SetIntervalDecimal import fmi3SetIntervalDecimal
from fmi3.fmi3SetIntervalFraction import fmi3SetIntervalFraction
from fmi3.fmi3SetShiftDecimal import fmi3SetShiftDecimal
from fmi3.fmi3SetShiftFraction import fmi3SetShiftFraction
from fmi3.fmi3SetString import fmi3SetString
from fmi3.fmi3SetTime import fmi3SetTime
from fmi3.fmi3SetUInt16 import fmi3SetUInt16
from fmi3.fmi3SetUInt32 import fmi3SetUInt32
from fmi3.fmi3SetUInt64 import fmi3SetUInt64
from fmi3.fmi3SetUInt8 import fmi3SetUInt8
from fmi3.fmi3SetFMUState import fmi3SetFMUState
from typing import List

setter_modules: List[BaseFMI3Setter] = [
    fmi3SetBinary(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetBoolean(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetClock(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetContinuousStates(),
    fmi3SetDebugLogging(),
    fmi3SetFloat32(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetFloat64(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetInt16(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetInt32(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetInt64(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetInt8(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetIntervalDecimal(),
    fmi3SetIntervalFraction(),
    fmi3SetShiftDecimal(),
    fmi3SetShiftFraction(),
    fmi3SetString(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetTime(),
    fmi3SetUInt16(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetUInt32(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetUInt64(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetUInt8(struct_file_path="include/struct.h", xml_file_path="modelDescription.xml"),
    fmi3SetFMUState(),
]
