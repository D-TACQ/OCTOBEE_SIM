"""Writing out multiplexed data of the format:

| BYTE | 00 | 02 | 04 | 06 | 08 | 10 | .. | 60 | 62 | 64 | 68 | 72 | 76  | 80  | 84  | 88  | 92  |
|------|----|----|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|-----|-----|
| AI   |CH01|CH02|CH03|CH04|CH05|CH06| .. |CH31|CH32|AQB1|AQB2|AQB3|SPAD0|SPAD1|SPAD2|SPAD3|SPAD4|
| FUNC |S1X |S1Y |S1Z |S1T |S2X |S2Y | .. |S8Z |S8T |XPOS|YPOS|ZPOS| CNT |USEC |USR1 |USR2 |USR3 |

channel1.values = [1,2,3]

channel8.values = [2,3,4]

current_position = position.now

SPAD0 = sample_count

SPAD1 = usec

SPAD2 = usr1

SPAD3 = usr2

SPAD4 = usr3

uses a numpy structured array to define data and writes it out
"""

import ast
import numpy as np
from config import SYSTEM_PARAMETERS


def n_sensors_dtype_generator(n_sensors, position_included=True):
    """Generates dtype string for writing and reading numpy structured arrays.

    Args:
        n_sensors (int): The number of sensors within the data
        position_included (bool): True if X, Y, Z position fields to be
        included in the data, False otherwise.

    Returns:
        str: a dtype definition of binary data format

    """
    if n_sensors < 1:
        raise ValueError("n_sensors must be integer > 0")
    channel_def_strings = ""
    for n in range(1, n_sensors + 1):
        channel_def_strings += (
            f"('S{n}X','<i2'), ('S{n}Y','<i2'), ('S{n}Z','<i2'), ('S{n}T','<i2'),"
        )
    if position_included:
        final_strings = ["XPOS", "YPOS", "ZPOS", "CNT", "USEC", "USR1", "USR2", "USR3"]
    else:
        final_strings = ["CNT", "USEC", "USR1", "USR2", "USR3"]

    for n in final_strings:
        channel_def_strings += f" ('{n}','<i4'),"

    channel_def = ast.literal_eval(f"[{channel_def_strings}]")
    return channel_def


def array_to_file(data, filename):
    np.save(filename, data)


def array_to_raw_binary_file(data, filename):
    data.tofile(filename)


if __name__ == "__main__":
    n_sensors = SYSTEM_PARAMETERS["sensor_count"]
    generated_dtype = n_sensors_dtype_generator(n_sensors)
    generated_dtype_no_position = n_sensors_dtype_generator(
        n_sensors, position_included=False
    )
    print(generated_dtype)
    print(generated_dtype_no_position)
    # Generating a dataset of zeros (but of the correct dtype)
    data = np.zeros(n_sensors, dtype=generated_dtype)
    data_no_position = np.zeros(n_sensors, dtype=generated_dtype_no_position)
    print(data.shape)
    print(data_no_position.shape)

    print("Accessing the USEC values in the results array")
    print(data["USEC"])
