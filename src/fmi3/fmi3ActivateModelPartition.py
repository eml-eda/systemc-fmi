from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3ActivateModelPartition(BaseFMI3Module):
    def __init__(self):
        template = """fmi3Status fmi3ActivateModelPartition(fmi3Instance instance,
                                      fmi3ValueReference clockReference,
                                      fmi3Float64 activationTime) {
    return fmi3OK;
}
"""
        super().__init__(template)

    def generate(self, config: dict):
        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3ActivateModelPartition()
    print(generator.generate())
