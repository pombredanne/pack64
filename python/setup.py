from setuptools import setup

setup(
    name="pack64",
    version = '1.0.2',
    maintainer='Luminoso, LLC',
    maintainer_email='dev@lumino.so',
    license = "MIT",
    url = 'http://github.com/LuminosoInsight/pack64',
    platforms = ["any"],
    description = "A library for encoding and decoding floating point vectors into a compact, base64-like format",
    py_modules=['pack64'],

    # This package additionally requires NumPy, but will not try to
    # auto-install it.

    #install_requires=['numpy'],
)
