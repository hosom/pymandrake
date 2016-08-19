# pymandrake
A python library for building plugins for Mandrake.

All of the work for performing threaded RPC has been done within this API. All you have to do is define an analyze function and register it!

## Example Plugin
```python

#!/usr/bin/python 

import json

from pymandrake import Plugin

def analyze(fmeta):
	fm = json.loads(fmeta)
	return '{"Hello from Python" : "%s"}' % fm['Filepath']

def main():

	plug = Plugin('HelloWorldPython')
	plug.listen(analyze)

if __name__ == '__main__':
	main()
```
