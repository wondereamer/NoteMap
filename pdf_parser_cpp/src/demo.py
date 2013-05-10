from pdfviewer import *
print "load sucess!" 
open_file("2008.pdf")
print annotations()
print "***************************************************" 
a = set()
annot = Annot()
annot.first = "ok"
aset = AnnotSet()
aset.insert(annot)
print get_spec_annots(aset)
print "************************" 
