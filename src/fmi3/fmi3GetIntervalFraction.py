from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3GetIntervalFraction(BaseFMI3Module):
    def __init__(self):
        template = """
    fmi3Status fmi3GetIntervalFraction(     fmi3Instance instance,
                                            const fmi3ValueReference valueReferences[],
                                            size_t nValueReferences,
                                            fmi3UInt64 intervalCounters[],
                                            fmi3UInt64 resolutions[],
                                            fmi3IntervalQualifier qualifiers[]) 
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
            "valueReferences",
            "nValueReferences",
            "intervalCounters",
            "resolutions",
            "qualifiers",
        ]

        unused_macros = self.generate_unused_macros(unsed_params)

        self.template = self.template.format(unused_macros=unused_macros)

        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3GetIntervalFraction()
    print(generator.generate())
