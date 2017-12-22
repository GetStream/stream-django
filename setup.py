import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

requirements = [
    'django>=1.5,<2.1.0',
    'stream-python>=2.8.1',
    'pytz'
]

extras_require = {
    'test': ['httpretty', 'coverage'],
}

setup(
    name='stream-django',
    version='1.3.3',
    packages=['stream_django'],
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    tests_require=['stream_django[test]'],
    test_suite='runtests.runtests',
    license='BSD License',
    description='A Django app to build activity, news and notification feeds.',
    long_description=README,
    url='https://getstream.io/',
    author='Tommaso Barbugli',
    author_email='tbarbugli@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
