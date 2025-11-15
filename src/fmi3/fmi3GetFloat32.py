from fmi3.base_fmi3_getter import BaseFMI3Getter


class fmi3GetFloat32(BaseFMI3Getter):
    def __init__(self, struct_file_path=None, xml_file_path=None):
        super().__init__(
            var_type="Float32",
            struct_file_path=struct_file_path,
            xml_file_path=xml_file_path,
        )


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3GetFloat32(
        struct_file_path="prova_struct.h", xml_file_path="modelDescription.xml"
    )
    print(generator.generate())
