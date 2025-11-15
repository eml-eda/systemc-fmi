from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3GetVariableDependencies(BaseFMI3Module):
    def __init__(self):
        template = """
    fmi3Status fmi3GetVariableDependencies(             fmi3Instance instance,
                                                        fmi3ValueReference dependent,
                                                        size_t elementIndicesOfDependent[],
                                                        fmi3ValueReference independents[],
                                                        size_t elementIndicesOfIndependents[],
                                                        fmi3DependencyKind dependencyKinds[],
                                                        size_t nDependencies) 
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
            "dependent",
            "elementIndicesOfDependent",
            "independents",
            "elementIndicesOfIndependents",
            "dependencyKinds",
            "nDependencies",
        ]

        unused_macros = self.generate_unused_macros(unsed_params)

        self.template = self.template.format(unused_macros=unused_macros)

        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3GetVariableDependencies()
    print(generator.generate())
