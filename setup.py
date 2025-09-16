from setuptools import setup
 
setup(
    name="jadnutils",
    version="0.1.0", 
    packages=["jadnutils", "jadnutils.html", "jadnutils.utils", "jadnutils.support"],
    install_requires=[
        "pytest",
        "pandas"
    ]    
)