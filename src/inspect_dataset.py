import h5py

file_path = input("Enter H5 file path: ")

with h5py.File(file_path, "r") as file:

    print("\nDataset Keys:")
    print(list(file.keys()))

    for key in file.keys():
        data = file[key]

        print("\n-----------------------------")
        print("Key:", key)
        print("Shape:", data.shape)
        print("Data Type:", data.dtype)
        print("-----------------------------")