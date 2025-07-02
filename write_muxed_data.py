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

    # input validation
    if (n_yscans < n_zscans) or (n_zscans < n_xscans):
        raise ValueError("Check scan counts")

    n_samples = sample_rate * (
        XSCAN_TIME * n_xscans + YSCAN_TIME * n_yscans + ZSCAN_TIME * n_zscans
    )
    return int(n_samples)


def _n_samples_to_elapsed_usec(sample_rate, n_samples):
    seconds = n_samples / sample_rate
    useconds = seconds * 1e6
    return useconds


def _find_optimum_gain(arr):
    """Finds optimum gain for array data by using maximum value of array
    and dynamic range of selected ADC"""
    dynamic_range_bits = SAMPLING["dynamic_range_bits"]
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


def _convert_m_to_ticks(a):
    # plucked this conversion factor out of thin air
    return a * 10000


def create_full_data_array(
    input_files_list, scan_path_filename, n_samples, generated_dtype
):
    """Creates data array ready to be written to binary file format.

    This includes the positions (if selected), sample counts and SPAD values.

    Args:
        input_files_list (list): stuff
        scan_path_filename (str): path
        n_samples (int): number of samples
        generated_dtype (str): numpy dtype defining data format
    """

    scan_path = np.load(scan_path_filename)
    scan_path_selection = scan_path[0:n_samples, :]
    elapsed_usec = _n_samples_to_elapsed_usec(10000, n_samples)
    print(scan_path_selection.shape)

    result = np.zeros(n_samples, dtype=generated_dtype)
    print(f"shape of result is {result.shape} and dtype is {result.dtype}")
    sensor_number = 1
    for filename in input_files_list:
        a = np.load(filename)
        print(a.shape)
        selection = a[0:n_samples, :]
        print(selection.shape)

        gain0 = _find_optimum_gain(selection[:, 0])
        gain1 = _find_optimum_gain(selection[:, 1])
        gain2 = _find_optimum_gain(selection[:, 2])
        gain3 = _find_optimum_gain(selection[:, 0])
        result[f"S{sensor_number}X"] = selection[:, 0] * gain0
        result[f"S{sensor_number}Y"] = selection[:, 1] * gain1
        result[f"S{sensor_number}Z"] = selection[:, 2] * gain2
        result[f"S{sensor_number}T"] = selection[:, 0] * gain3
        sensor_number += 1

    # Check if all required fields exist in the result array's dtype
    if all(field in result.dtype.names for field in ["XPOS", "YPOS", "ZPOS"]):
        result["XPOS"] = _convert_m_to_ticks(scan_path_selection[:, 0])
        print(scan_path_selection[:, 0])
        print(scan_path_selection[:, 0].shape)

        result["YPOS"] = _convert_m_to_ticks(scan_path_selection[:, 1])
        print(scan_path_selection[:, 1])
        print(scan_path_selection[:, 1].shape)

        result["ZPOS"] = _convert_m_to_ticks(scan_path_selection[:, 2])
        print(scan_path_selection[:, 2])
        print(scan_path_selection[:, 2].shape)

    result["CNT"] = np.linspace(0, n_samples, n_samples)
    result["USEC"] = np.linspace(0, elapsed_usec, n_samples)

    # USR value: 3 words of padding to round out the sample to 96 bytes
    # Default values 0x2222,0x3333,0x5555, helpful to check alignment
    # It’s also possible to inject other values here.

    result["USR1"] = np.ones(n_samples) * 0x2222
    result["USR2"] = np.ones(n_samples) * 0x3333
    result["USR3"] = np.ones(n_samples) * 0x5555
    return result

if __name__ == "__main__":
    filename_list = FILES["input_list"]
    scan_path_filename = FILES["recorded_scan_path"]
    N_SENSORS = SYSTEM_PARAMETERS["sensor_count"]
    N_XSCAN = SCAN_SETUP["scan_counts"]["x"]
    N_YSCAN = SCAN_SETUP["scan_counts"]["y"]
    N_ZSCAN = SCAN_SETUP["scan_counts"]["z"]
    SAMPLE_RATE = SAMPLING["rate_hz"]

    eight_sensors_with_position = data_writer.n_sensors_dtype_generator(N_SENSORS)
    eight_sensors_no_position = data_writer.n_sensors_dtype_generator(
        N_SENSORS, position_included=False
    )
    print(eight_sensors_with_position)
    n_samples = calculate_n_samples(
        n_yscans=N_YSCAN, n_xscans=N_XSCAN, n_zscans=N_ZSCAN, sample_rate=SAMPLE_RATE
    )

    result_with_position = create_full_data_array(
        filename_list, scan_path_filename, n_samples, eight_sensors_with_position
    )
    result_no_position = create_full_data_array(
        filename_list, scan_path_filename, n_samples, eight_sensors_no_position
    )

    print(result_with_position[0])
    print(result_with_position[51234])
    print(result_with_position[-1])

    # np.save saves as an array format with a header so it can be read back in
    # np.save("binary_data.bin",result)
    result_with_position.tofile(FILES["output_dir"] + "/with_position_" + FILES["output_muxed_result"])
    result_no_position.tofile(FILES["output_dir"] + "/no_position_" + FILES["output_muxed_result"])
    # to read this .bin back in you need to provide a dtype so numpy can interpret it
