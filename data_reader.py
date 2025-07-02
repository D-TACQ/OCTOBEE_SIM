"""Reading in multiplexed data of the format:

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

uses a numpy structured array to define data and reads in
"""

from data_writer import n_sensors_dtype_generator
import numpy as np
from config import SYSTEM_PARAMETERS


def raw_binary_file_to_array(filename, structured_array_dtype):
    """Read binary file into numpy array defined by the dtype string.

    Args:
        filename (str): File to be read
        structured_array_dtype (str): Definition of data to be read

    Returns:
        np.ndarray: Array of data
    """
    return np.fromfile(filename, dtype=structured_array_dtype)


if __name__ == "__main__":
    n_sensors = SYSTEM_PARAMETERS["sensor_count"]
    generated_dtype = n_sensors_dtype_generator(n_sensors)
    generated_dtype_no_position = n_sensors_dtype_generator(
        n_sensors, position_included=False
    )
    print(generated_dtype)
    print(generated_dtype_no_position)
    data_w_position = raw_binary_file_to_array(
        "data/with_position_binary_data.bin", generated_dtype
    )
    data_no_position = raw_binary_file_to_array(
        "data/no_position_binary_data.bin", generated_dtype_no_position
    )
    print(data_w_position.shape)

    print("access each field in structured array with data['field name']")
    print("Accessing the USEC values in the results array")
    print(data_w_position["USEC"])
    print(data_no_position["USEC"])
