/*
 * Copyright (C) 2008, Pino Toscano <pino@kde.org>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street - Fifth Floor, Boston, MA 02110-1301, USA.
 */

#include "pdf_document.h"
#include "using.h"
#include <string>
#include <QtGui/QApplication>
#include <QDebug>
#include <iostream>
#include <QDir>
#include <QString>
using std::string;

QString FILENAME_PNG = "temp_%1.png";  //relate to cpp server
QString CPP_RELATIVE_TO_HTML = "./bin/";
QString TEMP_PDF_PNG_PATH = CPP_RELATIVE_TO_HTML + FILENAME_PNG;// relate to html document
//using namespace IdeaNet;
using namespace std;
char* argv2[1]={ "name" };
int argc = 1;
//QApplication app(argc, argv2);
Pdf_Document document;
typedef std::pair<std::string, std::string> Annot;
typedef std::set<Annot> AnnotSet;
string open_file(const string &fname)
{
    if (fname.size() > 0 && document.load_document(QString(fname.c_str()))) {
        QString xml;
        xml += "<root>";
        xml += "<path>";
        xml += TEMP_PDF_PNG_PATH.arg(0);
        xml += "</path>";
        xml += "</root>";
        return xml.toStdString();
    }
}
std::string get_spec_annots(const AnnotSet &unique_annots)
{
    std::set<Pdf_Document::Annot> annots = document.get_annots_type();
    QString ret = document.get_spec_annots(annots);
 return ret.toStdString();
}
string annotations( )
{
    std::set<Pdf_Document::Annot> annots = document.get_annots_type();
    QString temp;
    QString xml;
    xml += "<root>" ;
    foreach(Pdf_Document::Annot annot, annots){
        QColor color(annot.second);
        xml += "<unique_annot>"; 
        xml += "<type>";
        xml += annot.first;
        xml += "</type>";
        xml += "<color>";
        xml += annot.second;
        xml += "</color>";
        xml += "<r>";
        xml += QString::number(color.red());
        xml += "</r>";
        xml += "<g>";
        xml += QString::number(color.green());
        xml += "</g>";
        xml += "<b>";
        xml += QString::number(color.blue());
        xml += "</b>";
        xml += "</unique_annot>";
    }
    xml += "</root>";
    return xml.toStdString();
}
string previous_page()
{

    int all = document.num_pages();
    int cur = document.get_curPage();
    QString xml;
    xml += "<root>";
    xml += "<path>";
    if (cur > 0) {
        QImage img = document.get_page(--cur);
        img.save(FILENAME_PNG.arg(cur));
        xml += TEMP_PDF_PNG_PATH.arg(cur);
    }
    xml += "</path>";
    xml += "</root>";
    return xml.toStdString();
}
string next_page()
{

    int all = document.num_pages();
    int cur = document.get_curPage();
    QString xml;
    xml += "<root>";
    xml += "<path>";
    if (cur < all - 2) {
        QImage img = document.get_page(++cur);
        img.save(FILENAME_PNG.arg(cur));
        xml += TEMP_PDF_PNG_PATH.arg(cur);
    }
    xml += "</path>";
    xml += "</root>";

    return xml.toStdString();

}
string get_page(const string &index)
{

    QString page(index.c_str());
    QString xml;
    xml += "<root>";
    xml += "<path>";
    QImage img = document.get_page(page.toInt() - 1);
    img.save(FILENAME_PNG.arg(page.toInt()));
    xml += TEMP_PDF_PNG_PATH.arg(page.toInt());
    xml += "</path>";
    xml += "</root>";
    return xml.toStdString();
}

