"""Setup configuration for NGO Campaign Assistant."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    requirements = [
        line.strip() 
        for line in requirements_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
else:
    requirements = []

setup(
    name="ngo-campaign-assistant",
    version="1.0.0",
    author="NGO Assistant Team",
    author_email="contact@ngo-assistant.com",
    description="CLI-based conversational agent for NGO campaign and donation management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/ngo-campaign-assistant",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Email",
        "Topic :: Office/Business :: Groupware",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ngo-assistant=ngo_assistant.main:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "ngo_assistant": ["data/*"],
    },
)