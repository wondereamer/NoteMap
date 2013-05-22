import threading
import webbrowser
import BaseHTTPServer
import SimpleHTTPServer
import pdfviewer as pdf
import ConfigParser 
import webcolors
import re
import util

#import subprocess
from xml.etree import ElementTree
#cpp_server = subprocess.Popen('./readPdf', cwd = './bin' )
#cpp_server.kill()
#time.sleep(1)
WEB_ANNOT_FILE = 'web/annotations.html'
PORT = 8080
target_pdf = "" 
PDF_DIRECTORY = "../" 

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
            annots.sort()
            # write 
            fname = util.path_fname(target_pdf)[1].rstrip('.pdf') + ".annot" 
            f = open(fname, 'w')
            print "write to file:", fname
            for annot in annots:
                print >> f, "**************************************************" 
                print >> f, annot.content
                print "**************************************************" 
                print annot.content
            self.wfile.write("to browser")
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
    #open_browser()
    global PDF_DIRECTORY
    global target_pdf
    target_pdf = PDF_DIRECTORY + fname
    start_server()

def open_pdf(fname):
    pdf.open_file(fname);
    types = pdf.get_annot_types();
    for item in pdf.get_spec_annots(types):
        #str_xml = item._content.decode('utf-8','replace')
        #str_xml = str_xml.replace('?',"ff")

        # decide the config color
        rgb = webcolors.hex_to_rgb(item._color)
        luv = util.rgb2luv(rgb[0], rgb[1], rgb[2])
        # find the closest color



    print "***************************************" 

def read_config(fname = "notemap.conf"):
    '''docstring for read_config''' 
    cf = ConfigParser.ConfigParser()
    cf.read(fname)
    #secs = cf.sections()
    TREE_RGB = "sematic_tree_rgb" 
    KEY_RGB = "key_rgb"
    tr_rgbs= []
    key_rgbs = []
    print "***loading configure file: '%s'**********" % fname
    for opt in cf.options(TREE_RGB):
        rgb = tuple(int(v) for v in re.findall("[0-9]+", cf.get(TREE_RGB, opt)))
        tr_rgbs.append(rgb)
        print opt, ":", rgb
    for opt in cf.options(KEY_RGB):
        rgb = tuple(int(v) for v in re.findall("[0-9]+", cf.get(KEY_RGB, opt)))
        key_rgbs.append(rgb)
        print opt,":", rgb
    print "***************************************" 

if __name__ == "__main__":
    #read_config("notemap.conf")
    #load_test_pdf("test.pdf")
    pdf_from_web("test.pdf")
