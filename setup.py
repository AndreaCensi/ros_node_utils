import os
from setuptools import setup, find_packages

version = "1.0"

description = """

"""

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
long_description = read('README.rst')
    

setup(name='ros_node_utils',
      author="Andrea Censi",
      author_email="censi@mit.edu",
      url='http://github.com/AndreaCensi/ros_node_utils',
      
      description=description,
      long_description=long_description,
      keywords="ROS",
      license="LGPL",
      
      classifiers=[
        'Development Status :: 4 - Beta',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        # 'Topic :: Software Development :: Quality Assurance',
        # 'Topic :: Software Development :: Documentation',
        # 'Topic :: Software Development :: Testing'
      ],

	  version=version,
      download_url='http://github.com/AndreaCensi/ros_node_utils/tarball/%s' % version,
      
      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=[ ],
      tests_require=['nose'],
      entry_points={},
)

