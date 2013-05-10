#ifndef PDF_DOCUMENT_h

#define PDF_DOCUMENT_h
#include <QString>
#include <poppler/qt4/poppler-qt4.h>
#include <QImage>
#include <set>
#include <QStringList>
#include <QRectF>
#include <QSize>
#include <cassert>
#include <map>
#include <vector>
#include <string>
//namespace IdeaNet{
/**
 * @brief R
 */
class Pdf_Document
{
    /*---------------------------  lifecycle  ------------------------------------------------ */
    public:
	typedef std::pair<QString, QString> Annot; //!<annot type and annot color 
	Pdf_Document();
	virtual ~Pdf_Document(){ } 

	/*------------------------------------------------------------------------------------ */
    public:
	QImage get_page(int page);
	QImage reload_page( );
	bool load_document(const QString &file);
	std::set<Annot> get_annots_type( );
    QString get_spec_annots(const std::set<Annot> &unique_annot);
	int num_pages() const {
	    assert(_doc);
	    return _doc->numPages();
	};
	
    protected:
//	void display_merge(Poppler::Page *page, int index);
//	void  merge_box( QRectF &a, const QRectF &b);

	/**
	 * @brief return true if two rects are in nearby line
	 *
	 */
//	bool display_mergeble(const QRectF &a, const QRectF &b);

    private:
	void init_type_map();

	/*--------------------  accessor methods  -------------------------------------------- */
    public:
	int             get_curPage( ) const                   { return _curPage;            }
	void            set_curPage( int curPage)              { _curPage = curPage;         }
	qreal           get_zoom( ) const                      { return _zoom;               }
	void            set_zoom(const qreal &zoom)            { _zoom = zoom;               }

    private:

	/*-----------------------  attributes  ------------------------------------------------ */

    protected:
	qreal	_zoom;
	int	_dpiX;
	int	_dpiY;
	int	_curPage;
	std::set<Annot> _unique_annots;
	std::map<QString,Poppler::Annotation::SubType> _type_map;
	std::map<QString,Poppler::HighlightAnnotation::HighlightType> _hl_sub_type_map;
	Poppler::Document *_doc;
	qreal	_text_height;                   //!<the height of one line of text(average) 
	QSize	_page_size;


}; 
//}

#endif 
