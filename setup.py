# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

PACKAGES = ['mamona', 'mamona.backends', 'mamona.backends.dummy', 'mamona.backends.paypal']

setup(
	name="mamona",
	version="0.1",
	description="Fully portable Django payments application",
	author=u"Michał Sałaban",
	author_email="michal@salaban.info",
	url="http://github.com/emesik/mamona",
#	package_dir={'mamona': 'mamona'},
	packages=PACKAGES,
	include_package_data=True,
#	package_data={'mamona': data_files}, 
	classifiers=[
		"Environment :: Web Environment",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: BSD License",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Framework :: Django",
		],
	zip_safe=False
	)
