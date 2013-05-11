#include "pdf_document.h"

#include <QtGui/QApplication>
#include <iostream>
#include <QtGui/QImage>
#include <QtGui/QMessageBox>
#include <QtGui/QLineEdit>
#include <QtGui>
#include <QDebug>
#include <QLinkedList>
#include <QPointF>
#include <QString>
#include <algorithm>
#include <cassert>
#include <set>
const int AText = 1;
const int ALine = 2;
const int MAX_SAMPLE = 30;                      //!< the number of annotations to estimate _text_height
//using namespace IdeaNet;
//Pdf_Document::Pdf_Document():_dpiX(QApplication::desktop()->physicalDpiX()),
//    _dpiY(QApplication::desktop()->physicalDpiY()),
//    _zoom(1.5),_doc(0),_text_height(0)

Pdf_Document::Pdf_Document()
{
    init_type_map();
}

void Pdf_Document::init_type_map()
{

    std::pair<std::string, Poppler::Annotation::SubType> v;
    v.first = "AText";
    v.second = Poppler::Annotation::AText;
    _type_map.insert(v);

    v.first = "ALine";
    v.second = Poppler::Annotation::ALine;
    _type_map.insert(v);
    //Highlight
    v.first = "Highlight";
    v.second = Poppler::Annotation::AHighlight;
    _type_map.insert(v);
    v.first = "Underline";
    v.second = Poppler::Annotation::AHighlight;
    _type_map.insert(v);
    v.first = "Squiggly";
    v.second = Poppler::Annotation::AHighlight;
    _type_map.insert(v);
    // end of Highlight

    v.first = "AFileAttachment";
    v.second = Poppler::Annotation::AFileAttachment;
    _type_map.insert(v);
    v.first = "ASound";
    v.second = Poppler::Annotation::ASound;
    _type_map.insert(v);
    v.first = "AMovie";
    v.second = Poppler::Annotation::AMovie;
    _type_map.insert(v);
    v.first = "A_BASE";
    v.second = Poppler::Annotation::A_BASE;
    _type_map.insert(v);
    v.first = "AStamp";
    v.second = Poppler::Annotation::AStamp;
    _type_map.insert(v);
    v.first = "AInk";
    v.second = Poppler::Annotation::AInk;
    _type_map.insert(v);
    v.first = "ALink";
    v.second = Poppler::Annotation::ALink;
    _type_map.insert(v);
    v.first = "ACaret";
    v.second = Poppler::Annotation::ACaret;
    _type_map.insert(v);
    v.first = "AGeom";
    v.second = Poppler::Annotation::AGeom;
    _type_map.insert(v);


    std::pair<std::string, Poppler::HighlightAnnotation::HighlightType> vv;
    vv.first = "Highlight";
    vv.second = Poppler::HighlightAnnotation::Highlight;
    _hl_subtype_map.insert(vv);

    vv.first = "Squiggly";
    vv.second = Poppler::HighlightAnnotation::Squiggly;
    _hl_subtype_map.insert(vv);

    vv.first = "Underline";
    vv.second = Poppler::HighlightAnnotation::Underline;
    _hl_subtype_map.insert(vv);
}
QImage Pdf_Document::get_page(int page)
{
    Poppler::Page *popplerPage = _doc->page(page);
    const double resX = _dpiX * _zoom;
    const double resY = _dpiY * _zoom;
    QImage image = popplerPage->renderToImage(800, 1200);
    set_curPage(page);
    delete popplerPage;
    return image;
}

QImage Pdf_Document::reload_page()
{
    return get_page(_curPage);
}

bool Pdf_Document::load_document(const std::string &file)
{
    _unique_annots.clear();
    _curPage = 0;
    if (_doc) {
        delete _doc;
    }
    _doc = Poppler::Document::load(QString(file.c_str()));
    if (!_doc) {
        qDebug()<<"Failed to open file!";
        return false;
    }

    //    while (_doc->isLocked()) {
    //	bool ok = true;
    //	std::string password = QInputDialog::getText(0, "Document Password",
    //		"Please insert the password of the document:",
    //		QLineEdit::Password, std::string(), &ok);
    //	if (!ok) {
    //	    delete _doc;
    //	    return false;
    //	}
    //	_doc->unlock(password.toLatin1(), password.toLatin1());
    //    }

    _doc->setRenderHint(Poppler::Document::TextAntialiasing, true);
    _doc->setRenderHint(Poppler::Document::Antialiasing, true);
    _doc->setRenderBackend((Poppler::Document::RenderBackend)0);
    return true;

}



