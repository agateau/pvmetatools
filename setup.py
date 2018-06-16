#!/usr/bin/env python3
from setuptools import setup

import pvmeta

with open('README.md') as f:
    long_description = f.read()

setup(
    name=pvmeta.__appname__,
    version=pvmeta.__version__,
    description=pvmeta.DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Aurélien Gâteau',
    author_email='mail@agateau.com',
    license=pvmeta.__license__,
    url='https://github.com/agateau/pvmeta',
    packages=['pvmeta'],
    entry_points={
        'console_scripts': [
            'pvmeta-video-adjusttime = pvmeta.video_adjusttime:main',
            'pvmeta-video-autorename = pvmeta.video_autorename:main',
            'pvmeta-video-metaread = pvmeta.video_metaread:main',
            'pvmeta-video-metawrite = pvmeta.video_metawrite:main',
        ],
    },
    classifiers=[
        # TODO
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        # TODO
        # 'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        # TODO: Topic
    ],
    keywords='video photo meta time',
)
