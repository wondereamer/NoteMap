from pdfviewer import *
print "load sucess!" 
open_file("python.pdf")
print get_spec_annots(get_annot_types())
