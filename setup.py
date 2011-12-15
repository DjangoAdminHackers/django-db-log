from setuptools import find_packages
from setuptools import setup

setup(name='django-db-log',
      version='0.1',
      description='django db log',
      author='Andy Baker',
      author_email='andy@andybak.net',
      packages=find_packages(),
      package_data={
          'djangodblog': [
            'templates/*.html',
          ]
      },
      include_package_data=True,
)
