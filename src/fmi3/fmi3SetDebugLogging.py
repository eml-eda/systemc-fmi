import subprocess
import tempfile
from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3SetDebugLogging(BaseFMI3Module):
    def __init__(self):
        template = """fmi3Status fmi3SetDebugLogging(  fmi3Instance instance,
                                                            fmi3Boolean loggingOn,
                                                            size_t nCategories,
                                                            const fmi3String categories[])
    {
        return fmi3OK;
    }"""
        super().__init__(template)

    def generate(self, config: dict):
        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3SetDebugLogging()
    print(generator.generate())
