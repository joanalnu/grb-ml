from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read()

with open("grb_ml/_version.py", "r") as version_file:
    for line in version_file:
        if "__version__" in line:
            __version__ = line.split()[-1].replace('"','')


setup(
        name="GRB-ML",
        # version=__version__,
        author="Alcaide-Núñez, J.",
        author_email="",
        description="CubeSat GRB Detection",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/joanalnu/grb-ml",
        packages=find_packages(),
        python_requires=">=3.12",
        install_requires=requirements,
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Unix'
            ],
        package_data={'package_name': ['static/*']},
        include_package_data=True,
        )
