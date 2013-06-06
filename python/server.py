import threading
import webbrowser
import BaseHTTPServer
import SimpleHTTPServer
import pdfviewer as pdf
import ConfigParser 
import webcolors
import re
import util
import mindmap

#import subprocess
from xml.etree import ElementTree
#cpp_server = subprocess.Popen('./readPdf', cwd = './bin' )
#cpp_server.kill()
#time.sleep(1)
WEB_ANNOT_FILE = 'web/annotations.html'
PORT = 8080
target_pdf = "" 
PDF_DIRECTORY = "../" 
# annotation types found in configure file
tr_rgbs= []
key_rgbs = []
# annotation types found in the target pdf
annot_types = set()
color_map = { }

class AnnotStruct(object):
    """struct wrap annotation from pdf.js"""
    def __init__(self, content, mtype, rgb, rect, page):
        self.rect = rect
        self.page = page
        self.content = content
        self.rgb = rgb
        self.mtype = mtype
    def __cmp__(a, b):
        if a.page < b.page:
            return -1
        elif a.page > b.page:
            return 1
        elif a.rect[1] > b.rect[1]:
            return -1
        elif a.rect[1] < b.rect[1]:
            return 1
        elif a.rect[3] > b.rect[3]:
            return -1
        elif a.rect[3] < b.rect[3]:
            return 1
        elif a.rect[0] < b.rect[0]:
            return -1
        else: 
            return 1
    def __hash__(self):
        '''docstring for __hash__''' 
        return hash((self.mtype, self.rgb))

class WebCmdHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """ handle command from web browser"""
    global target_pdf
    def do_POST(self):
        # command.................
        OPEN_PDF = "OPEN_PDF"
        NEXT = "NEXT" 
        PREVIOUS = "PREVIOUS" 
        ANNOTS_TYPE = "ANNOTS_TYPE" 
        SPEC_ANNOTS = "SPEC_ANNOTS"
        GET_PAGE = "GET_PAGE"
        # ......................
        """Handle a post request by returning the square of the number."""
        length = int(self.headers.getheader('content-length'))        
        xml = self.rfile.read(length)
        root = ElementTree.fromstring(xml)

        xml_cmd = root.find("command")
        attr =  xml_cmd.attrib
        cmd =  attr['name']
        print "**********************************************************" 
        if cmd == OPEN_PDF:
           filename = xml_cmd.find("filename").text
           print "receive < OPEN_PDF > command with argument: " + filename
           pdf.open_file(filename)
        elif cmd == PREVIOUS:
            print "receive < PREVIOUS > command"
        elif cmd == NEXT:
            print "receive < NEXT > command"
        elif cmd == ANNOTS_TYPE:
            print "receive < ANNOTS_TYPE >"
            print pdf.get_annot_types()
        elif cmd == SPEC_ANNOTS:
            print "receive <SPEC_ANNOTS> command with arguments:" + xml_cmd.find("spec_annots").text
        elif cmd == GET_PAGE:
            page = xml_cmd.find('page').text
            print "receive <GET_PAGE> command with argument" + page
        elif cmd == "TARGET_PDF":
            print "receive <TARGET_PDF> command" 
            print target_pdf
            self.wfile.write(target_pdf)
        elif cmd == "Annots":
            print "receive <Annots>"
            SEPANNOT = "%AnNot!"
            SEPITEM = "%ItEm!"
            annots_str = xml_cmd.find("data").text.split(SEPANNOT)
            # content, type, rgb, rect(minX, minY, maxX, *maxY), page
            annots = []
            for annot in annots_str:
                items = annot.strip(' ').split(SEPITEM)
                if len(items) == 5:
                    rect =  tuple(float(v) for v in items[3].split(','))
                    rgb = tuple(float(v) for v in items[2].split(','))
                    rgb = tuple(str(v*100)+'%'  for v in rgb)
                    # rgb tuple (int, int, int)
                    rgb = webcolors.rgb_percent_to_rgb(rgb)
                    # minx < maxx, miny < maxy
                    assert rect[0] < rect[2] and rect[1] < rect[3]
                    a = AnnotStruct(items[0].encode('utf-8'), items[1], rgb, rect,
                            int(items[4]))
                    annots.append(a)
            # sort annotations according to page index etc.
            annots.sort()
            # map the annot to the losest annotation configured 
            for annot in annots:
                annot.rgb = pdf_annot_to_sys_annot(annot)[1]
            fname = util.path_fname(target_pdf)[1].rstrip('.pdf')
            annots2mindmap(annots, fname + ".xmind")
            # write  to ".annot" file
            f = open(fname + ".annot" , 'w')
            print "write to file:", fname
            for annot in annots:
                print >> f, "**************************************************" 
                print >> f, annot.content
                #print "**************************************************" 
                #print annot.content
                annot_types.add((annot.mtype, annot.rgb))
            self.wfile.write("to browser")
            #print "************annotations types:*************" 
            #print annot_types
            print "Done!" 
        else:
            print "error:Unknown Command." 

        # excute command
        #rst_from_cpp = proxy.pdfserver(cmd_to_cpp );
        #if(cmd == SPEC_ANNOTS):
            ## well-formed purpose
            #str_xml = rst_from_cpp.data.decode('utf-8','replace').encode('utf-8')
            #str_xml = str_xml.replace('?',"ff")
            ##haiyou cong cpp cong pdf ti qu de shi hou jiu shi zhen le#
            #str_xml.replace(" ","&nbsp;")
            #self.wfile.write(str_xml)
        #else:
            ## push result to browser


