from setuptools import setup, find_packages

__version__ = "0.0.1"

short_desc = (
    "Faster FVA Algorithm that needs less solves"
)

with open('README.md') as f:
    long_description = f.read()


setup(
    name='FasterFVA',
    version=__version__,
    author='Dustin R. Kenefake',
    author_email='Dustin.Kenefake@tamu.edu',
    description=short_desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/DKenefake/fasterfva',
    extras_require={
        'test': ['pytest']
    },
    install_requires=["numpy",
                      "scipy",
                      "gurobipy",],
    packages=find_packages(where='src'),
    package_dir={'': 'src'}
)