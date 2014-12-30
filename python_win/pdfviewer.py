# This file was created automatically by SWIG 1.3.29.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _pdfviewer
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
    __swig_destroy__ = _pdfviewer.delete_PySwigIterator
    __del__ = lambda self : None;
    def value(*args): return _pdfviewer.PySwigIterator_value(*args)
    def incr(*args): return _pdfviewer.PySwigIterator_incr(*args)
    def decr(*args): return _pdfviewer.PySwigIterator_decr(*args)
    def distance(*args): return _pdfviewer.PySwigIterator_distance(*args)
    def equal(*args): return _pdfviewer.PySwigIterator_equal(*args)
    def copy(*args): return _pdfviewer.PySwigIterator_copy(*args)
    def next(*args): return _pdfviewer.PySwigIterator_next(*args)
    def previous(*args): return _pdfviewer.PySwigIterator_previous(*args)
    def advance(*args): return _pdfviewer.PySwigIterator_advance(*args)
    def __eq__(*args): return _pdfviewer.PySwigIterator___eq__(*args)
    def __ne__(*args): return _pdfviewer.PySwigIterator___ne__(*args)
    def __iadd__(*args): return _pdfviewer.PySwigIterator___iadd__(*args)
    def __isub__(*args): return _pdfviewer.PySwigIterator___isub__(*args)
    def __add__(*args): return _pdfviewer.PySwigIterator___add__(*args)
    def __sub__(*args): return _pdfviewer.PySwigIterator___sub__(*args)
    def __iter__(self): return self
_pdfviewer.PySwigIterator_swigregister(PySwigIterator)

