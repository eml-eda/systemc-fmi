from fmi3.base_fmi3_setter import BaseFMI3Setter


class fmi3SetFloat64(BaseFMI3Setter):
    def __init__(self, struct_file_path=None, xml_file_path=None):
        super().__init__(
            var_type="Float64",
            struct_file_path=struct_file_path,
            xml_file_path=xml_file_path,
        )


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3SetFloat64(
        struct_file_path="prova_struct.h", xml_file_path="modelDescription.xml"
    )
    print(generator.generate())
