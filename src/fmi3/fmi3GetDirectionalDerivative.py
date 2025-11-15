from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3GetDirectionalDerivative(BaseFMI3Module):
    def __init__(self):
        template = """
    fmi3Status fmi3GetDirectionalDerivative(    fmi3Instance instance,
                                                const fmi3ValueReference unknowns[],
                                                size_t nUnknowns,
                                                const fmi3ValueReference knowns[],
                                                size_t nKnowns,
                                                const fmi3Float64 seed[],
                                                size_t nSeed,
                                                fmi3Float64 sensitivity[],
                                                size_t nSensitivity) 
    {{

        {unused_macros}

        return fmi3OK;
    }}
"""
        super().__init__(template, defines=["UNUSED(x) (void)(x)"])

    def generate(self, config: dict):
        """Generate the complete function implementation"""
        unsed_params = [
            "instance",
            "unknowns",
            "nUnknowns",
            "knowns",
            "nKnowns",
            "seed",
            "nSeed",
            "sensitivity",
            "nSensitivity",
        ]

        unused_macros = self.generate_unused_macros(unsed_params)

        self.template = self.template.format(unused_macros=unused_macros)

        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3GetDirectionalDerivative()
    print(generator.generate())
