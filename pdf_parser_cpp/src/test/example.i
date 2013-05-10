%module example
%include <std_set.i>
//%include <std_string.i>
%{ 
    #include "example.h"
%}


%template(IntSet) std::set<int>;
// Instantiate templates used by example
//namespace std {
//}
//
//extern std::string fn(IntVector);


class Math {
 public:
    int pi() const;
    void pi(int pi);
 private:
    int _pi;
};
extern std::set<int> fn(std::set<int> m);
