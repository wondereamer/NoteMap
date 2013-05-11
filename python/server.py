import threading
import webbrowser
import BaseHTTPServer
import SimpleHTTPServer
import pdfviewer as pdf
import ConfigParser 
import webcolors
#import subprocess
from xml.etree import ElementTree
#cpp_server = subprocess.Popen('./readPdf', cwd = './bin' )
#cpp_server.kill()
#time.sleep(1)
FILE = './pdfviewer.html'
PORT = 8080

def rgb2luv(R, G, B):
    eps = 216.0 / 24389.0;
    k = 24389.0/27.0;
    Xr = 0.964221;
    Yr = 1.0;
    Zr = 0.825211;
    r = R/255.0; 
    g = G/255.0; 
    b = B/255.0;    
    if r <= 0.04045:
        r = r/12;
    else:
        r = ((r+0.055)/1.055) ** 2.4
    if g <= 0.04045:
        g = g/12;
    else:
        g = ((g+0.055)/1.055) ** 2.4

    if b <= 0.04045:
        b = b/12;
    else:
        b = ((b+0.055)/1.055) ** 2.4
    X =  0.436052025*r     + 0.385081593*g + 0.143087414 *b;
    Y =  0.222491598*r     + 0.71688606 *g + 0.060621486 *b;
    Z =  0.013929122*r     + 0.097097002*g + 0.71418547  *b;
    u_ = 4*X / (X + 15*Y + 3*Z);
    v_ = 9*Y / (X + 15*Y + 3*Z);		 
    ur_ = 4*Xr / (Xr + 15*Yr + 3*Zr);
    vr_ = 9*Yr / (Xr + 15*Yr + 3*Zr);
    yr = Y/Yr;
    if yr > eps:
        L =  116*pow(yr,float(1/3.0)) - 16;
    else:
        L = k * yr;
    u = 13*L*(u_ -ur_);
    v = 13*L*(v_ -vr_);
    return (int)(2.55*L + .5), (int) (u + .5), (int) (v + .5)       

class CmdHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """The test example handler."""
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
            #self.wfile.write(rst_from_cpp)


def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, CmdHandler)
    server.serve_forever()

def load_test_pdf(fname):
    '''docstring for load_test_pdfll''' 
    pdf.open_file(fname);
    types = pdf.get_annot_types();
    print "***************annotation types**********" 
    print types
    print "***************annotation contents**********" 
    for item in pdf.get_spec_annots(types):
        #str_xml = item._content.decode('utf-8').encode('utf-8')
        #str_xml = str_xml.replace('?',"ff")
        if len(item._content):
            print "^^^^^^^^^^" 
            print item._content
            #print item._color
            print "^^^^^^^^^^" 

def open_pdf(fname):
    pdf.open_file(fname);
    types = pdf.get_annot_types();
    for item in pdf.get_spec_annots(types):
        #str_xml = item._content.decode('utf-8','replace')
        #str_xml = str_xml.replace('?',"ff")

        # decide the config color
        rgb = webcolors.hex_to_rgb(item._color)
        luv = rgb2luv(rgb[0], rgb[1], rgb[2])
        # find the closest color



    print "***************************************" 

def read_config(fname = "notemap.conf"):
    '''docstring for read_config''' 
    cf = ConfigParser.ConfigParser()
    cf.read(fname)
    #secs = cf.sections()
    TREE_COLOR = "sematic_tree_color" 
    KEY_COLOR = "key_color"
    tr_colors= []
    key_colors = []
    print "***loading configure file: '%s'**********" % fname
    for opt in cf.options(TREE_COLOR):
        tr_colors.append(cf.get(TREE_COLOR, opt))
        print opt, ":", cf.get(TREE_COLOR, opt)
    for opt in cf.options(KEY_COLOR):
        key_colors.append(cf.get(KEY_COLOR, opt))
        print opt,":", cf.get(KEY_COLOR, opt)
    print "***************************************" 

if __name__ == "__main__":
    #open_browser()
    #start_server()
    read_config("notemap.conf")
    load_test_pdf("python.pdf")
