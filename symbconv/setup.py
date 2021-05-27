#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="symbconv",
    version="1.0.1",
    description="Symbol Converter and Utility",
    long_description="",
    long_description_content_type='text/x-rst',
    author="Iceflower S",
    author_email="iceflower@gmx.de",
    license='MIT',
    url="",
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Environment :: Console',
    ],
    packages=find_packages(include=['symbconv', 'symbconv.*']),
    python_requires='>=3.9',
    install_requires=[
        "lxml",
        "scour",
        "tqdm",
    ],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'symbconv = symbconv.main:main',
        ],
    },
)
