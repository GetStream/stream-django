import os
import sys
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

if sys.version_info < (3, 0, 0):
    django = "django>=1.11.29,<2.0"
else:
    django = "django>=2.0,<3.3"  # checked https://docs.djangoproject.com/en/dev/releases/3.2/#backwards-incompatible-3-2

requirements = [django, "stream-python>=3.0.1", "pytz"]

extras_require = {"test": ["httpretty==1.1.1"], "ci": ["black", "flake8", "pytest-cov"]}

setup(
    name="stream-django",
    version="1.7.1",
    packages=["stream_django"],
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    tests_require=["stream_django[test]"],
    test_suite="runtests.runtests",
    license="BSD License",
    description="A Django app to build activity, news and notification feeds.",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://getstream.io/",
    author="Tommaso Barbugli",
    author_email="tbarbugli@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
