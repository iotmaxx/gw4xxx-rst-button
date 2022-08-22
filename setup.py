from setuptools import setup, find_packages

version = {}
with open("iot_rst_button/version.py") as fp:
    exec(fp.read(), version)

setup(
    name='rst_button',
    version=version['__version__'],
    url='https://github.com/iotmaxx/iot_rst_button',
    author='Ralf Glaser',
    author_email='glaser@iotmaxx.de',
    description='GW4xxx reset button support',
    packages=find_packages(),    
    install_requires=[],
)
