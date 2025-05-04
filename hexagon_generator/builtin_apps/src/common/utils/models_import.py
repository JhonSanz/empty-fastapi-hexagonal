import importlib
import pkgutil
from pathlib import Path


def models_import(base_package: str = "src"):
    """
    Importa dinámicamente todos los módulos `domain.models` desde subdirectorios de `src`.

    Args:
        base_package (str): El nombre del paquete base donde buscar los submódulos.

    Returns:
        dict: Un diccionario con las referencias a los módulos importados.
              Las claves son los nombres de los módulos, y los valores son los módulos importados.
    """
    imported_modules = {}
    base_path = Path(base_package.replace(".", "/"))

    for package in pkgutil.walk_packages([str(base_path)], f"{base_package}."):
        module_name = package.name
        if module_name.endswith(
            ".domain.models"
        ):  # Filtrar solo los módulos `domain.models`
            try:
                module = importlib.import_module(module_name)
                imported_modules[module_name] = module
            except Exception as e:
                print(f"Error al importar el módulo {module_name}: {e}")

    return imported_modules
