from setuptools import setup

DIST_NAME = 'PTCAccount2'
VERSION = 'v2.0.8'
AUTHOR = 'Kitryn'
EMAIL = 'snowfennard@gmail.com'
GITHUB_USER = 'Kitryn'
GITHUB_URL = 'https://github.com/{GITHUB_USER}/{DIST_NAME}'.format(**locals())

setup(
    name=DIST_NAME,
    packages=['ptcaccount2'],
    version=VERSION,
    description='Semi-automatic creation of Pokemon Trainer Club accounts.',
    author=AUTHOR,
    author_email=EMAIL,
    url=GITHUB_URL,
    license='BSD-new',
    download_url='{GITHUB_URL}/tarball/master'.format(**locals()),
    keywords='',
    install_requires=[
        'selenium==2.53.6'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'console_scripts': [
            'ptc2 = ptcaccount2.console:entry',
        ],
    }
)
