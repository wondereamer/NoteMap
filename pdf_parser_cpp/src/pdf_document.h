#ifndef PDF_DOCUMENT_h

#define PDF_DOCUMENT_h
#include <poppler/qt4/poppler-qt4.h>
#include <QImage>
#include <set>
//#include <std::stringList>
#include <QRectF>
#include <QSize>
#include <cassert>
#include <map>
#include <vector>
#include <string>

struct AnnotStruct{
    float _y;
    float _x;
    int _page;
    bool operator < (const AnnotStruct &other) const{
        if(_page < other._page)
            return true;
        else if(_page > other._page)
            return false;
        else if(_y < other._y)
            return true;
        else if(_y > other._y)
            return false;
        else if(_x < other._x)
            return true;
        else return false;
    }
    std::string _content;
    std::string _color;
    std::string _type;
};
//namespace IdeaNet{
/**
 * @brief R
 */
class Pdf_Document
{
    /*---------------------------  lifecycle  ------------------------------------------------ */
    public:
	typedef std::pair<std::string, std::string> Annot; //!<annot type and annot color 
	Pdf_Document();
	virtual ~Pdf_Document(){ } 

	/*------------------------------------------------------------------------------------ */
    public:
	QImage get_page(int page);
	QImage reload_page( );
	bool load_document(const std::string &file);
	std::set<Annot> get_annots_type( );
    std::vector<AnnotStruct> get_spec_annots(const std::set<Annot> &unique_annots);
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
    //! map std::string to annotation type 
	std::map<std::string,Poppler::Annotation::SubType> _type_map;
    //! map std::string to highlight annotation subtype 
	std::map<std::string,Poppler::HighlightAnnotation::HighlightType> _hl_subtype_map;
	Poppler::Document *_doc;
    //! the height of one line of text(average) 
	qreal	_text_height;                
	QSize	_page_size;


}; 
//}

#endif 