def open_browser( ):
    """Start a browser after waiting for half a second during which
    the web sever is started."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, WEB_ANNOT_FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the web server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, WebCmdHandler)
    server.serve_forever()

def pdf_from_poppler(fname):
    ''' open pdf file with poppler interface''' 
    pdf.open_file(fname);
    types = pdf.get_annot_types();
    print "***************annotation types**********" 
    print types
    print "***************annotation contents**********" 
    # find potential encoding
    contents = []
    for item in pdf.get_spec_annots(types):
        #str_xml = item._content.decode('utf-8').encode('utf-8')
        #str_xml = str_xml.replace('?',"ff")
        if len(item._content):
            contents.append(item._content)
    #code = possible_encode(contents)
    #unicode2(contents)
    # print result
    #for content in contents:
        #print content.decode(code).encode('utf-8')
        #print "********************************************" 

def pdf_from_web(fname):
    open_browser()
    global PDF_DIRECTORY
    global target_pdf
    target_pdf = PDF_DIRECTORY + fname
    start_server()


def pdf_annot_to_sys_annot(pdf_annot):
    '''map annotations of pdf file to 
       annotations configured.
    ''' 
    color_dist = 100000
    annot = None
    for i,sys_annot in enumerate(tr_rgbs):
        if sys_annot[0] == pdf_annot.mtype:
            t = util.color_distance(sys_annot[1], pdf_annot.rgb)
            if t < color_dist:
                color_dist = t
                annot = sys_annot

    for i,sys_annot in enumerate(key_rgbs):
        if sys_annot[0] == pdf_annot.mtype:
            t = util.color_distance(sys_annot[1], pdf_annot.rgb)
            if t < color_dist:
                color_dist = t
                annot = sys_annot
    assert annot != None
    return annot

        # code...


#def open_pdf(fname):
    #pdf.open_file(fname);
    #types = pdf.get_annot_types();
    #for item in pdf.get_spec_annots(types):
        ##str_xml = item._content.decode('utf-8','replace')
        ##str_xml = str_xml.replace('?',"ff")

        ## decide the config color
        #rgb = webcolors.hex_to_rgb(item._color)
        #luv = util.rgb2luv(rgb[0], rgb[1], rgb[2])
        ## find the closest color



    print "***************************************" 
from pprint import pprint
def read_config(fname = "notemap.conf"):
    '''docstring for read_config''' 
    cf = ConfigParser.ConfigParser()
    cf.read(fname)
    #secs = cf.sections()
    TREE_RGB = "sematic_tree_rgb" 
    KEY_RGB = "key_rgb"
    global color_map
    print "***loading configure file: '%s'**********" % fname
    for opt in cf.options(TREE_RGB):
        temp = cf.get(TREE_RGB, opt)
        if temp.find('#') == -1:
            rgb = tuple(int(v) for v in re.findall("[0-9]+", temp))
            prev_rgb = rgb
            t = re.findall("[a-zA-Z]+",temp)[0]
            tr_rgbs.append((t,rgb))
        elif temp.find('#') != -1:
            color_map[prev_rgb] = temp

        #print opt,":", (t,rgb)
    for opt in cf.options(KEY_RGB):
        temp = cf.get(KEY_RGB, opt)
        if temp.find('#') == -1:
            rgb = tuple(int(v) for v in re.findall("[0-9]+", temp))
            prev_rgb = rgb
            t = re.findall("[a-zA-Z]+",temp)[0]
            key_rgbs.append((t,rgb))
        elif temp.find('#') != -1:
            color_map[prev_rgb] = temp
        #print opt,":", (t,rgb)

    print "tr_rgbs:" 
    pprint(tr_rgbs)
    print "key_rgbs:" 
    pprint(key_rgbs)
    print "color_map:" 
    pprint(color_map)
    assert len(color_map) > 0 and len(tr_rgbs) > 0 and len(key_rgbs) > 0
    print "***************************************" 

def is_parent_level(a, b):
    '''return the level of annotation in the mindmap,
       the root has the smallest level
    ''' 
    def level(arg):
        '''docstring for level''' 
        for i,annot in enumerate(tr_rgbs):
            if arg == annot:
               return i 
        # key rgbs
        return 10000
    return level(a) < level(b)
        

def annots2mindmap( annots, fname, root = ""):
    '''save pdf annotations list to xmind file''' 
    if root:
        root_name = root
    else:
        root_name = fname.rstrip(".xmind")
    mmap = mindmap.MindMap(root_name)
    stack = []
    #import ipdb
    #ipdb.set_trace()
    global color_map
    assert len(color_map) > 0
    
    for annot in annots:
        annot_type = (annot.mtype, annot.rgb)
        style = mmap.create_topic_style(fill = color_map[annot.rgb])
        if not stack:
            h = mmap.add_subtopic(mmap.root, format_content(annot.content.decode('utf-8')), style)
            if annot_type in tr_rgbs:
                stack.append((h, annot_type))
        else:
            for i,v in reversed(list(enumerate(stack))):
                if is_parent_level(v[1], annot_type):
                    h = mmap.add_subtopic(v[0], format_content(annot.content.decode('utf-8')), style)
                    if annot_type in tr_rgbs:
                        stack.append((h, annot_type))
                    break
                elif annot_type in tr_rgbs:
                    stack.pop()
                    if not stack:
                        h = mmap.add_subtopic(mmap.root, format_content(annot.content.decode('utf-8')), style)
                        stack.append((h, annot_type))
                        break
    mmap.save(fname)
    mindmap2txt(mmap, fname.rstrip(".xmind") + ".txt")
    return mmap

def mindmap2txt(mmap, fname):

    def visit_element(topic, level, f):
        '''docstring for visit_element''' 
        STEP = 2
        MARK = "*" 
        print topic.get_title()
        print >> f, MARK*level*STEP + \
                 format_content(topic.get_title()).encode('utf-8').replace('\n', '\n'+' '*level*STEP )
        for t in topic.get_subtopics():
           visit_element(t, level+1, f) 
        

    f = open(fname, "w")

    visit_element(mmap.root,0, f)

def format_content(content, LENGTH = 50, TOLERATION = 5):
    '''docstring for format_content''' 
    TOLERATION = LENGTH/10
    c_list = content.split(u'\n')
    l_list = []
    for line in c_list:
        b = 0
        e = LENGTH
        num = 0
        while True:
            t = line[b:e]
            if t:
                l_list.append(t)
                num += 1
            else:
                break
            b = e
            e = b + LENGTH
            if num >=2 and len(l_list[-1]) < TOLERATION:
                temp = l_list.pop()
                l_list[-1] += temp
    return u'\n'.join(l_list)


import argparse
if __name__ == "__main__":
    parser =  argparse.ArgumentParser(description = 'Process some integers.')
    parser.add_argument('f', help = 'an integer for the accumulator')
    args = parser.parse_args()
    read_config("notemap.conf")
    print color_map
    #load_test_pdf("test.pdf")
    pdf_from_web(args.f)
