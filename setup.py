"""
Command line tool for nuking a directory..
"""
from setuptools import find_packages, setup
from os import path
import nuke

dependencies = [
    "click==6.7", 
    "crayons==0.1.2"
]

here = path.abspath(path.dirname(__file__))

setup(
    name='nuke',
    version=nuke.__version__,
    url='https://github.com/varunagrawal/nuke',
    license=nuke.__license__,
    author=nuke.__author__,
    author_email=nuke.__email__,
    description='Command line tool to nuke a directory',
    long_description=open("README.md", 'r').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'nuke = nuke.nuke:main',
        ],
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)