
"""
This setup.py allows your python package to be installed. 
Please completely update the parameters in the opts dictionary. 
For more information, see https://stackoverflow.com/questions/1471994/what-is-setup-py
"""

from setuptools import setup, find_packages
PACKAGES = find_packages()

opts = dict(name='new_hire',
            maintainer='Chilliwack',
            maintainer_email='chilliwack@nowhere.com',
            description='new_hire is a script and set of functions that intergrates with the Hutchs Toolbox system',
            long_description=("""new_hire is a script and set of functions that intergrates with the Hutchs Toolbox system to make it easier to identify new users."""),
            url='https://github.com/FredHutch/new_data_employee',
            license='MIT', # default license, change here and in the git repo if using a different license
            author='Chilliwack',
            author_email='chilliwack@nowhere.com',
            version='0.1',
            packages=PACKAGES
           )

setup(**opts)
