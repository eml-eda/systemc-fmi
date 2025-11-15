from fmi3.base_fmi3_getter import BaseFMI3Getter


class fmi3GetUInt64(BaseFMI3Getter):
    def __init__(self, struct_file_path=None, xml_file_path=None):
        super().__init__(
            var_type="UInt64",
            struct_file_path=struct_file_path,
            xml_file_path=xml_file_path,
        )


if __name__ == "__main__":
    generator = fmi3GetUInt64(
        struct_file_path="prova_struct.h", xml_file_path="modelDescription.xml"
    )
    print(generator.generate())
