import numpy as np
import data_writer

filename_list = [
    "B-field_zoff_0.npy",
    "B-field_zoff_5.npy",
    "B-field_zoff_10.npy",
    "B-field_zoff_15.npy",
    "B-field_zoff_20.npy",
    "B-field_zoff_25.npy",
    "B-field_zoff_30.npy",
    "B-field_zoff_35.npy",
]


def calculate_n_samples(n_yscans, n_xscans=0, n_zscans=0, sample_rate=10000):
    XSCAN_TIME = 7
    YSCAN_TIME = 15
    ZSCAN_TIME = 11

    n_samples = sample_rate * (
        XSCAN_TIME * n_xscans + YSCAN_TIME * n_yscans + ZSCAN_TIME * n_zscans
    )
    return n_samples


def n_samples_to_elapsed_usec(sample_rate, n_samples):
    seconds = n_samples / sample_rate
    useconds = seconds * 1e6
    return useconds


if __name__ == "__main__":
    N_SENSORS = 8
    N_XSCAN = 0
    N_YSCAN = 1
    N_ZSCAN = 0

    generated_dtype = data_writer.n_sensors_dtype_generator(N_SENSORS)
    print(generated_dtype)
    n_samples = calculate_n_samples(n_yscans=1)
    # read in data
    result = np.zeros(n_samples, dtype=generated_dtype)
    print(f"shape of result is {result.shape} and dtype is {result.dtype}")
    inp = input("press any key to continue")
    sensor_number = 1
    for filename in filename_list:
        a = np.load(filename)
        print(a.shape)
        # peel off x entries...
        selection = a[0:n_samples, :]
        print(selection.shape)

        result[f"S{sensor_number}X"] = selection[:, 0]
        result[f"S{sensor_number}Y"] = selection[:, 1]
        result[f"S{sensor_number}Z"] = selection[:, 2]
        result[f"S{sensor_number}T"] = selection[:, 0]
        sensor_number += 1

    elapsed_usec = n_samples_to_elapsed_usec(10000, n_samples)

    result["XPOS"] = np.zeros(150000)
    result["YPOS"] = np.linspace(
        0, 300, n_samples
    )  # TODO: change this from hardcoded mm
    result["ZPOS"] = np.zeros(150000)
    result["CNT"] = np.linspace(0, n_samples, n_samples)
    result["USEC"] = np.linspace(0, elapsed_usec, n_samples)

    # USR value: 3 words of padding to round out the sample to 96 bytes
    # Default values 0x2222,0x3333,0x5555, helpful to check alignment
    # It’s also possible to inject other values here.

    result["USR1"] = np.ones(150000) * 0x2222
    result["USR2"] = np.ones(150000) * 0x3333
    result["USR3"] = np.ones(150000) * 0x5555

    print(result[0])
    print(result[51234])
    print(result[-1])

    # np.save saves as an array format with a header so it can be read back in
    # np.save("binary_data.bin",result)
    result.tofile("binary_data.bin")
# to read this .bin back in you need to provide a dtype so numpy can interpret it
