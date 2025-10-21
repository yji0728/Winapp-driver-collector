"""
Setup script for WinAppDriver Automation Framework
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="winappdriver-automation",
    version="1.0.0",
    author="WinAppDriver Automation Team",
    description="Automation framework for Windows applications using Microsoft WinAppDriver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yji0728/Winapp-driver-collector",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Appium-Python-Client>=2.9.0",
        "selenium>=4.0.0",
        "click>=8.0.0",
        "PyYAML>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "winapp-cli=cli.main:cli",
            "winapp-gui=gui.main:main",
        ],
    },
)
