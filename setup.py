from setuptools import setup
 
setup(
    name="jadnutils",
    version="0.2.0", 
    packages=["jadnutils", "jadnutils.json", "jadnutils.html", "jadnutils.utils", "jadnutils.support"],
    install_requires=[
        "pytest",
        "pandas"
    ]    
)