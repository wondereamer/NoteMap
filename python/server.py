import threading
import webbrowser
import BaseHTTPServer
import SimpleHTTPServer
import xmlrpclib
import subprocess
from xml.etree import ElementTree
import time
cpp_server = subprocess.Popen('./readPdf', cwd = './bin' )
#cpp_server.kill()
time.sleep(1)
FILE = './pdfviewer.html'
PORT = 8080
# command.................
OPEN_PDF = "OPEN_PDF"
NEXT = "NEXT" 
PREVIOUS = "PREVIOUS" 
ANNOTS_TYPE = "ANNOTS_TYPE" 
SPEC_ANNOTS = "SPEC_ANNOTS"
GET_PAGE = "GET_PAGE"
# ......................
proxy =  xmlrpclib.ServerProxy("http://localhost:3344/")
class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """The test example handler."""
    def do_POST(self):
        """Handle a post request by returning the square of the number."""
        length = int(self.headers.getheader('content-length'))        
        xml = self.rfile.read(length)
        root = ElementTree.fromstring(xml)
	xml_cmd = root.find("command")
	attr =  xml_cmd.attrib
	cmd =  attr['name']
	#
	print "*************************************" 
	print "received command from browser:" + cmd
	rst_from_cpp = "";
	cmd_to_cpp = "" ;
	if cmd == OPEN_PDF:
	    filename = xml_cmd.find("filename").text
	    cmd_to_cpp = {"command":OPEN_PDF,"arg1":filename }
	    print "send < OPEN_PDF > command to cpp server:" + filename
	elif cmd == PREVIOUS:
	    cmd_to_cpp = {"command":PREVIOUS}
	    print "send < PREVIOUS > command to cpp server:"
	elif cmd == NEXT:
	    cmd_to_cpp = {"command":NEXT}
	    print "send < NEXT > command to cpp server:"
	elif cmd == ANNOTS_TYPE:
	    cmd_to_cpp = {"command":ANNOTS_TYPE}
	    print "send < ANNOTS_TYPE > command to cpp server:"
	elif cmd == SPEC_ANNOTS:
	    spec_annots = xml_cmd.find("spec_annots").text
	    print "arguments:"
	    cmd_to_cpp = {"command":SPEC_ANNOTS,"arg1":spec_annots}
	    print "send < SPEC_ANNOTS > command to cpp server:"
	elif cmd == GET_PAGE:
	    page = xml_cmd.find('page').text
	    cmd_to_cpp = {"command":GET_PAGE,"arg1":page }
	    print "send <GET_PAGE> command to cpp server:" + page
	else:
	    print "error:Unknown Command." 

	# excute command
	rst_from_cpp = proxy.pdfserver(cmd_to_cpp );
	if(cmd == SPEC_ANNOTS):
	    # well-formed purpose
	    str_xml = rst_from_cpp.data.decode('utf-8','replace').encode('utf-8')
	    str_xml = str_xml.replace('?',"ff")
	    #haiyou cong cpp cong pdf ti qu de shi hou jiu shi zhen le#
	    str_xml.replace(" ","&nbsp;")
	    self.wfile.write(str_xml)
	else:
	    # push result to browser
	    self.wfile.write(rst_from_cpp)


def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    #send data to readpdf server
    #working as http server
    open_browser()
    start_server()

