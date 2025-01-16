import os
import shutil
import random

IMG_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "target")

def split_dataset(folder_a, folder_b, train_size=80, val_size=20, test_size=10):
    # List all files in folder A and B without extensions
    files_a = {os.path.splitext(f)[0]: f for f in os.listdir(folder_a)}
    files_b = {os.path.splitext(f)[0]: f for f in os.listdir(folder_b)}

    # Ensure files in A and B match by name
    common_files = sorted(set(files_a.keys()) & set(files_b.keys()))
    assert train_size + val_size + test_size == len(common_files), "Full target dataset size is not equal to common files size."

    # Shuffle the file names randomly
    random.seed()  # Use system time or a default seed
    random.shuffle(common_files)

    train_files = common_files[:train_size]
    val_files = common_files[train_size:train_size + val_size]
    test_files = common_files[train_size + val_size:]

    # Create subfolders
    for folder in [folder_a, folder_b]:
        for split in ['train', 'val', 'test']:
            os.makedirs(os.path.join(folder, split), exist_ok=True)

    # Move files to respective subfolders
    for split, split_files in zip(['train', 'val', 'test'], [train_files, val_files, test_files]):
        for base_name in split_files:
            if base_name in files_a:
                shutil.move(os.path.join(folder_a, files_a[base_name]), os.path.join(folder_a, split, files_a[base_name]))
            if base_name in files_b:
                shutil.move(os.path.join(folder_b, files_b[base_name]), os.path.join(folder_b, split, files_b[base_name]))

    print("Dataset successfully split into train, val, and test sets.")

# Example usage
folder_a = os.path.join(IMG_FOLDER, 'A')
folder_b = os.path.join(IMG_FOLDER, 'B')
split_dataset(folder_a, folder_b)