class Annot(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Annot, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Annot, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _pdfviewer.new_Annot(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_setmethods__["first"] = _pdfviewer.Annot_first_set
    __swig_getmethods__["first"] = _pdfviewer.Annot_first_get
    if _newclass:first = property(_pdfviewer.Annot_first_get, _pdfviewer.Annot_first_set)
    __swig_setmethods__["second"] = _pdfviewer.Annot_second_set
    __swig_getmethods__["second"] = _pdfviewer.Annot_second_get
    if _newclass:second = property(_pdfviewer.Annot_second_get, _pdfviewer.Annot_second_set)
    def __len__(self): return 2
    def __repr__(self): return str((self.first, self.second))
    def __getitem__(self, index): 
      if not (index % 2): 
        return self.first
      else:
        return self.second
    def __setitem__(self, index, val):
      if not (index % 2): 
        self.first = val
      else:
        self.second = val
    __swig_destroy__ = _pdfviewer.delete_Annot
    __del__ = lambda self : None;
_pdfviewer.Annot_swigregister(Annot)

class AnnotSet(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, AnnotSet, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, AnnotSet, name)
    __repr__ = _swig_repr
    def iterator(*args): return _pdfviewer.AnnotSet_iterator(*args)
    def __iter__(self): return self.iterator()
    def __nonzero__(*args): return _pdfviewer.AnnotSet___nonzero__(*args)
    def __len__(*args): return _pdfviewer.AnnotSet___len__(*args)
    def append(*args): return _pdfviewer.AnnotSet_append(*args)
    def __contains__(*args): return _pdfviewer.AnnotSet___contains__(*args)
    def __getitem__(*args): return _pdfviewer.AnnotSet___getitem__(*args)
    def __init__(self, *args): 
        this = _pdfviewer.new_AnnotSet(*args)
        try: self.this.append(this)
        except: self.this = this
    def empty(*args): return _pdfviewer.AnnotSet_empty(*args)
    def size(*args): return _pdfviewer.AnnotSet_size(*args)
    def clear(*args): return _pdfviewer.AnnotSet_clear(*args)
    def swap(*args): return _pdfviewer.AnnotSet_swap(*args)
    def get_allocator(*args): return _pdfviewer.AnnotSet_get_allocator(*args)
    def begin(*args): return _pdfviewer.AnnotSet_begin(*args)
    def end(*args): return _pdfviewer.AnnotSet_end(*args)
    def rbegin(*args): return _pdfviewer.AnnotSet_rbegin(*args)
    def rend(*args): return _pdfviewer.AnnotSet_rend(*args)
    def count(*args): return _pdfviewer.AnnotSet_count(*args)
    def erase(*args): return _pdfviewer.AnnotSet_erase(*args)
    def find(*args): return _pdfviewer.AnnotSet_find(*args)
    def lower_bound(*args): return _pdfviewer.AnnotSet_lower_bound(*args)
    def upper_bound(*args): return _pdfviewer.AnnotSet_upper_bound(*args)
    def equal_range(*args): return _pdfviewer.AnnotSet_equal_range(*args)
    def insert(*args): return _pdfviewer.AnnotSet_insert(*args)
    __swig_destroy__ = _pdfviewer.delete_AnnotSet
    __del__ = lambda self : None;
_pdfviewer.AnnotSet_swigregister(AnnotSet)

class AnnotStruct(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, AnnotStruct, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, AnnotStruct, name)
    __repr__ = _swig_repr
    __swig_setmethods__["_y"] = _pdfviewer.AnnotStruct__y_set
    __swig_getmethods__["_y"] = _pdfviewer.AnnotStruct__y_get
    if _newclass:_y = property(_pdfviewer.AnnotStruct__y_get, _pdfviewer.AnnotStruct__y_set)
    __swig_setmethods__["_x"] = _pdfviewer.AnnotStruct__x_set
    __swig_getmethods__["_x"] = _pdfviewer.AnnotStruct__x_get
    if _newclass:_x = property(_pdfviewer.AnnotStruct__x_get, _pdfviewer.AnnotStruct__x_set)
    __swig_setmethods__["_page"] = _pdfviewer.AnnotStruct__page_set
    __swig_getmethods__["_page"] = _pdfviewer.AnnotStruct__page_get
    if _newclass:_page = property(_pdfviewer.AnnotStruct__page_get, _pdfviewer.AnnotStruct__page_set)
    def __lt__(*args): return _pdfviewer.AnnotStruct___lt__(*args)
    __swig_setmethods__["_content"] = _pdfviewer.AnnotStruct__content_set
    __swig_getmethods__["_content"] = _pdfviewer.AnnotStruct__content_get
    if _newclass:_content = property(_pdfviewer.AnnotStruct__content_get, _pdfviewer.AnnotStruct__content_set)
    __swig_setmethods__["_color"] = _pdfviewer.AnnotStruct__color_set
    __swig_getmethods__["_color"] = _pdfviewer.AnnotStruct__color_get
    if _newclass:_color = property(_pdfviewer.AnnotStruct__color_get, _pdfviewer.AnnotStruct__color_set)
    __swig_setmethods__["_type"] = _pdfviewer.AnnotStruct__type_set
    __swig_getmethods__["_type"] = _pdfviewer.AnnotStruct__type_get
    if _newclass:_type = property(_pdfviewer.AnnotStruct__type_get, _pdfviewer.AnnotStruct__type_set)
    def __init__(self, *args): 
        this = _pdfviewer.new_AnnotStruct(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _pdfviewer.delete_AnnotStruct
    __del__ = lambda self : None;
_pdfviewer.AnnotStruct_swigregister(AnnotStruct)

class AnnotStructVec(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, AnnotStructVec, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, AnnotStructVec, name)
    __repr__ = _swig_repr
    def iterator(*args): return _pdfviewer.AnnotStructVec_iterator(*args)
    def __iter__(self): return self.iterator()
    def __nonzero__(*args): return _pdfviewer.AnnotStructVec___nonzero__(*args)
    def __len__(*args): return _pdfviewer.AnnotStructVec___len__(*args)
    def pop(*args): return _pdfviewer.AnnotStructVec_pop(*args)
    def __getslice__(*args): return _pdfviewer.AnnotStructVec___getslice__(*args)
    def __setslice__(*args): return _pdfviewer.AnnotStructVec___setslice__(*args)
    def __delslice__(*args): return _pdfviewer.AnnotStructVec___delslice__(*args)
    def __delitem__(*args): return _pdfviewer.AnnotStructVec___delitem__(*args)
    def __getitem__(*args): return _pdfviewer.AnnotStructVec___getitem__(*args)
    def __setitem__(*args): return _pdfviewer.AnnotStructVec___setitem__(*args)
    def append(*args): return _pdfviewer.AnnotStructVec_append(*args)
    def empty(*args): return _pdfviewer.AnnotStructVec_empty(*args)
    def size(*args): return _pdfviewer.AnnotStructVec_size(*args)
    def clear(*args): return _pdfviewer.AnnotStructVec_clear(*args)
    def swap(*args): return _pdfviewer.AnnotStructVec_swap(*args)
    def get_allocator(*args): return _pdfviewer.AnnotStructVec_get_allocator(*args)
    def begin(*args): return _pdfviewer.AnnotStructVec_begin(*args)
    def end(*args): return _pdfviewer.AnnotStructVec_end(*args)
    def rbegin(*args): return _pdfviewer.AnnotStructVec_rbegin(*args)
    def rend(*args): return _pdfviewer.AnnotStructVec_rend(*args)
    def pop_back(*args): return _pdfviewer.AnnotStructVec_pop_back(*args)
    def erase(*args): return _pdfviewer.AnnotStructVec_erase(*args)
    def __init__(self, *args): 
        this = _pdfviewer.new_AnnotStructVec(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(*args): return _pdfviewer.AnnotStructVec_push_back(*args)
    def front(*args): return _pdfviewer.AnnotStructVec_front(*args)
    def back(*args): return _pdfviewer.AnnotStructVec_back(*args)
    def assign(*args): return _pdfviewer.AnnotStructVec_assign(*args)
    def resize(*args): return _pdfviewer.AnnotStructVec_resize(*args)
    def insert(*args): return _pdfviewer.AnnotStructVec_insert(*args)
    def reserve(*args): return _pdfviewer.AnnotStructVec_reserve(*args)
    def capacity(*args): return _pdfviewer.AnnotStructVec_capacity(*args)
    __swig_destroy__ = _pdfviewer.delete_AnnotStructVec
    __del__ = lambda self : None;
_pdfviewer.AnnotStructVec_swigregister(AnnotStructVec)

open_file = _pdfviewer.open_file
previous_page = _pdfviewer.previous_page
next_page = _pdfviewer.next_page
get_page = _pdfviewer.get_page
get_annot_types = _pdfviewer.get_annot_types
get_spec_annots = _pdfviewer.get_spec_annots


