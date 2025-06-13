from setuptools import setup, find_packages

setup(
    name="tracsis-cli",
    version="1.0.0",
    description="Command line tool for Tracsis API",
    author="Sajid Ahmed",
    author_email="abu.syeed@apsissolutions.com",
    py_modules=["tracsis_cli", "tracsis_api", "command_handlers"],
    install_requires=[
        "requests>=2.25.0",
        "selenium==4.15.0",
        "webdriver-manager==4.0.0"
    ],
    entry_points={
        "console_scripts": [
            "tracsis=tracsis_cli:main",
        ],
    },
    python_requires=">=3.7",
)