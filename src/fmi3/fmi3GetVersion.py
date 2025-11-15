from fmi3.base_fmi3_module import BaseFMI3Module

class fmi3GetVersion(BaseFMI3Module):
    def __init__(self):
        template = """
const char* fmi3GetVersion(void) {
    return fmi3Version;
}
        """
        super().__init__(template)

    def generate(self, config: dict):
        return self.format_code(style="LLVM")

if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3GetVersion()
    print(generator.generate())
