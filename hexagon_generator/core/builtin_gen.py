import shutil
import os


class BuiltInGenerator:
    def copy_builtin_apps(self, *, path_source: str, path_target: str):
        source_dir_full = f"hexagon_generator/builtin_apps/{path_source}"
        destination_dir = f"{path_target}"

        if os.path.exists(destination_dir):
            print(f"Dir {destination_dir} already exists.")
            return

        try:
            shutil.copytree(source_dir_full, destination_dir)
            print(f"Dir copied from {source_dir_full} to {destination_dir}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def copy_builtin_files(self, *, path_source: str, path_target: str):
        source_dir_full = f"hexagon_generator/builtin_apps/{path_source}"
        destination_dir = f"{path_target}"

        if os.path.exists(destination_dir):
            print(f"File {destination_dir} already exists.")
            return

        try:
            shutil.copyfile(source_dir_full, destination_dir)
            print(f"File copied from {source_dir_full} to {destination_dir}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            return
