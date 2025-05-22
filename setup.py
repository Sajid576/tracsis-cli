from setuptools import setup, find_packages

setup(
    name="tracsis-cli",
    version="1.0.0",
    description="Command line tool for Tracsis API",
    author="Your Name",
    author_email="your.email@example.com",
    py_modules=["tracsis_cli"],
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "tracsis=tracsis_cli:main",
        ],
    },
    python_requires=">=3.7",
)