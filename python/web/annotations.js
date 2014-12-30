var extracted_annotations = new Array();
var extracted_annotations_page = new Array();

alert("OOO");
function get_annots(url) {
    var SUPPORTED_ANNOTS = ["Highlight", "Underline"];
    extracted_annotations = [];
    extracted_annotations_page = [];
    ret = [];
    var parameters = {"" :"" };
    if (typeof url === 'string') { // URL
        parameters.url = url;
    } 
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
                                extracted_annotations_page.push(pdfPage.pageNumber);
                            }
                        });
                    });
                }
            });

}



function send_annots_to_server( ) {
    SEPANNOT = "%AnNot!";
    SEPITEM = "%ItEm!";
    str = "" 
    for (var i = 0; i < extracted_annotations.length; i++) {
        str += SEPANNOT;
        str += extracted_annotations[i].content;
        str += SEPITEM;
        str += extracted_annotations[i].type;
        str += SEPITEM;
        str += extracted_annotations[i].color;
        str += SEPITEM;
        str += extracted_annotations[i].rect;
        str += SEPITEM;
        str += extracted_annotations_page[i];
    };
    str += SEPANNOT;
    var cmds = new Commands();
    var annotCmd = new Command("Annots");
    annotCmd.add_param("data", str);
    cmds.insert_command(annotCmd);
    cmds.excute(function(text) {
        console.log("^^^^^^^^^^^^^^^^^^^^");
        console.log(text);
    });
}
function get_pdf_filename() {
    var pdfName = "";
    var cmds = new Commands();
    var annotCmd = new Command("TARGET_PDF");
    cmds.insert_command(annotCmd);
    cmds.excute(function(text) {
        console.log(text);
        pdfName = text;
        alert(text);
    });
    return pdfName;
}//end of get_pdf_filename
var fname = get_pdf_filename();
alert(fname);
get_annots(fname);
/*setTimeout("get_annots(fname)", 1000 );*/
setTimeout("send_annots_to_server( )", 2000 );
