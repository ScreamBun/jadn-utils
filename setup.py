from setuptools import setup
 
setup(
    name="jadnutils",
    version="0.2.0", 
    packages=["jadnutils", "jadnutils.html", "jadnutils.utils", "jadnutils.support"],
    install_requires=[
        "pytest",
        "pandas"
    ],
    include_package_data=True,
    package_data={
        "jadnutils.support": ["theme.css"],
    },
)