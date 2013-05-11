%module pdfviewer
%include <std_string.i>
%include <std_set.i>
%include <std_pair.i>
%include <std_vector.i>
%{
#include "pdf_document.h" 
extern bool open_file(const std::string &fname);
extern std::set<std::pair<std::string, std::string> > get_annot_types();
extern std::string previous_page();
extern std::string next_page();
extern std::string get_page(const std::string &index);
extern std::vector<AnnotStruct> get_spec_annots(const std::set<std::pair<std::string, 
                                                   std::string> > &unique_annots);


%}

%template(Annot) std::pair<std::string, std::string>;
%template(AnnotSet) std::set<std::pair<std::string, std::string> >;
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
%template(AnnotStructVec) std::vector<AnnotStruct>;

extern bool open_file(const std::string &fname);
extern std::string previous_page();
extern std::string next_page();
extern std::string get_page(const std::string &index);
extern std::set<std::pair<std::string, std::string> > get_annot_types();
extern std::vector<AnnotStruct> get_spec_annots(const std::set<std::pair<std::string, 
                                                   std::string> > &unique_annots);


