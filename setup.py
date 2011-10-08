from distutils.core import setup
import os

# Package compilation taken from django-registration:
# http://bitbucket.org/ubernostrum/django-registration/src/tip/setup.py
# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('mamona'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[13:]
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(name="mamona",
      version="0.1",
      description="Fully portable Django payments application",
      author="Michal Salaban",
      author_email="",
      install_requires = ['setuptools'],
      url="http://michal.salaban.info",
      package_dir={'mamona': 'mamona'},
      packages=packages,
      package_data={'mamona': data_files}, 
      classifiers=["Environment :: Web Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Framework :: Django",])