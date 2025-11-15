import subprocess
import tempfile
from fmi3.base_fmi3_module import BaseFMI3Module


class fmi3InstantiateScheduledExecution(BaseFMI3Module):
    def __init__(self):
        template = """fmi3Instance fmi3InstantiateScheduledExecution(  fmi3String                     instanceName,
                                                                            fmi3String                     instantiationToken,
                                                                            fmi3String                     resourcePath,
                                                                            fmi3Boolean                    visible,
                                                                            fmi3Boolean                    loggingOn,
                                                                            fmi3InstanceEnvironment        instanceEnvironment,
                                                                            fmi3LogMessageCallback         logMessage,
                                                                            fmi3ClockUpdateCallback        clockUpdate,
                                                                            fmi3LockPreemptionCallback     lockPreemption,
                                                                            fmi3UnlockPreemptionCallback   unlockPreemption)
    {{
        {unused_macros}

        return NULL;
    }}"""
        super().__init__(template, defines=["UNUSED(x) (void)(x)"])

    def generate(self, config: dict):
        """Generate the complete function implementation"""
        unsed_params = [
            "instanceName",
            "instantiationToken",
            "resourcePath",
            "visible",
            "loggingOn",
            "instanceEnvironment",
            "logMessage",
            "clockUpdate",
            "lockPreemption",
            "unlockPreemption",
        ]

        unused_macros = self.generate_unused_macros(unsed_params)

        self.template = self.template.format(unused_macros=unused_macros)

        return self.format_code(style="LLVM")


if __name__ == "__main__":
    """Test the generator"""
    generator = fmi3InstantiateScheduledExecution()
    print(generator.generate())
