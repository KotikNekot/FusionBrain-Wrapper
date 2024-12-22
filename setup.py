from setuptools import setup, find_packages

setup(
    name='fusionbrain',
    version='0.1.0',
    packages=find_packages,
    install_requires=["aiohttp", "pydantic"],
    author='whynotvoid',
    description='api wrapper for fusionbrain https://fusionbrain.ai/docs/doc/api-dokumentaciya/',
    url='https://github.com/KotikNekot/FusionBrain-Wrapper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)