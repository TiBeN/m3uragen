import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="m3uragen",
    version="1.0.0",
    author="Benjamin Legendre",
    author_email="jeff58888@hotmail.com",
    description="Generate M3U playlists from multi images software romsets for use with RetroArch ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TiBeN/m3uragen",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'm3uragen=m3uragen.main:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
