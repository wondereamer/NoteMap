#include "example.h"
#include <iostream>

int Math::pi() const {
    return this->_pi;
}  
void Math::pi(int pi) {
    this->_pi = pi;
}

std::set<int> fn(std::set<int> m)
{
    std::set<int> a;
    std::cout<<"*********************************"<<std::endl;    
    std::set<int>::iterator i = m.begin();
    std::cout<<*i<<std::endl;
    return a;
}
