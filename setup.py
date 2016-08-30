#!/usr/bin/python

from distutils.core import setup

setup(name='pymandrake',
		version='0.1',
		description='Python Mandrake Plugins',
		author='Stephen Hosom',
		author_email='0xhosom@gmail.com',
		url='https://github.com/hosom/pymandrake',
		packages=['pymandrake'],
		install_requires=[
			'python-jsonrpc',
		],
		)
