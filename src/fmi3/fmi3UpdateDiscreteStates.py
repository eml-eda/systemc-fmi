from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3UpdateDiscreteStates(BaseFMI3Module):
    def __init__(self):
        template = """
    fmi3Status fmi3UpdateDiscreteStates(fmi3Instance instance,
                                        fmi3Boolean* discreteStatesNeedUpdate,
                                        fmi3Boolean* terminateSimulation,
                                        fmi3Boolean* nominalsOfContinuousStatesChanged,
                                        fmi3Boolean* valuesOfContinuousStatesChanged,
                                        fmi3Boolean* nextEventTimeDefined,
                                        fmi3Float64* nextEventTime)
    {
        return fmi3OK;
    }
        """
        super().__init__(template)

    def generate(self, config: dict):
        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3UpdateDiscreteStates()
    print(generator.generate())
