from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3EnterInitializationMode(BaseFMI3Module):
    def __init__(self):
        template = """
    fmi3Status fmi3EnterInitializationMode( fmi3Instance instance,
                                            fmi3Boolean toleranceDefined,
                                            fmi3Float64 tolerance,
                                            fmi3Float64 startTime,
                                            fmi3Boolean stopTimeDefined,
                                            fmi3Float64 stopTime)
    {   
        return fmi3OK;
    }
        """
        super().__init__(template)

    def generate(self, config: dict):
        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3EnterInitializationMode()
    print(generator.generate())
