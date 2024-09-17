from setuptools import find_packages, setup
from typing import List

def get_packages(file_path: str) -> List[str]:
    """
    ### Retrieve all package dependencies from a requirements.txt file.

    Args:
        file_path (str): Path to the requirements.txt file.

    Returns:
        List[str]: A list of package names without version specifiers or "-e .".
    """
    with open(file_path, "r") as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("-e .")]
        return requirements

setup(
    name="Crop Yield Prediction Project",
    version="0.1.1",
    author="Taofeek Opeyemi Olawoye",
    author_email="habephe21@gmail.com",
    packages=find_packages(),
    install_requires=get_packages('requirements.txt')
)