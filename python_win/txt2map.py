# -*- coding: utf8 -*-
import threading
import webbrowser
import subprocess
#import pdfviewer as pdf
import ConfigParser 
import re
import util
import mindmap
import webcolors

#import subprocess
WEB_ANNOT_FILE = 'web/annotations.html'
PORT = 8080
HOME = 'http://localhost:%s/' % PORT
# annotation types found in configure file
tr_rgbs= []
key_rgbs = []
# annotation types found in the target pdf
annot_types = set()
color_map = { }
#if path.find('.pdf') != -1:
    #page = fname
    #(path, fname) = util.path_fname(path)
    #print "Open file: %s"% fname
    #print "Page: %s"%page
    #self.wfile.write("ok")
    #subprocess.Popen(['xpdf',fname,page])


def open_browser( ):
    """Start a browser after waiting for the web sever to be started."""
    def _open_browser():
        webbrowser.open(HOME + WEB_ANNOT_FILE)
    thread = threading.Timer(0.5, _open_browser)
    thread.start()



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


def parse_args(suffix):
    """ 解析颜色和页面参数 """
    suffix = suffix.rstrip(" \n")
    if suffix.find("#") != -1:
        #color = "#ff0000"
        #color = webcolors.name_to_hex("blue")
        m = suffix.split("#")
        color = webcolors.name_to_hex(m[1]) if len(m)>1 else m[0]
        page = m[0] if len(m) > 1 else ''
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
    rootname = annots_txt[0].rstrip(u'\n').lstrip(u'*')
    mmap = mindmap.MindMap(rootname)
    stack = []
    global color_map
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
                url = HOME+fname.rstrip(".xmind")+".pdf/"+page
            for l in temp[1:]:
                str_annot += l.lstrip(u'\t')
            temp = []
            temp.append(annot)
            try:
                style = mmap.create_topic_style(fill = color if color else color_map[level])
            except KeyError:
                # 默认红色
                style = mmap.create_topic_style(fill = "#ffffff" )
            if not stack:
                h = mmap.add_subtopic(mmap.root, format_content(str_annot),
                        style, link = url if len(item)>1 and page else None)
                stack.append((h,level))
            else:
                for i,v in reversed(list(enumerate(stack))):
                    if v[1] < level:
                        h = mmap.add_subtopic(v[0], format_content(str_annot),
                                style, link = None if page == ""  else url)
                        stack.append((h, level))
                        break
                    else:
                        stack.pop()
                        if not stack:
                            h = mmap.add_subtopic(mmap.root, format_content(str_annot),
                                    style, link = None if page == ""  else url)
                            stack.append((h, level))
                            break

        else:
            temp.append(annot)
    mmap.save(fname)
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
    #TOLERATION = LENGTH/10
    #c_list = content.split(u'\n')
    #l_list = []
    #for line in c_list:
        #b = 0
        #e = LENGTH
        #num = 0
        #while True:
            #t = line[b:e]
            #if t:
                #l_list.append(t)
                #num += 1
            #else:
                #break
            #b = e
            #e = b + LENGTH
            #if num >=2 and len(l_list[-1]) < TOLERATION:
                ## 处理PDF中可能出现的截断
                #temp = l_list.pop()
                #l_list[-1] += temp
    #return u'\n'.join(l_list)
    return content


if __name__ == "__main__":
    str2mindmap(open('test2.txt', "r").readlines(), "trend2.xmind")

# mekk.xmind
# chardet
# webcolors
