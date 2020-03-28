from setuptools import setup, find_packages

setup(
    name="curver",
    description="Curve editor",
    version="0.0.1",
    author=u"Wojciech Pratkowiecki",
    author_email="wpratkowiecki@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt5==5.14.1",
        "PyQt5-sip==12.7.1",
    ],
    python_requires=">=3.6",
)
