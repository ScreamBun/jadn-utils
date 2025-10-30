from setuptools import setup
 
setup(
    name="jadnutils",
    version="0.4.0", 
    packages=["jadnutils", "jadnutils.json", "jadnutils.html", "jadnutils.utils", "jadnutils.support", "jadnutils.gv", "jadnutils.gv.utils", "jadnutils.puml"],
    install_requires=[
        "pytest",
        "pandas",
        "isodate",
        "python-dateutil"
    ],
    include_package_data=True,
    package_data={
        "jadnutils.support": ["theme.css"],
    },
)