std::set<Pdf_Document::Annot> Pdf_Document::get_annots_type( )
{
    assert(_doc);
    int num = _doc->numPages();
    //    int max_sample = MAX_SAMPLE;
    bool per_page_flag = false;
    //    std::multiset<qreal> height_set;
    _unique_annots.clear();
    for (int index = 0; index < num; index++) {
        Poppler::Page *popplerPage = _doc->page(index);
        per_page_flag = true;                   // make sure to sample an annotation per page 
        QList< Poppler::Annotation* > annots = popplerPage->annotations();
        _page_size = popplerPage->pageSize();
        foreach(Poppler::Annotation *annot, annots){
            Pdf_Document::Annot unique_annot;
            switch(annot->subType()) {
                case Poppler::Annotation::AText:
                    //			_unique_annots.insert(unique_annot);
                    break;
                case Poppler::Annotation::ALine:
                    //			_unique_annots.insert(unique_annot);
                    break;
                case Poppler::Annotation::AHighlight:{
                     Poppler::HighlightAnnotation *hlannt = dynamic_cast<Poppler::HighlightAnnotation*>(annot);
                     //		    // calcuate _text_height
                     //		    if( per_page_flag && max_sample-- > 0 ){
                     //			QList<Poppler::HighlightAnnotation::Quad> quads = hlannt->highlightQuads();
                     //			Poppler::HighlightAnnotation::Quad quad = quads[0];
                     //			qreal height = quad.points[3].y() - quad.points[0].y();
                     //			height_set.insert(height);
                     //		    }
                     QColor anncol = hlannt->style.color;
                     std::string color = anncol.name().toStdString();
                     unique_annot.second = color;
                     switch(hlannt->highlightType()) {
                         case Poppler::HighlightAnnotation::Highlight:
                             unique_annot.first = "Highlight";
                             break;
                         case Poppler::HighlightAnnotation::Squiggly:
                             unique_annot.first = "Squiggly";
                             break;
                         case Poppler::HighlightAnnotation::Underline:
                             unique_annot.first = "Underline";
                             break;
                         default:
                             unique_annot.first = "Unknown" ;
                     }

                     _unique_annots.insert(unique_annot);
                     break; }//end of AHighlight
                default:
                                                     ;
            }//end of subType() switch
            per_page_flag = false;
        }// end of annots iterate loop

        delete popplerPage;
    }// end of page interate loop
    //    if (height_set.size() > 0) {
    //	std::multiset<qreal>::iterator i = height_set.begin();
    //	for (int j = 0; j < height_set.size()/2; j++) {
    //		i++;
    //	}
    //	_text_height = *i;

    //    }
    return _unique_annots;
}

