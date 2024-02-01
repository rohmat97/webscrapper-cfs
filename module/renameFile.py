import shutil
import os

def copy_and_rename_xlsx(src_path, dest_path, new_filename):
    try:
        # Copy the file
        shutil.copy(src_path, dest_path)

        # Build the new file path with the new filename
        new_file_path = os.path.join(dest_path, new_filename)

        # Rename the copied file
        os.rename(os.path.join(dest_path, os.path.basename(src_path)), new_file_path)

        print(f"File copied and renamed successfully: {new_file_path}")

        os.remove(src_path)
    except Exception as e:
        print(f"Error: {e}")