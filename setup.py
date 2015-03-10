from setuptools import find_packages, setup

with open('README.rst') as f:
    long_description = f.read()

setup(name='copypastarino',
      version='0.1.0',
      author='Alistair Lynn',
      author_email='alistair@alynn.co.uk',
      license='MIT',
      url='https://github.com/prophile/copypastarino',
      description='Simple Python project generator',
      long_description=long_description,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Utilities'
      ],
      entry_points={'console_scripts':
        'copypastarino=copypastarino:main'
      },
      zip_safe=True,
      install_requires=[
        'six >=1.9, <2'
      ],
      packages=find_packages())
