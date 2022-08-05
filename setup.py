from setuptools import setup, find_packages

setup(
    name="mosmix2geojson",
    version="0.0.1",
    description="Convert DWD MOSMIX data to GeoJSON.",
    url="https://github.com/DeutscherWetterdienst/mosmix2geojson",

    packages=find_packages("src"),
    package_dir={"": "src"},

    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "mosmix2geojson = mosmix2geojson.__main__:main"
        ]
    },
    extras_require={
        "dev": ["bump2version>=1.0.1"]
    }
)
