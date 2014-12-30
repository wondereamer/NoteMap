//  constructor
XML_Parser = function(){ return this};
//  object prototype
XML_Parser.prototype._dom = "";

//  method: parseXML( xmlsource )
XML_Parser.prototype.parseXML = function ( xml ) {
    var root;
    if ( window.DOMParser ) {
        var xmldom = new DOMParser();
//      xmldom.async = false;           // DOMParser is always sync-mode
        this._dom = xmldom.parseFromString( xml, "application/xml" );
    } else if ( window.ActiveXObject ) {
        xmldom = new ActiveXObject('Microsoft.XMLDOM');
        xmldom.async = false;
        this._dom = xmldom.loadXML( xml );
    }
    if (!this._dom ) 
	return false;
    else
	return true;
};
XML_Parser.prototype.get_nodes = function(tagName){

	return this._dom.getElementsByTagName(tagName);
};
XML_Parser.prototype.add_node = function(parentNode, newNode){
    parentNode.appendChild(newNode);
};
XML_Parser.prototype.create_node = function(nodeName,nodeText){
	newNode = this._dom.createElement(nodeName);
	newText = this._dom.createTextNode(nodeText);
	newNode.appendChild(newText);
	return newNode;
};
XML_Parser.prototype.xml_to_string = function(){
    if ( window.DOMParser ) {
	return  (new XMLSerializer()).serializeToString(this._dom);
    } else if ( window.ActiveXObject ) {
	return this._dom.xml;
    }
};
