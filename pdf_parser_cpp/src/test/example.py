# This file was created automatically by SWIG 1.3.29.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _example
import new
new_instancemethod = new.instancemethod
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class PySwigIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, PySwigIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, PySwigIterator, name)
    def __init__(self): raise AttributeError, "No constructor defined"
    __repr__ = _swig_repr
    __swig_destroy__ = _example.delete_PySwigIterator
    __del__ = lambda self : None;
    def value(*args): return _example.PySwigIterator_value(*args)
    def incr(*args): return _example.PySwigIterator_incr(*args)
    def decr(*args): return _example.PySwigIterator_decr(*args)
    def distance(*args): return _example.PySwigIterator_distance(*args)
    def equal(*args): return _example.PySwigIterator_equal(*args)
    def copy(*args): return _example.PySwigIterator_copy(*args)
    def next(*args): return _example.PySwigIterator_next(*args)
    def previous(*args): return _example.PySwigIterator_previous(*args)
    def advance(*args): return _example.PySwigIterator_advance(*args)
    def __eq__(*args): return _example.PySwigIterator___eq__(*args)
    def __ne__(*args): return _example.PySwigIterator___ne__(*args)
    def __iadd__(*args): return _example.PySwigIterator___iadd__(*args)
    def __isub__(*args): return _example.PySwigIterator___isub__(*args)
    def __add__(*args): return _example.PySwigIterator___add__(*args)
    def __sub__(*args): return _example.PySwigIterator___sub__(*args)
    def __iter__(self): return self
_example.PySwigIterator_swigregister(PySwigIterator)

class IntSet(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, IntSet, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, IntSet, name)
    __repr__ = _swig_repr
    def iterator(*args): return _example.IntSet_iterator(*args)
    def __iter__(self): return self.iterator()
    def __nonzero__(*args): return _example.IntSet___nonzero__(*args)
    def __len__(*args): return _example.IntSet___len__(*args)
    def append(*args): return _example.IntSet_append(*args)
    def __contains__(*args): return _example.IntSet___contains__(*args)
    def __getitem__(*args): return _example.IntSet___getitem__(*args)
    def __init__(self, *args): 
        this = _example.new_IntSet(*args)
        try: self.this.append(this)
        except: self.this = this
    def empty(*args): return _example.IntSet_empty(*args)
    def size(*args): return _example.IntSet_size(*args)
    def clear(*args): return _example.IntSet_clear(*args)
    def swap(*args): return _example.IntSet_swap(*args)
    def get_allocator(*args): return _example.IntSet_get_allocator(*args)
    def begin(*args): return _example.IntSet_begin(*args)
    def end(*args): return _example.IntSet_end(*args)
    def rbegin(*args): return _example.IntSet_rbegin(*args)
    def rend(*args): return _example.IntSet_rend(*args)
    def count(*args): return _example.IntSet_count(*args)
    def erase(*args): return _example.IntSet_erase(*args)
    def find(*args): return _example.IntSet_find(*args)
    def lower_bound(*args): return _example.IntSet_lower_bound(*args)
    def upper_bound(*args): return _example.IntSet_upper_bound(*args)
    def equal_range(*args): return _example.IntSet_equal_range(*args)
    def insert(*args): return _example.IntSet_insert(*args)
    __swig_destroy__ = _example.delete_IntSet
    __del__ = lambda self : None;
_example.IntSet_swigregister(IntSet)

class Math(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Math, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Math, name)
    __repr__ = _swig_repr
    def pi(*args): return _example.Math_pi(*args)
    def __init__(self, *args): 
        this = _example.new_Math(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _example.delete_Math
    __del__ = lambda self : None;
_example.Math_swigregister(Math)

fn = _example.fn


