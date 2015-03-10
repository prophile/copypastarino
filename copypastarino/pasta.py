import os
import os.path
import six
from six.moves import input
import datetime
import textwrap
import subprocess
from six.moves.urllib.request import urlretrieve


class Pasta(object):
    def __init__(self, directory, library=True, tests=False, python2=False):
        self.path = directory
        self.name = os.path.basename(directory)
        self.library = library
        self.tests = tests
        self.python2 = python2

    def setup(self):
        self.create_directory_if_necessary()
        self.get_metadata()
        self.create_setup()
        self.create_license()
        self.create_readme()
        if self.tests:
            self.create_skeleton_tests()
            self.create_travis_yml()
        self.create_gitignore()
        if self.tests and self.is_git_repo():
            self.start_travis()
        self.create_skeleton_source()
        if not self.is_git_repo():
            self.create_git_repo()

    def create_git_repo(self):
        self.git_command(('init',))
        self.git_command(('add', '.'))
        self.git_command(('commit', '-m', 'Initial commit.'))
        with open(os.path.join(self.path, '.git', 'description'), 'w') as f:
            f.write(self.description + '\n')
        with open(os.path.join(self.path, '.git', 'info', 'exclude'), 'a') as f:
            f.write('venv\n')

    def create_skeleton_source(self):
        directory = os.path.join(self.path, self.name)
        os.mkdir(directory)
        if self.library:
            self.create_skeleton_library(directory)
        else:
            self.create_skeleton_program(directory)

    def create_skeleton_library(self, directory):
        with open(os.path.join(directory, '__init__.py'), 'w') as f:
            f.write('"""{}"""\n'.format(self.description))

    def create_skeleton_program(self, directory):
        with open(os.path.join(directory, '__init__.py'), 'w') as f:
            f.write('from .cli import main\n')
        with open(os.path.join(directory, '__main__.py'), 'w') as f:
            f.write('from .cli import main\n\nmain()\n')
        with open(os.path.join(directory, 'cli.py'), 'w') as f:
            f.write('from .args import argument_parser\n')
            f.write('from .run import run\n\n')
            f.write('import sys\n\n')
            f.write('def main(args=sys.argv[1:]):\n')
            f.write('    config = argument_parser().parse_args(args)\n')
            f.write('    run(config)\n')
        with open(os.path.join(directory, 'run.py'), 'w') as f:
            if self.python2:
                f.write('from __future__ import print_function\n\n')
            f.write('def run(config):\n')
            f.write('    print("Hello, world!")\n')
        with open(os.path.join(directory, 'args.py'), 'w') as f:
            f.write('import argparse\nimport pkg_resources\n')
            f.write('from email.parser import FeedParser\n\n')
            f.write('def get_package_metadata():\n')
            f.write('    dist = pkg_resources.get_distribution({name!r})\n'.format(name=self.name))
            f.write('    if dist.has_metadata("METADATA"):\n')
            f.write('        metadata = dist.get_metadata("METADATA")\n')
            f.write('    elif dist.has_metadata("PKG-INFO"):\n')
            f.write('        metadata = dist.get_metadata("PKG-INFO")\n')
            f.write('    else:\n')
            f.write('        metadata = ""\n')
            f.write('    feed_parser = FeedParser()\n')
            f.write('    feed_parser.feed(metadata)\n')
            f.write('    return dict(feed_parser.close())\n\n')
            f.write('def argument_parser():\n')
            f.write('    metadata = get_package_metadata()\n')
            f.write('    parser = argparse.ArgumentParser(description=metadata.get("Summary"))\n')
            f.write('    parser.add_argument("-V", "--version", action="version",\n')
            f.write('                        version="{} {}".format(metadata.get("Name"),')
            f.write('                                               metadata.get("Version"),')
            f.write('                        help="show version")\n')
            f.write('    return parser\n')

    def is_git_repo(self):
        return os.path.exists(os.path.join(self.path, '.git'))

    def create_directory_if_necessary(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def create_skeleton_tests(self):
        os.mkdir(os.path.join(self.path, 'tests'))
        with open(os.path.join(self.path, 'tests', 'test_{}.py'.format(self.name)), 'w') as f:
            f.write('from nose.tools import eq_\n\n')
            f.write('import {}\n\n'.format(self.name))
            f.write('def test_tests_written():\n')
            f.write('    """Test that {} has written some tests."""\n'.format(self.author.split(' ')[0]))
            f.write('    raise AssertionError("Ceci n\'est pas un test.")\n')

    def create_travis_yml(self):
        with open(os.path.join(self.path, '.travis.yml'), 'w') as f:
            f.write('language: python\n')
            f.write('sudo: false\n')
            f.write('python:\n')
            for python in self.supported_pythons:
                f.write('  - \'{}\'\n'.format(python))
            f.write('install: python setup.py develop\n')
            f.write('script: python setup.py nosetests\n')

    def create_gitignore(self):
        urlretrieve('https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore',
                    os.path.join(self.path, '.gitignore'))

    def create_readme(self):
        with open(os.path.join(self.path, 'README.rst'), 'w') as f:
            f.write(self.name + '\n')
            f.write(('=' * len(self.name)) + '\n\n')
            # TODO: if it's github and there are tests, include the Travis badge
            f.write('{}\n'.format(self.description))

    def create_license(self):
        creator = getattr(self, 'create_license_{}'.format(self.license))
        creator()

    def create_license_MIT(self):
        prototype = """
        Copyright (c) {year} {author}

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
        THE SOFTWARE.
        """

        license = textwrap.dedent(prototype)
        with open(os.path.join(self.path, 'LICENSE'), 'w') as f:
            f.write(license.format(year=datetime.date.today().year,
                                   author=self.author))

    def create_setup(self):
        prototype = """
        from setuptools import setup, find_packages

        with open('README.rst') as f:
            long_description = f.read()

        setup(name={name!r},
              version={version!r},
              author={author!r},
              author_email={author_email!r},
              license={license!r},
              url={url!r},
              long_description=long_description,
              classifiers=[
                {classifiers_list}
              ],
              zip_safe=True,
              packages=find_packages(),
              setup_requires=[
                'wheel >= 0.24, <1',
                {nose_requirement}
              ],
              {entry_points})
        """

        prototype = textwrap.dedent(prototype)

        if self.library:
            entry_points = ''
        else:
            entry_points = "{{'console_scripts': ['{name} = {name}:main']}}".format(name=self.name)

        classifiers_list = '\n'.join('        {classifier!r},'.format(classifier=c) for c in self.classifiers).lstrip()

        if self.tests:
            nose_requirement = "'nose >= 1.3, <2',"
        else:
            nose_requirement = ''

        with open(os.path.join(self.path, 'setup.py'), 'w') as f:
            f.write(prototype.format(name=self.name,
                                     version=self.version,
                                     author=self.author,
                                     author_email=self.author_email,
                                     license=self.license,
                                     url=self.url,
                                     classifiers_list=classifiers_list,
                                     nose_requirement=nose_requirement,
                                     entry_points=entry_points))

        if self.python2:
            with open(os.path.join(self.path, 'setup.cfg'), 'w') as f:
                f.write('[bdist_wheel]\nuniversal=1\n')

    def git_command(self, cmd):
        return subprocess.check_output(('git',) + tuple(cmd),
                                        cwd=self.path,
                                        universal_newlines=True).strip()

    def compute_author_credentials(self):
        return (self.git_command(('config', 'user.name')),
                self.git_command(('config', 'user.email')))

    @property
    def supported_pythons(self):
        if self.python2:
            return ('2.7', '3.2', '3.3', '3.4')
        else:
            return ('3.4',)

    def compute_url(self):
        try:
            origin_url = self.git_command(('config', 'remote.origin.url'))
        except subprocess.CalledProcessError:
            origin_url = ''
        if origin_url.startswith('http://') or origin_url.startswith('https://'):
            return origin_url
        if origin_url.startswith('git@github.com:') or origin_url.startswith('github:'):
            return 'https://github.com/' + origin_url[origin_url.index(':') + 1:]
        return input('Project URL: ')

    def get_metadata(self):
        # Items: version, url, author, author_email, classifiers, description
        self.version = '0.1.0'
        self.author, self.author_email = self.compute_author_credentials()
        self.description = input('Project description: ')
        self.url = self.compute_url()
        self.license = 'MIT'
        self.classifiers = []
        self.classifiers.append('Development Status :: 2 - Pre-Alpha')
        self.classifiers.append('License :: OSI Approved :: MIT License')
        self.classifiers.append('Operating System :: POSIX')
        for python in self.supported_pythons:
            self.classifiers.append('Programming Language :: Python :: {}'.format(python))
