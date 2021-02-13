import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Map_module",
    version="0.0.1",
    author="Marta Nahorniuk",
    author_email="marta.nahorniuk@ucu.edu.ua",
    description="Create a map of closest films",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martazavro/puzzle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8.5',
)