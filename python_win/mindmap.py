from mekk.xmind import XMindDocument
class MindMap(object):
    """docstring for MindMap"""
    def __init__(self, root_name):
        self.doc = XMindDocument.create(u"first sheet name", root_name)
        self.sheet = self.doc.get_first_sheet()
        self.root = self.sheet.get_root_topic()

    def add_subtopic(self, parent, content, style, link = None, 
                        attachment = None, label = None, marker = None):
        '''parent: parent topic
           content: the content
        ''' 
        topic = parent.add_subtopic(content)
        topic.set_style(style)
        if link:
           topic.set_link(link)
        if attachment:
           topic.set_attachment(file(attachment[0]).read(), attachment[1]) 
        if label:
           topic.set_label(label)
        if marker:
           topic.add_marker(marker)
        return topic

    def create_topic_style(self, *args, **kwargs):
        return self.doc.create_topic_style(*args, **kwargs)

    def add_sheet_marker(self, marker, content):
        legend = self.sheet.get_legend()
        legend.add_marker(marker, content)

    def save(self, fname):
        self.doc.save(fname)

    
if __name__ == '__main__':
    mmap = MindMap("test")
    style = mmap.create_topic_style(fill = "#37D02B")
    r = mmap.add_subtopic(mmap.root, "hello", style)
    t = mmap.add_subtopic(mmap.root, "world", style)
    mmap.add_subtopic(r, "nihao", style)
    mmap.save("test_mindmapper.xmind")
