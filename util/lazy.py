
"""
lazy - Decorators and utilities for lazy evaluation in Python
Alberto Bertogli (albertito@blitiri.com.ar)
"""

class _LazyWrapper:
	"""Lazy wrapper class for the decorator defined below.
	It's closely related so don't use it.

	We don't use a new-style class, otherwise we would have to implement
	stub methods for __getattribute__, __hash__ and lots of others that
	are inherited from object by default. This works too and is simple.
	I'll deal with them when they become mandatory.
	"""
	def __init__(self, f, args, kwargs):
		self._override = True
		self._isset = False
		self._value = None
		self._func = f
		self._args = args
		self._kwargs = kwargs
		self._override = False

	def _checkset(self):
		if not self._isset:
			self._override = True
			self._value = self._func(*self._args, **self._kwargs)
			self._isset = True
			self._checkset = lambda: True
			self._override = False

	def __getattr__(self, name):
		if self.__dict__['_override']:
			# XXX: This check added by Jonathan Heathcote to ignore calls to __trunc__
			# which makes everything work but it is not understood why this was being
			# called in the first place...
			if name in self.__dict__:
				return self.__dict__[name]
		self._checkset()
		return self._value.__getattribute__(name)

	def __setattr__(self, name, val):
		if name == '_override' or self._override:
			self.__dict__[name] = val
			return
		self._checkset()
		setattr(self._value, name, val)
		return

def lazy(f):
	"Lazy evaluation decorator"
	def newf(*args, **kwargs):
		return _LazyWrapper(f, args, kwargs)

	return newf


class _AsNeededWrapper:
	"""
	Perform the function action every time the value is requested
	
	An addition by Jonathan Heathcote.
	"""
	
	def __init__(self, f, args, kwargs):
		self._func = f
		self._args = args
		self._kwargs = kwargs

	def __getattr__(self, name):
		if name in ["_func", "_args", "_kwargs"]:
			return self.__dict__[name]
		return self._func(*self._args, **self._kwargs).__getattribute__(name)

	def __setattr__(self, name, val):
		if name in ["_func", "_args", "_kwargs"]:
			self.__dict__[name] = val
			return
		setattr(self._func(*self._args, **self._kwargs), name, val)
		return


def as_needed(f):
	"Evaluate every time the value is needed evaluation decorator"
	def newf(*args, **kwargs):
		return _AsNeededWrapper(f, args, kwargs)

	return newf
