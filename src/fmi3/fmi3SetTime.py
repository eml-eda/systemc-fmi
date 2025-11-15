from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3SetTime(BaseFMI3Module):
    def __init__(self):
        template = """
    fmi3Status fmi3SetTime(fmi3Instance instance, fmi3Float64 time) 
    {
        return fmi3OK;
    }
        """
        super().__init__(template)

    def generate(self, config: dict):
        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3SetTime()
    print(generator.generate())
