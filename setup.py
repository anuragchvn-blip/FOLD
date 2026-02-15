from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="fold",
    version="1.0.0",
    description="Fractal Optimized Layered Data - Convert anything to video and back",
    author="FOLD Team",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fold=fold.cli.main:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)