import os
import sys
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

if sys.version_info < (3, 0, 0):
    django = "django>=1.11.29,<2.0"
else:
    django = "django>=2.0,<5.0"

requirements = [django, "stream-python>=3.0.1", "pytz"]

extras_require = {
    "test": ["httpretty"],
    "ci": ["black; python_version > '3.6'", "flake8", "pytest-cov", "pytest-django"],
}

version = "1.8.0"

setup(
    name="stream-django",
    version=version,
    url="https://github.com/GetStream/stream-django",
    project_urls={
        "Bug Tracker": "https://github.com/GetStream/stream-django/issues",
        "Documentation": "https://getstream.io/activity-feeds/docs/python/adding_activities/?language=python",
        "Release Notes": "https://github.com/GetStream/stream-django/releases/tag/{}".format(
            version
        ),
    },
    packages=["stream_django"],
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    license="BSD License",
    description="A Django app to build activity, news and notification feeds.",
    long_description_content_type="text/markdown",
    long_description=README,
    author="Tommaso Barbugli",
    author_email="tbarbugli@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
