import yaml
#from pprint import pprint
import util
with open('yaml.txt', "r") as f:
    doc = util.my_decode(f.read())
    print doc
    print "-----------" 
    obj = yaml.load(doc)
    print obj
