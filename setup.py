try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(name='vaelstmpredictor',
      version=0.2,
      description='Combined Classifying, Regressing, Variational Autoencoder, \
                  and Long Short Term Memory Recurrent Neural Network for \
                  Autocorrelated Data',
      long_description=open('README.md').read(),
      url='https://github.com/exowanderer/vaelstmpredictor',
      license='GPL3',
      author="(Algorithm + Original Code) Jay A. Hennig, Akash Umakantha, "\
            "Ryan C. Williamson, and (Updated Code) "\
            "Jonathan Fraine (exowanderer)",
      packages=find_packages(),
      install_requires=['tensorflow>=1.4.0', 'keras>2.0.8', 'scipy', 'numpy'],
      extras_require={'plots':  ["matplotlib"]}
      )