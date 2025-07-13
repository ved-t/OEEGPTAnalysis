# requirements.py

import subprocess
import importlib

required_packages = {
    "pandas": "pandas",
    "google-generativeai": "google.generativeai",
    "colorama": "colorama",
    "pydantic": "pydantic"
}

for package_name, import_name in required_packages.items():
    try:
        importlib.import_module(import_name)
        print(f"{package_name} is already installed.")
    except ImportError:
        print(f"{package_name} not found. Installing...")
        subprocess.check_call(["pip", "install", package_name])
