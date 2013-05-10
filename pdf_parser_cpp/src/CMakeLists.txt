CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
PROJECT(PdfViewer_PRO)
add_definitions("-std=gnu++0x -Winline")

#SET(M_LIBRARY_LIB "${CMAKE_SOURCE_DIR}/build/library")
#set(CMAKE_C_COMPILER   "/usr/bin/gcc-4.7")
#set( CMAKE_CXX_COMPILER "/usr/bin/g++-4.7")
#set(CMAKE_CXX_FLAGS                "-Wall -std=c++11 -Winline")
#set(CMAKE_CXX_FLAGS_DEBUG          "-O0 -g")
#set(CMAKE_CXX_FLAGS_MINSIZEREL     "-Os -DNDEBUG")
#set(CMAKE_CXX_FLAGS_RELEASE        "-O4 -DNDEBUG")
#set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "-O2 -g")


file(GLOB source
    "*.cpp"
    "*.cxx" 
    )


FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})
FIND_PACKAGE(PythonLibs)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})

SET(CMAKE_SWIG_FLAGS "")

SET_SOURCE_FILES_PROPERTIES(pdfviewer.i PROPERTIES CPLUSPLUS ON)
SET_SOURCE_FILES_PROPERTIES(pdfviewer.i PROPERTIES SWIG_FLAGS "-includeall")
SWIG_ADD_MODULE(pdfviewer python pdfviewer.i ${source})
SWIG_LINK_LIBRARIES(pdfviewer ${PYTHON_LIBRARIES})

find_package(Qt4 COMPONENTS QtCore QtGui REQUIRED )
if (QT4_FOUND)
    message(STATUS "Qt4 found!") 
    include(${QT_USE_FILE})
    SWIG_LINK_LIBRARIES (pdfviewer ${QT_LIBRARIES})
endif (QT4_FOUND)

INCLUDE_DIRECTORIES("/usr/local/include/")
INCLUDE_DIRECTORIES("/home/wondereamer/local/include/")
SWIG_LINK_LIBRARIES(pdfviewer
    /usr/local/lib/libiqxmlrpc.so
    /usr/lib/libxml2.so
    /usr/local/lib/libpoppler-cpp.so
    /usr/local/lib/libpoppler-qt4.so
    /usr/local/lib/libpoppler.so
    /home/wondereamer/local/lib/libtiff.so
    /usr/lib/libopenjpeg.so
    /home/wondereamer/local/lib/libjpeg.so
    /home/wondereamer/local/lib/libfontconfig.so.1
    /home/wondereamer/local/lib/libfreetype.so.6)
