import os
from setuptools import setup

VERSION = '0.0'
DESCRIPTION = 'Data generation, feature extraction and classification'
LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='pythogram-core',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=['Natural Language :: English',
                 'Topic :: Scientific/Engineering',
                 'Intended Audience :: Science/Research',
                 'Development Status :: 1 - Planning',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 ],
    keywords=['python',
              'photogrammetry',
              'artificial data',
              'feature extraction',
              'machine learning',
              'classification',
              ],
    author='Christodoulos Psaltis',
    author_email='cpsaltis@unweb.me',
    url='http://github.com/photogrammetry/pythogram-core',
    license='MIT License',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    zip_safe=False,
    install_requires=[
        'setuptools',
        'numpy',
        'scipy',
        'pillow',
        'scikit-image',
        'scikit-learn',
    ],
    entry_points={
        'console_scripts': [
            'gram = core.scripts.gram:gram',
        ],
    },
)
