"""Writing out multiplexed data of the format:

| BYTE | 00 | 02 | 04 | 06 | 08 | 10 | .. | 60 | 62 | 64 | 68 | 72 | 76  | 80  | 84  | 88  | 92  |
|------|----|----|----|----|----|----|----|----|----|----|----|----|-----|-----|-----|-----|-----|
| AI   |CH01|CH02|CH03|CH04|CH05|CH06| .. |CH31|CH32|AQB1|AQB2|AQB3|SPAD0|SPAD1|SPAD2|SPAD3|SPAD4|
| FUNC |S1X |S1Y |S1Z |S1T |S2X |S2Y | .. |S8Z |S8T |XPOS|YPOS|ZPOS| CNT |USEC |USR1 |USR2 |USR3 |
"""

"""
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


def n_sensors_dtype_generator(n_sensors):
    """
    'S{n}X', S{n}Y', 'S{n}Z', 'S{n}T', "XPOS", "YPOS", "ZPOS", "CNT", "USEC", "USR1", "USR2", "USR3"
    """
    if n_sensors < 1:
        raise ValueError("n_sensors must be integer > 0")
    channel_def_strings = ""
    for n in range(1, n_sensors + 1):
        channel_def_strings += (
            f"('S{n}X','<i2'), ('S{n}Y','<i2'), ('S{n}Z','<i2'), ('S{n}T','<i2'),"
        )

    final_strings = ["XPOS", "YPOS", "ZPOS", "CNT", "USEC", "USR1", "USR2", "USR3"]

    for n in final_strings:
        channel_def_strings += f" ('{n}','<i4'),"

    channel_def = ast.literal_eval(f"[{channel_def_strings}]")
    return channel_def


def array_to_file(data, filename):
    np.save(filename, data)


def array_to_raw_binary_file(data, filename):
    data.tofile(filename)


if __name__ == "__main__":
    n_sensors = 8
    generated_dtype = n_sensors_dtype_generator(n_sensors)
    print(generated_dtype)
    # Generating a dataset of zeros (but of the correct dtype)
    data = np.zeros(n_sensors, dtype=generated_dtype)
    print(data)

    print("Accessing the USEC values in the results array")
    print(data["USEC"])
