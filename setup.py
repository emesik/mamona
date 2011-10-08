from distutils.core import setup

setup(name="mamona",
      version="0.1",
      description="Fully portable Django payments application",
      author="Michał Sałaban",
      author_email="",
      url="http://michal.salaban.info",
      packages=["mamona",],
      package_dir={"": "mamona"},
      classifiers=["Environment :: Web Environment",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Framework :: Django",])