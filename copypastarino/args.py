import argparse
import pkg_resources
from email.parser import FeedParser


def get_package_metadata():
    dist = pkg_resources.get_distribution('copypastarino')
    if dist.has_metadata('METADATA'):
        metadata = dist.get_metadata('METADATA')
    elif dist.has_metadata('PKG-INFO'):
        metadata = dist.get_metadata('PKG-INFO')
    else:
        metadata = ''
    feed_parser = FeedParser()
    feed_parser.feed(metadata)
    pkg_info = feed_parser.close()
    return dict(pkg_info)


def argument_parser():
    metadata = get_package_metadata()
    parser = argparse.ArgumentParser(description=metadata['Summary'])
    parser.add_argument('-V', '--version',
                        action='version',
                        version='{Name} {Version}'.format(**metadata),
                        help='show version')
    parser.add_argument('-t', '--tests',
                        action='store_true',
                        help='enable tests')
    parser.add_argument('-2', '--python2',
                        action='store_true',
                        help='enable Python 2 compatibility')
    parser.add_argument('-l', '--library',
                        action='store_true',
                        help='make project a library, not a program')
    parser.add_argument('project',
                        help='path to project')
    return parser
