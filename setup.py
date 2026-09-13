from setuptools import setup, find_packages

setup(
    name="univac_ix_aerospace_bridge",
    version="1.0.0",
    author="Revolutionary Technology Company",
    description="Form-molded bridge node for Boeing and Lockheed Martin systems via UNIVAC IX",
    long_description_content_type="text/markdown",
    url="https://github.com",
    
    # Automatically locate and configure all modules within the src/ directory
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    
    # Track critical physical and software math runtimes
    install_requires=[
        "numpy>=1.24.0",
    ],
    
    # Track integration test runners
    extras_require={
        "test": [
            "pytest>=7.4.0",
        ],
    },
    
    # Configure absolute Python target runtime constraints
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Aerospace Engineers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
