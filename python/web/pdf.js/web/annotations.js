function get_annots(url) {

    var parameters = {"" :"" };
    if (typeof url === 'string') { // URL
      parameters.url = url;
    } 
    var extracted_annotations = [];
    var extracted_annotations_page = [];
    var SUPPORTED_ANNOTS = ["Highlight", "Underline"];
    PDFJS.getDocument(parameters, 0).then(
      function getDocumentCallback(pdfDocument) {
    var pagesCount = pdfDocument.numPages;
      //------------------------------------------------------------------
     // iterate over all pages
      for (var pageNum = 1; pageNum <= pagesCount; ++pageNum) {
        var pagePromise = pdfDocument.getPage(pageNum);
        pagePromise.then(function(pdfPage) {
        // iterate over annotations
          pdfPage.getAnnotations().then(function (annos) {
            // filter for supported annotations
            var annots = annos.filter(function(anno) {return SUPPORTED_ANNOTS.indexOf(anno.type) >= 0;});
            // skip page if there is nothing interesting
            if (annots.length==0) {
              ;
            }
            // handle annotations
            for (var i=0;i<annots.length;i++) {
              // push annotation to array
              console.log("******************");
              console.log(annots[i].type);
              console.log(annots[i].content);
              console.log(annots[i].color);
              console.log(annots[i].rect);
            extracted_annotations.push(annots[i]);
            extracted_annotations_page.push(pageNum);
            }
          });
        });
      }
      });
    }

get_annots("compressed.tracemonkey-pldi-09.pdf" );
a = stringToPDFString(" ???????????????????????????????? ????????????????");
