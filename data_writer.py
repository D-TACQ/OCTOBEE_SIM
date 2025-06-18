"""
Writing out multiplexed data of the format:

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
"""
import ast
import numpy as np

# use a numpy structured array to define data and write it out???
n_sensors = 8
channel_def_strings = ""
for n in range(1, n_sensors + 1):
    channel_def_strings += (
        f"('S{n}X','<i2'), ('S{n}Y','<i2'), ('S{n}Z','<i2'), ('S{n}T','<i2'),"
    )

final_strings = ["XPOS", "YPOS", "ZPOS", "CNT", "USEC", "USR1", "USR2", "USR3"]

for n in final_strings:
    channel_def_strings += f" ('{n}','<i4'),"

channel_def = ast.literal_eval(f"[{channel_def_strings}]")

data = np.zeros(16, dtype=channel_def)


def to_file(data, filename):
    data.tofile(filename)


if __name__ == "__main__":

    print(channel_def_strings)
    print(channel_def)
    print(data)
