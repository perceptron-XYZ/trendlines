from setuptools import setup

install_rerquires = [
     'setuptools',
     'docopt',
     'requests'
]
setup(name='trendlines',
      version='0.1.0',
      packages=['trendlines'],
      entry_points={
          'console_scripts': [
              'trendlines = trendlines.main:main'
          ]
      },
)
