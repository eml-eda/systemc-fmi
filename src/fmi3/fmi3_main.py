from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3Main(BaseFMI3Module):
    def __init__(self):
        template = """
        #include "systemc"

        using namespace sc_core;
        
        int sc_main(int argc, char *argv[]) {
            sc_set_time_resolution(1,SC_MS);
            return 0;
        }
        """
        super().__init__(template)

    def generate(self, config: dict):
        self.config = config
        return self.format_code(style="LLVM")

    def write_to_file(self, path: str = "src") -> None:
        filename = f"{path}/main.cpp"
        with open(filename, "w") as file:
            file.write(self.generate(config=self.config))
        return filename


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3Main()
    print(generator.generate())
