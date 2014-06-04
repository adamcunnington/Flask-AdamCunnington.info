#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name="Flask-AdamCunnington",
      version="1.0",
      description="The contents of http://adamcunnington.info",
      author="Adam Cunnington",
      author_email="ac@adamcunnington.info",
      license="GPLv3",
      classifiers=[
          "Development Status :: 1 - Planning",
          "Environment :: Web Environment",
          "Framework :: Flask",
          "Intended Audience :: End Users/Desktop",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.0",
          "Programming Language :: Python :: 3.1",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content"],
      keywords="adam cunnington adamcunnington adamcunnington.info",
      packages=find_packages(exlude=".virtualenv"),
      install_requires=["flask", "flask-httpauth", "flask-sqlalchemy"])
