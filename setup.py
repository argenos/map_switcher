from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['map_switcher'],
    package_dir={'map_switcher': 'src/map_switcher'}
)

setup(**d)