std::vector<AnnotStruct> Pdf_Document::get_spec_annots(const std::set<Annot> &unique_annots)
{
    assert(_doc);
    std::string result;
    int num = _doc->numPages();
    std::vector<AnnotStruct> annotStructS;
    // iterate all pages
    for (int index = 0; index < num; index++) {
        Poppler::Page *popplerPage = _doc->page(index);
        _page_size = popplerPage->pageSize();
        QList< Poppler::Annotation* > annots = popplerPage->annotations();
        std::string content;
        // iterate all annotations in one page
        foreach(Poppler::Annotation *annot, annots){
            AnnotStruct annotStruct;
            std::string annot_type;
            std::string annot_color;
            QPointF pos;
            std::set<Annot>::const_iterator iterator = unique_annots.begin();
            std::string color = annot->style.color.name().toStdString();
            // check if the annot is required type
            for (; iterator != unique_annots.end(); iterator++) {
                if(annot->subType() == _type_map[iterator->first]
                        && color == iterator->second){
                    annot_type = iterator->first;
                    annot_color = iterator->second;
                    break;
                }
            }
            if (annot_type.size()) {
                //the annot is required
                switch(annot->subType()) {
                    case Poppler::Annotation::AText:
                        break;
                    case Poppler::Annotation::ALine:{
                        Poppler::LineAnnotation *line_annt = dynamic_cast<Poppler::LineAnnotation*>(annot);
                        QLinkedList<QPointF> p = line_annt->linePoints();
                        const double resX = _dpiX * _zoom * 1;
                        const double resY = _dpiY * _zoom * 1;
                        QPointF a = p.takeFirst();
                        QPointF b = p.takeLast();
                        //			qDebug()<<"***********************"<<index;
                        //			qDebug()<<line_annt->lineInnerColor()<<a<<b;
                        //		    qDebug()<<popplerPage->text(QRectF(a.x(),792-a.y()-13,200,50));
                        //		    qDebug()<<popplerPage->text(QRectF(0,0,400,500));
                        //		    qDebug()<<resX<<resY;
                        //		    QImage image = popplerPage->renderToImage(resX, resY);
                        //		    image.save("line.png");
                        break; }
                    case Poppler::Annotation::AHighlight:{
                         Poppler::HighlightAnnotation *hlannt = dynamic_cast<Poppler::HighlightAnnotation*>(annot);
                         // get the right Highlight subtype
                         Poppler::HighlightAnnotation::HighlightType sub_type = _hl_subtype_map[annot_type];
                         // check the hightlight subtype
                         // Highlight, Underline, or Squiggly
                         if (hlannt->highlightType() == sub_type) {
//                             content += "<![CDATA[ ]]>";
                             QList<Poppler::HighlightAnnotation::Quad> quads = hlannt->highlightQuads();
                             Poppler::HighlightAnnotation::Quad pre_annot = quads[0];
                             // find the begining of segment
                             float minX = 10000000; 
                             float maxX = -10000000; 
                             foreach(Poppler::HighlightAnnotation::Quad quad, quads)
                                if(quad.points[0].x() < minX)
                                    minX = quad.points[0].x();
                                else if(quad.points[3].x() > maxX)
                                    maxX = quad.points[3].x();

                             // for each piece of Highlight mark
                             foreach(Poppler::HighlightAnnotation::Quad quad, quads){
                                 //up down
                                 quad.points[0].setY(_page_size.height() - quad.points[0].y());
                                 quad.points[3].setY(_page_size.height() - quad.points[3].y());
                                 QRectF textBox(quad.points[0],quad.points[3]);
                                 pos.rx() = quad.points[0].x();
                                 pos.ry() = quad.points[0].y();
                                 // deal with different piece
                                 if(pre_annot.points[0].y() != quad.points[0].y())
                                     if(quad.points[0].x() == minX ||
                                         pre_annot.points[3].x() > minX + (maxX - minX)/2)
                                         content += " ";
                                     else
                                         content += "\n";
                                 else 
                                     qDebug()<<"Warning: Find two seperate pieces in page"<<index+1<<"!";
//                                 if(quad.points[0].x() > minX)
//                                     qDebug()<<quad.points[0].x() - minX;
                                 content.append(popplerPage->text(textBox).toStdString());
                                 pre_annot = quad;
                             }

                         }
                         break; }//end of AHighlight
                    default: ;
                }//end of subType() switch

            }

            /// @todo ff '  luan ma
            if (content.size()) {
                annotStruct._type = annot_type;
                annotStruct._color = annot_color;
                annotStruct._page = index + 1;
                annotStruct._content = content;
                annotStruct._x = pos.x();
                annotStruct._y = pos.y();
                content.clear();
                annotStructS.push_back(annotStruct);

            }
        }// end of annots iterate loop
        delete popplerPage;
    }// end of page interate loop
    //
    std::sort(annotStructS.begin(), annotStructS.end());
    return annotStructS;
}


//void Pdf_Document::display_merge(Poppler::Page *page, int index)
//{
////    qDebug()<<_spec_hl_boxs.size();
//    assert(page);
//    if(_spec_hl_boxs.empty())
//	return;
//    std::vector< QRectF >::iterator i;
//    int no_segment = 0;
//    for( i = _spec_hl_boxs.begin(); i != _spec_hl_boxs.end(); ){
//
//	no_segment++;
//	std::vector< QRectF >::iterator pre;
//	QRectF segment(*i);
//	while (pre = i, ++i != _spec_hl_boxs.end() && display_mergeble(*pre,*i)) {
//		merge_box(segment,*i);
//	}
//	// have found a maxmum mergeble segment
//	segment.setLeft(0);
//	segment.setRight(_page_size.width());
//	qDebug()<<"**********************";
//	qDebug()<<page->text(segment);
//	    //render to image
//    }
//
//}

//bool Pdf_Document::display_mergeble(const QRectF &a, const QRectF &b)
//{
//    if (b.top() - a.bottom() <= _text_height) {
//	return true;
//    }
//    return false;
//}

//void Pdf_Document::merge_box( QRectF &a, const QRectF &b)
//{
//    a = a.united(b);
//}
