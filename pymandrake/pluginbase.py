from __future__ import print_function

import threading
import Queue
import sys
import signal
import pyjsonrpc

from datetime import datetime

def to_unicode(obj, encoding='utf-8'):
	'''Make strings unicode safe for stdout/stdin.
	'''
	if isinstance(obj, basestring):
		if not isinstance(obj, unicode):
			obj = unicode(obj, encoding, errors='replace')

	return obj


class Plugin:

	def __init__(self, name='Python_BASE', plugin_type='analyzer'):

		self.__NAME__ = name
		self.__plugin_type = plugin_type
		self.log('Initializing plugin.')
		self.queue = Queue.Queue()
		self.printer_thread = threading.Thread(target=self.printer)
		self.printer_thread.start()

		def signal_handler(signal, frame):
			self.queue.put('kill')
			self.printer_thread.join()
			sys.exit(0)

		signal.signal(signal.SIGINT, signal_handler)

	def log(self, *objs):
		'''A wrapper function that makes it easier to print logs in a more go
		friendly style.
		'''
		ts = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		print('[%s]' % self.__NAME__, ts, *objs, file=sys.stderr)

	def printer(self):
		'''Output handler. This method will poll the results queue and output
		results as they appear.
		'''
		while True:
			out = self.queue.get()
			if out == 'kill':
				self.log('Kill signal received, stopping threads.')
				return
			sys.stdout.write(out + '\n')
			sys.stdout.flush()

		return

	def worker(self, line):
		'''Worker thread that handles RPC server calls.'''
		out = self.rpc.call(line)
		self.log(out)
		self.queue.put(out)
		return

	def listen(self, method):
		'''Listen for JSON RPC method calls.'''
		method_name = 'Analyze'
		if self.__plugin_type == 'Logger':
			method_name = 'Log'
		self.rpc = pyjsonrpc.JsonRpc(methods = {'%s.%s' % (self.__NAME__ , method_name): method})
		line = sys.stdin.readline()

		while line:
			try:
				this_input = line
				t = threading.Thread(target=self.worker, args=[line])
				t.start()
				line = sys.stdin.readline()
			except Exception, e:
				self.log('Exception occurred: ', e)
				self.queue.put('kill')
				self.printer_thread.join()