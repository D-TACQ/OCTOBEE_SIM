"""
Writes simulation data to a file format that matches the ACQ400 data format.

Simulation data is scaled here to use the full dynamic range available to 
the AI module selected.
"""

import numpy as np
from config import FILES, SAMPLING, SCAN_SETUP, SYSTEM_PARAMETERS
import data_writer


def calculate_n_samples(n_yscans, n_xscans=0, n_zscans=0, sample_rate=10000):
    XSCAN_TIME = SCAN_SETUP["durations_s"]["x_scan"]
    YSCAN_TIME = SCAN_SETUP["durations_s"]["y_scan"]
    ZSCAN_TIME = SCAN_SETUP["durations_s"]["z_scan"]

    n_samples = sample_rate * (
        XSCAN_TIME * n_xscans + YSCAN_TIME * n_yscans + ZSCAN_TIME * n_zscans
    )
    return int(n_samples)


def n_samples_to_elapsed_usec(sample_rate, n_samples):
    seconds = n_samples / sample_rate
    useconds = seconds * 1e6
    return useconds


def find_optimum_gain(arr):
    """Finds optimum gain for array data by using maximum value of array
    and dynamic range of selected ADC"""
    dynamic_range_bits = SAMPLING['dynamic_range_bits']
    m = arr.max()
    n = arr.min()
    dynamic_range = 2**dynamic_range_bits
    pos_range = dynamic_range // 2
    neg_range = -1 * dynamic_range // 2
    gain1 = pos_range // m
    gain2 = neg_range // n
    if gain1 > gain2:
        return gain1
    else:
        return gain2

if __name__ == "__main__":
    filename_list = FILES["input_list"]
    N_SENSORS = SYSTEM_PARAMETERS["sensor_count"]
    N_XSCAN = SCAN_SETUP["scan_counts"]["x"]
    N_YSCAN = SCAN_SETUP["scan_counts"]["y"]
    N_ZSCAN = SCAN_SETUP["scan_counts"]["z"]

    generated_dtype = data_writer.n_sensors_dtype_generator(N_SENSORS)
    print(generated_dtype)
    n_samples = calculate_n_samples(n_yscans=N_YSCAN)
    # read in data
    result = np.zeros(n_samples, dtype=generated_dtype)
    print(f"shape of result is {result.shape} and dtype is {result.dtype}")
    inp = input("press any key to continue")
    sensor_number = 1
    for filename in filename_list:
        a = np.load(filename)
        gain = find_optimum_gain(a)
        print(a.shape)
        selection = a[0:n_samples, :]
        print(selection.shape)

        gain0 = find_optimum_gain(selection[:, 0])
        gain1 = find_optimum_gain(selection[:, 1])
        gain2 = find_optimum_gain(selection[:, 2])
        gain3 = find_optimum_gain(selection[:, 0])
        result[f"S{sensor_number}X"] = selection[:, 0] * gain0
        result[f"S{sensor_number}Y"] = selection[:, 1] * gain1
        result[f"S{sensor_number}Z"] = selection[:, 2] * gain2
        result[f"S{sensor_number}T"] = selection[:, 0] * gain3
        sensor_number += 1

    elapsed_usec = n_samples_to_elapsed_usec(10000, n_samples)

    # TODO: populate positions based on encoder ticks
    result["XPOS"] = np.zeros(n_samples)
    result["YPOS"] = np.linspace(
        0, 300, n_samples
    )  # TODO: change this from hardcoded mm
    result["ZPOS"] = np.zeros(n_samples)
    result["CNT"] = np.linspace(0, n_samples, n_samples)
    result["USEC"] = np.linspace(0, elapsed_usec, n_samples)

    # USR value: 3 words of padding to round out the sample to 96 bytes
    # Default values 0x2222,0x3333,0x5555, helpful to check alignment
    # It’s also possible to inject other values here.

    result["USR1"] = np.ones(n_samples) * 0x2222
    result["USR2"] = np.ones(n_samples) * 0x3333
    result["USR3"] = np.ones(n_samples) * 0x5555

    print(result[0])
    print(result[51234])
    print(result[-1])

    # np.save saves as an array format with a header so it can be read back in
    # np.save("binary_data.bin",result)
    result.tofile(FILES["output_muxed_result"])
    # to read this .bin back in you need to provide a dtype so numpy can interpret it
