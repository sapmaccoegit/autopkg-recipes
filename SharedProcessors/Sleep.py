#!/usr/local/autopkg/python
#
# (c) Copyright 2022 SAP SE and AutoPkg contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for Sleep class"""

import time

from autopkglib import Processor, ProcessorError

__all__ = ["Sleep"]


class Sleep(Processor):
    """This processor inserts a delay of a specified number of seconds. You probably do not want to do this."""

    description = __doc__
    input_variables = {
        "sleep_seconds": {
            "required": False,
            "description": (
                "Earth-normal seconds specified as zero or a positive number. The processor will sleep for the specified number of seconds. Defaults to 0."
            ),
            "default": "0",
        },
    }
    output_variables = {
    }


    def sleep(self, seconds):
        """Sleep for the specified number of seconds."""
        time.sleep(seconds)
        return True


    def main(self):
        """Perform the main function, which is to sleep."""
        if "sleep_seconds" not in self.env:
            # The default is 0
            self.sleep_seconds = 0
        else:
            # If something else was specified, use that instead
            self.sleep_seconds = self.env.get("sleep_seconds")

        if (not self.sleep_seconds):
            # Nothing was specified, even though there is a default
            raise ProcessorError("Number of seconds not specified. Which is weird because there is a default value.")
        elif (not self.sleep_seconds.isnumeric()):
            # Whatever was specified, it wasn't numeric enough
            raise ProcessorError("Specified value was not a number that can be used for sleep. Please specify a number of seconds greater than or equal to 0. Or don't specify anything, since there is a default value.")

        try:
            # The input for the "sleep" function must be an integer
            self.sleep_seconds_int = int(self.sleep_seconds)

            # Pluralize all the things when printing output
            if self.sleep_seconds_int == 1:
                self.output_phrase = f"{self.sleep_seconds} second"
            else:
                self.output_phrase = f"{self.sleep_seconds} seconds"

            # Actually try to sleep
            self.sleep(self.sleep_seconds_int)
            if self.sleep_seconds_int > 0:
                self.output(f"The computer thinks it has slept for {self.output_phrase}. Who are we to argue, really?")
            else:
                self.output(f"The computer didn't sleep, because {self.output_phrase} were specified. Why even run this processor?")
        except:
            raise ProcessorError(f"Something went wrong while trying to sleep for {self.sleep_seconds} seconds. One would think this was easy, but perhaps it's noisy or the temperature isn't right or there's just a lot on the computer's mind.")


if __name__ == "__main__":
    PROCESSOR = Sleep()
    PROCESSOR.execute_shell()