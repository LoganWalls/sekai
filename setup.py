from setuptools import setup

setup(
        name='sekai',
        version='0.1',
        description='Sekai is a minimalist framework for defining simple grid-world simulations.',
        url='https://github.com/LoganWalls/sekai',
        author='Logan Walls',
        packages=['sekai'],
        install_requires=[
            'asciimatics',
        ],
        zip_safe=False
)
