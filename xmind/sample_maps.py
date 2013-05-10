# -*- coding: utf-8 -*-
# (c) 2008, Marcin Kasperski

"""
Zbiór funkcji generujących pliki służące do testów. Funkcje są normalnie używane
przy testach regresywnych (różne unittesty w tym katalogu) ale mogą też służyć do
ich inicjalnego utworzenia.

Każdy zwraca obiekt Document gotowy do zapisu.
"""

from mekk.xmind import XMindDocument

def generate_simple():
    doc = XMindDocument.create(u"root_topic_name", u"Projekty")
    sheet = doc.get_first_sheet()
    root = sheet.get_root_topic()
    root.set_note("View the Help sheet for info\nwhat you can do with this map")

    # (file = "", doc = "", shape = , line_color = "", line_width = "1pt" )
    #SHAPE_RECTANGLE
    #SHAPE_ROUND_RECTANGLE
    #SHAPE_ELLIPSIS
    style = doc.create_topic_style(fill = "#37D02B")
    #style_sub = doc.create_topic_style(fill = "CCCCCC")

    for i in range(1,5):
        topic = root.add_subtopic(u"Elemiątko %d" % i, "b%d" % i)
        topic.set_label("%d" % i)
        topic.set_style(style)
        topic.add_subtopic(u"Załączony").set_attachment( file("map_creator.py").read(), ".txt")
        topic.set_link("file:/home/wondereamer/3.png")
        for j in range(1,3):
            subtopic = topic.add_subtopic(u"Subelemiątko %d/%d" % (i,j),
                                          u"a%da%d" % (i,j))
            subtopic.add_marker("task-start")
            if j < 2:
                subtopic.add_marker("other-people")

    legend = sheet.get_legend()
    legend.add_marker("task-start", u"Dzień dobry")
    legend.add_marker("other-people", u"Do widzenia")

    return doc


def parse_and_print(file_name):
    xmind = XMindDocument.open(file_name)

    sheet = xmind.get_first_sheet()
    print "Sheet title: ", sheet.get_title()

    root = sheet.get_root_topic()
    print "Root title: ", root.get_title()
    print "Root note: ", root.get_note()

    for topic in root.get_subtopics():
        print "* ", topic.get_title()
        print "   label: ", topic.get_label()
        print "   link: ", topic.get_link()
        print "   markers: ", list(topic.get_markers())

if __name__ == "__main__":
    generate_simple().save("simple.xmind")
    parse_and_print("simple.xmind")
