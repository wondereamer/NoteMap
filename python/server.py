import threading
import webbrowser
import subprocess
import BaseHTTPServer
import SimpleHTTPServer
#import pdfviewer as pdf
import ConfigParser 
import webcolors
import re
import util
import mindmap

#import subprocess
from xml.etree import ElementTree
WEB_ANNOT_FILE = 'web/annotations.html'
PORT = 8080
HOME = 'http://localhost:%s/' % PORT
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
import urllib
class WebCmdHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """ handle command from web browser"""
    global target_pdf
    def do_GET(self):
        #'''docstring for do_GET''' 
        ##length = int(self.headers.getheader('content-length'))        
        ##str2 = self.rfile.read(length)
        ##print str2
        (path,fname) = util.path_fname(self.path)
        if fname.find('.html') != -1 or fname.find('.htm') != -1 or fname.find(".js") != -1:
            self.copyfile(urllib.urlopen("." + self.path), self.wfile)
        if path.find('.pdf') != -1:
            page = fname
            (path, fname) = util.path_fname(path)
            print "Open file: %s"% fname
            print "Page: %s"%page
            self.wfile.write("ok")
            subprocess.Popen(['xpdf',fname,page])
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
           #pdf.open_file(filename)
        elif cmd == PREVIOUS:
            print "receive < PREVIOUS > command"
        elif cmd == NEXT:
            print "receive < NEXT > command"
        elif cmd == ANNOTS_TYPE:
            print "receive < ANNOTS_TYPE >"
            #print pdf.get_annot_types()
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
            #f = open(fname + ".annot" , 'w')
            #print "save to file:", fname + ".txt" 
            #for annot in annots:
                #print >> f, "**************************************************" 
                #print >> f, annot.content
                ##print "**************************************************" 
                ##print annot.content
                #annot_types.add((annot.mtype, annot.rgb))
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
    """Start a browser after waiting for the web sever to be started."""
    def _open_browser():
        webbrowser.open(HOME + WEB_ANNOT_FILE)
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
    try:
        count = 0
        for opt in cf.options(TREE_RGB):
            # code...
            temp = cf.get(TREE_RGB, opt)
            if temp.find('#') == -1:
                rgb = tuple(int(v) for v in re.findall("[0-9]+", temp))
                prev_rgb = rgb
                t = re.findall("[a-zA-Z]+",temp)[0]
                tr_rgbs.append((t,rgb))
            elif temp.find('#') != -1:
                color_map[prev_rgb] = temp
                color_map[count] = temp
                count += 1
    except Exception, e:
        print e

    try:
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

    except Exception, e:
        print e

    print "tr_rgbs:" 
    pprint(tr_rgbs)
    print "key_rgbs:" 
    pprint(key_rgbs)
    print "color_map:" 
    pprint(color_map)
    #assert len(color_map) > 0 and len(tr_rgbs) > 0 and len(key_rgbs) > 0
    print "***************************************" 

def is_parent_level(a, b):
    '''return the level of annotation in the mindmap,
       the root has the smallest level
       a: annot
       b: annot
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
    '''save pdf annotations list to xmind file
    ''' 
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
            h = mmap.add_subtopic(mmap.root,
                                   format_content(util.my_decode(annot.content), style, 
                                   link = HOME + fname.rstrip(".xmind")+".pdf/"+
                                   str(annot.page)))
            if annot_type in tr_rgbs:
                stack.append((h, annot_type))
        else:
            for i,v in reversed(list(enumerate(stack))):
                if is_parent_level(v[1], annot_type):
                    h = mmap.add_subtopic(v[0],
                        format_content(util.my_decode(annot.content), style, 
                                      link = HOME +
                                      fname.rstrip(".xmind")+".pdf/"+
                                      str(annot.page)))
                    if annot_type in tr_rgbs:
                        stack.append((h, annot_type))
                    break
                elif annot_type in tr_rgbs:
                    stack.pop()
                    if not stack:
                        h = mmap.add_subtopic(mmap.root,
                            format_content(util.my_decode(annot.content),
                                              style, link = HOME +
                                              fname.rstrip(".xmind")+".pdf/"+
                                              str(annot.page)))
                        stack.append((h, annot_type))
                        break
    mmap.save(fname)
    mindmap2txt(mmap, fname.rstrip(".xmind") + ".txt")
    return mmap
def parse_args(suffix):
    '''docstring for parse_args''' 
    suffix = suffix.rstrip(" \n")
    if suffix.find("#") != -1:
        color = "#ff0000"
        page = suffix.split("#")[0]
    else:
        color = None
        page = suffix
    return (color, page)


def str2mindmap( annots_txt, fname, ENCODE = "utf-8"):
    '''save pdf annotations list to xmind file''' 
    uni_lines = []
    for annot in annots_txt:
        uni_lines.append(util.my_decode(annot))
    uni_lines.append(u'\t*end')
    mmap = mindmap.MindMap(annots_txt[0].rstrip(u'\n').lstrip(u'*'))
    stack = []
    global color_map
    # assert len(color_map) > 0
    temp = []
    for annot in uni_lines[1:]:
        if annot.lstrip(u'\t').startswith('*'):
            # get the topic content
            if len(temp) == 0:
                temp.append(annot)
                continue 
            level = len(temp[0]) - len(temp[0].lstrip(u'\t'))
            str_annot = temp[0].lstrip(u'\t*')
            item = str_annot.rsplit(u'**')
            str_annot = item[0]
            # parse  arguments
            color = None
            page = "" 
            if len(item) > 1:
                (color, page) = parse_args(item[1])
            for l in temp[1:]:
                str_annot += l.lstrip(u'\t')
            temp = []
            temp.append(annot)
            try:
                style = mmap.create_topic_style(fill = color if color else color_map[level])
            except KeyError:
                style = mmap.create_topic_style(fill = "#ffffff" )
            if not stack:
                h = mmap.add_subtopic(mmap.root, format_content(str_annot),
                        style, link = None if len(item) <= 1 else HOME+fname.rstrip(".xmind")+".pdf/"+page)
                stack.append((h,level))
            else:
                for i,v in reversed(list(enumerate(stack))):
                    if v[1] < level:
                        h = mmap.add_subtopic(v[0], format_content(str_annot),
                                style, link = None if page == ""  else HOME+fname.rstrip(".xmind")+".pdf/"+page)
                        stack.append((h, level))
                        break
                    else:
                        stack.pop()
                        if not stack:
                            h = mmap.add_subtopic(mmap.root, format_content(str_annot),
                                    style, link = None if page == ""  else HOME+fname.rstrip(".xmind")+".pdf/"+page)
                            stack.append((h, level))
                            break

        else:
            temp.append(annot)
    mmap.save(fname)
    #mindmap2txt(mmap, "t.txt")
    return mmap
def mindmap2txt(mmap, fname):
    STEP = 1
    MARK = "\t" 
    def visit_element(topic, level, f):
        '''docstring for visit_element''' 
        print >> f, MARK*level*STEP + '*' + \
                 format_content(topic.get_title()).encode('utf-8').replace('\n', '\n'+ MARK*level*STEP+' ')
        for t in topic.get_subtopics():
           visit_element(t, level+1, f) 
        

    f = open(fname, "w")
    print >> f, format_content(mmap.root.get_title()).encode('utf-8')
    for t in mmap.root.get_subtopics():
       visit_element(t, 0, f) 

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
    #pdf_from_web(args.f)
    str2mindmap(open(args.f,"r").readlines(), "%s.xmind" % args.f.split(".")[0])
# mekk.xmind
# chardet
# webcolors
