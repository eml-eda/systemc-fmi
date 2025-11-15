from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3GetOutputDerivatives(BaseFMI3Module):
    def __init__(self):
        template = """
        fmi3Status fmi3GetOutputDerivatives(    fmi3Instance instance,
                                            const fmi3ValueReference valueReferences[],
                                            size_t nValueReferences,
                                            const fmi3Int32 orders[],
                                            fmi3Float64 values[],
                                            size_t nValues) 
        {   
            return fmi3OK;
        }
        """
        super().__init__(template)

    def generate(self, config: dict):
        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3GetOutputDerivatives()
    print(generator.generate())
