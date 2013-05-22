from chardet.universaldetector import UniversalDetector
import ntpath

def path_fname(path):
    '''
    return (parent_dir, filename), working for both linux and windows

    >>> paths =  ['a/b/c/', 'a/b/c']
    >>> [path_fname(path) for path in paths]
    [('a/b/', 'c'), ('a/b', 'c')]

     '''
    head, tail =  ntpath.split(path)
    if not tail:
        fname = ntpath.basename(head)
        parent = head.rstrip(fname)
        return parent, fname
    else:
        return head, tail


def unicode2(string):
    '''make unicode'''
    encodings = [ "ascii", "utf_8", "big5", "big5hkscs", "cp037", "cp424", "cp437", "cp500", "cp737", "cp775", "cp850", "cp852", "cp855", 
        "cp856", "cp857", "cp860", "cp861", "cp862", "cp863", "cp864", "cp865", "cp866", "cp869", "cp874", "cp875", "cp932", "cp949", 
        "cp950", "cp1006", "cp1026", "cp1140", "cp1250", "cp1251", "cp1252", "cp1253", "cp1254", "cp1255", "cp1256", "cp1257", "cp1258", 
        "euc_jp", "euc_jis_2004", "euc_jisx0213", "euc_kr", "gb2312", "gbk", "gb18030", "hz", "iso2022_jp", "iso2022_jp_1", "iso2022_jp_2", 
        "iso2022_jp_2004", "iso2022_jp_3", "iso2022_jp_ext", "iso2022_kr", "latin_1", "iso8859_2", "iso8859_3", "iso8859_4", "iso8859_5", 
        "iso8859_6", "iso8859_7", "iso8859_8", "iso8859_9", "iso8859_10", "iso8859_13", "iso8859_14", "iso8859_15", "johab", "koi8_r", "koi8_u", 
        "mac_cyrillic", "mac_greek", "mac_iceland", "mac_latin2", "mac_roman", "mac_turkish", "ptcp154", "shift_jis", "shift_jis_2004", 
        "shift_jisx0213", "utf_32", "utf_32_be", "utf_32_le", "utf_16",
        "utf_16_be", "utf_16_le", "utf_7", "utf_8_sig" ,"END"]
    for enc in encodings:
        try:
            utf8 = string.decode(enc)
            return utf8
        except Exception:
            if enc == encodings[-1]:
                print "can't find encoding" 

def possible_encode(strList, name='stdin'):
    """Return a string describing the probable encoding of a file."""
    u = UniversalDetector()
    for line in strList:
        u.feed(line)
    u.close()
    result = u.result
    if result['encoding']:
        return result['encoding']
    else:
        return '' 

def rgb2luv(R, G, B):
    ''' covert color from rgb space to luv space which could be compared based
    on the perception similarity  '''
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
