from setuptools import setup 

setup(
    name="ffconverter",
    version="0.1",
    description="File Format Converter",
    url='https://github.com/ttteety/file-format-converter',
    author='Atit',
    author_email='ttteety@yahoo.com',
    license='MIT',
    packages=['ffconverter'],
    install_rquires=[
        'pandas<=1.5.10',
    ],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['ffconverter=ffconverter:main'],
    }
)