%module pdfviewer
%include <std_string.i>
%include <std_set.i>
%include <std_pair.i>
%{
extern std::string open_file(const std::string &fname);
extern std::string annotations( );
extern std::string previous_page();
extern std::string next_page();
extern std::string get_page(const std::string &index);
extern std::string get_spec_annots(const std::set<std::pair<std::string, std::string> > &unique_annots);
%}

%template(Annot) std::pair<std::string, std::string>;
%template(AnnotSet) std::set<std::pair<std::string, std::string> >;
extern std::string open_file(const std::string &fname);
extern std::string annotations( );
extern std::string previous_page();
extern std::string next_page();
extern std::string get_page(const std::string &index);
extern std::string get_spec_annots(const std::set<std::pair<std::string, std::string> > &unique_annots);
