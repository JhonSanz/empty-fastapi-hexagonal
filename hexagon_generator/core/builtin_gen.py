import shutil
import os


class BuiltInGenerator:
    def copy_builtin_apps(self, *, path_source: str, path_target: str):
        source_dir_full = f"hexagon_generator/builtin_apps/{path_source}"
        destination_dir = f"{path_target}"

        if os.path.exists(destination_dir):
            print(f"Directorio {destination_dir} ya existe.")
            return

        try:
            shutil.copytree(source_dir_full, destination_dir)
            print(f"Directorio copiado de {source_dir_full} a {destination_dir}")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def copy_builtin_files(self, *, path_source: str, path_target: str):
        source_dir_full = f"hexagon_generator/builtin_apps/{path_source}"
        destination_dir = f"{path_target}"

        if os.path.exists(destination_dir):
            print(f"Archivo {destination_dir} ya existe.")
            return

        try:
            shutil.copyfile(source_dir_full, destination_dir)
            print(f"Archivo copiado de {source_dir_full} a {destination_dir}")
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            return
