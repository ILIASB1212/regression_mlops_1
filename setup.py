from setuptools import setup, find_packages

def get_requirements( ) :
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()
    

setup(
    name="my-mlops-project",
    version="0.1.0",
    author="Your Name",
    packages=find_packages(),
    install_requires=get_requirements(),
)