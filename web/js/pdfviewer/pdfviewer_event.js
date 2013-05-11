/*alert($(this).find("option:selected").text());*/
function assert(bCondition, sErrorMsg) {
    if (!bCondition) {
	alert(sErrorMsg);
	throw new Error(sErrorMsg);
    }
}
function xml_to_string(xml) {
    if ( window.DOMParser ) {
	return  (new XMLSerializer()).serializeToString(xml);
    } else if ( window.ActiveXObject ) {
	return xml.xml;
    }
}
function haiming_distance(a,b) {
    var sum =  0;
	for (var i = 0; i < a.length; i++) {
		var temp = a[i] - b[i];
		if (temp < 0)
		    temp = 0 - temp;
		sum += temp;
	};
    return sum;
}
//  constructor
XML_Parser = function(){ return this};
//  object prototype
XML_Parser.prototype.__dom = "";
XML_Parser.prototype._root = "";

//  method: parseXML( xmlsource )
XML_Parser.prototype.parseXML = function ( xml ) {
    if ( window.DOMParser ) {
	var xmldom = new DOMParser();
	//      xmldom.async = false;           // DOMParser is always sync-mode
	this.__dom = xmldom.parseFromString( xml, "application/xml" );
    } else if ( window.ActiveXObject ) {
	xmldom = new ActiveXObject('Microsoft.XMLDOM');
	xmldom.async = false;
	this.__dom = xmldom.loadXML( xml );
    }
    if (this.__dom ) {
	this._root = this.get_nodes("root")[0];
	return true;
    }
    return false;

};
XML_Parser.prototype.get_nodes = function(tagName){
    return this.__dom.getElementsByTagName(tagName);
};

XML_Parser.prototype.get_root = function(tagName){
    return this._root;
};
XML_Parser.prototype.add_node = function(parentNode, newNode){
    parentNode.appendChild(newNode);
};
XML_Parser.prototype.create_node = function(nodeName,nodeText){
    var newNode = this.__dom.createElement(nodeName);
    if(arguments.length == 2)
    {
	var newText = this.__dom.createTextNode(nodeText);
	newNode.appendChild(newText);
    }
    return newNode;
};
XML_Parser.prototype.xml_to_string = function(){
    if ( window.DOMParser ) {
	return  (new XMLSerializer()).serializeToString(this.__dom);
    } else if ( window.ActiveXObject ) {
	return this.__dom.xml;
    }
};
//*****************************************************************************************

Commands = function(){ 
    var head = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><root> <source>pdfviewer</source> </root>";
    this._parser = new XML_Parser();
    this._parser.parseXML(head);
    return this;
};

Commands.prototype._parser = "" 

Commands.prototype.__get_commands = function(){
    return this._parser.xml_to_string();
};
Commands.prototype.insert_command = function (command) {

    var cmdNode = this._parser.create_node("command");
    cmdNode.setAttribute("name",command._name);
    this._parser.add_node(this._parser.get_root(),cmdNode);
    //
    if (command._params['names'].length > 0) {
	for (var i = 0; i < command._params['names'].length; i++) {
	    var name = command._params['names'][i];
	    var value = command._params['values'][i];
	    var paramNode = this._parser.create_node(name,value);
	    this._parser.add_node(cmdNode,paramNode);
	}
    }

}
Commands.prototype.excute = function(callback){
    $.ajax({
	url:'handle', //后台处理程序
	type:'POST',         //数据发送方式
	dataType:'xml',     //接受数据格式
	data:this.__get_commands(),         //要传递的数据
	success:function(data){
	    callback(data);
	},
	async:false
    });
};
//************************************************************************
Command = function(name){ 
    this._name = name;
    this._params['names']=[];
    this._params['values']=[];
    return this;
}

Command.prototype._name = "";
Command.prototype._params = {
				'names': [],
				'values': []
			    }

Command.prototype.add_param = function(name,value){
    if (arguments.length == 2) {
	this._params['names'].push(name);
	this._params['values'].push(value);
    } else{
	alert("error: wrong arguments of Command.add_param()");
    }
};
//************************************************************************
// global variables.....................
unique_annots = new Array();
unique_annots[0] = new Array(); //type
unique_annots[1] = new Array(); //color
unique_annots[2] = new Array(); //r
unique_annots[3] = new Array(); //g
unique_annots[4] = new Array(); //b
groups_annot = new Array();
temp_annots = new Array();
cur_page = -1;                              // string
cur_annot = 0;
// signal....................
OPEN_PDF = "OPEN_PDF";
NEXT = "NEXT";
PREVIOUS = "PREVIOUS";
ANNOTS_TYPE = "ANNOTS_TYPE";
SPEC_ANNOTS = "SPEC_ANNOTS";
GET_PAGE = "GET_PAGE";
// slot.........................

function on_open_pdf(filename) {
    cur_page = 1;
    var cmds = new Commands();
    var openCmd = new Command(OPEN_PDF);
    openCmd.add_param("filename",filename);
    cmds.insert_command(openCmd);
    cmds.excute(function(xml) {
	var path = $(xml).find("path").text();
	console.log(path);
	$('#content_widget').attr('src',path);
    });
}
function on_next() {
    /// @todo the end of page
    cur_page += 1;
    get_page(cur_page);
}

function on_previous() {

    cur_page -= 1;
    get_page(cur_page);
}

function on_annots_type() {
    // clean data
    for (var i = 0; i < unique_annots.length; i++) {
    	unique_annots[i] = [];
    };
    std_annots = [];
    groups_annot = [];
    $('#Dialog_annots li').remove();
    // excute command
    var cmds = new Commands();
    var openCmd = new Command(ANNOTS_TYPE);
    cmds.insert_command(openCmd);
    cmds.excute(function(xml) {
    var index = 0;
    //about command resualt
    $(xml).find("unique_annot").each(function (i) {
	var type = $(this).children("type").text();
	var color = $(this).children("color").text();
	unique_annots[0].push(type);
	unique_annots[1].push(color);
	unique_annots[2].push($(this).children("r").text());
	unique_annots[3].push($(this).children("g").text());
	unique_annots[4].push($(this).children("b").text());
	var li = $('<li></li>');
	li.css("background-color",color);
	li.data('index',index);
	li.html(type).appendTo($('#Dialog_annots ul'));
	index++;
    });
    // display the dialog
    $('#Dialog_annots').dialog("open");
    // slot of dialog ................................................................
    //
    $('#Dialog_annots li').click(function(){
	var value = $(this).data('index');
	// whether exist
	for (var i = 0; i < std_annots.length; i++) {
		if(std_annots[i] == value)
		    return;
	};
	if(temp_annots.length == 0)
	    std_annots.push(value);
	temp_annots.push(value);
	$(this).remove();
    });
    //
});
}
//signal map to slot.......................................................
$(document).ready(function(){
    $('#Open').click(function(){
	rst = prompt("Input Filename:","moses.pdf");
	if (rst != "" ) {
	    on_open_pdf(rst);
	};
    });
    $('#Next').click(function(){
	on_next();
    });
    $('#Previous').click(function(){
	on_previous();
    });
    $('#Annots_type').click(function(){
	on_annots_type();
    });
    //go to next_annot_page
    $('#content_widget').click(function(){
       to_next_annot_page(); 
    	    });

    // close event
    $('#Dialog_annots').bind( "dialogbeforeclose", function(event, ui) {
	// about "li click" and "confirm" 
	if (std_annots.length <= 0 || temp_annots.length > 0)
	    return false;
	else{
	    // clear the select elments
	    $('#select_annots option').remove();
	    $('<option value="-1">Default</option>').appendTo($('#select_annots')) ;
	    // add element
	    console.log("lenth of std_annots:");
	    console.log(std_annots.length);
	    for (var i = 0; i < std_annots.length; i++) {
		var type = unique_annots[0][std_annots[i]];
		var color = unique_annots[1][std_annots[i]];
		// value == index
		/*var option =  '<option value="' + std_annots[i] + '" style="color:' + color + '" >' + type + '</option>'; */
		var option =  '<option value="' + std_annots[i] + '" style="color:' + color + '" >' + type + '</option>'; 
		console.log(option);
		$(option).appendTo($('#select_annots'));
	    };
	    return true;
	}

    });

    // todo double click
    $('#Btn_Dialog_annots_confirm').click(function(){
	if(temp_annots.length > 0){
	    groups_annot.push(temp_annots);	    
	    console.log("groups_annot:");
	    console.log(groups_annot);
	}
	temp_annots = [];
    });
    // select one specify annotation
    $('#select_annots').change(function(){
	assert(groups_annot.length > 0, "change");
	var choosed = $(this).val();
	console.log("choosed:");
	console.log(choosed);
	var spec_annots_i =  0;
	for (var i = 0; i < groups_annot.length; i++) {
	    if(choosed == groups_annot[i][0])
		spec_annots_i = i;
	};
	var arg = "<root>";
	console.log("groups_annot");
	console.log(groups_annot);
	console.log("spec_annots:");
	console.log(groups_annot[spec_annots_i]);
	for (var i = 0; i < groups_annot[spec_annots_i].length; i++) {
	    arg += "<annot>";
	    arg += "<type>";
	    arg += unique_annots[0][groups_annot[spec_annots_i][i]];
	    arg += "</type>";
	    arg += "<color>";
	    arg += unique_annots[1][groups_annot[spec_annots_i][i]];
	    arg += "</color>";
	    arg += "</annot>";
	};
	arg += "</root>";
	// send Commands to server
	var cmds = new Commands();
	var cmd = new Command(SPEC_ANNOTS);
	cmd.add_param("spec_annots",arg);
	cmds.insert_command(cmd);

	console.log("send data to server:");
	console.log(arg);
	cmds.excute(function(xml) {
	    //initial
	    $('#Dialog_dis_annots tr').remove();
	    var head = $('<tr></tr>');
	    $('<td></td>').html('type').appendTo(head);
	    $('<td></td>').html('content').appendTo(head);
	    $('<td></td>').html('page').appendTo(head);
	    head.appendTo('#Dialog_dis_annots table');
	    $(xml).find("annot").each(function (i) {
		var type = $(this).children("type").text();
		var color = $(this).children("color").text();
		var content = $(this).children("content").text();
		var page = $(this).children("page").text();
		//
		var tr = $('<tr></tr>').data('page',page);
		$('<td></td>').html(type).css("background-color",color).appendTo(tr);
		$('<td></td>').html(content).appendTo(tr);
		$('<td></td>').html(page).appendTo(tr);
		tr.appendTo($('#Dialog_dis_annots table'));

	    });
	    $('#Dialog_dis_annots').dialog("open");
	    $('#Dialog_dis_annots tr').click(function(){
			var page = new Number($(this).data('page'));
			if(page) {
			    cur_annot = $(this);
			    $('#Dialog_dis_annots').dialog("close");
			    cur_page = page;
			    get_page(page);

			}
	    	    });

	});
    });//end of function

});
function get_page(page) {
    var cmds = new Commands();
    var cmd = new Command(GET_PAGE);
    cmd.add_param("page",page);
    cmds.insert_command(cmd);
    cmds.excute(function(xml) {
	var path = $(xml).find("path").text();
	if(path != ""){
	    $('#content_widget').attr('src',path);
	    console.log(path);
	}else
	    console.log("the end");
    });
}//end of get_page
function keyboard_manage(e) 
{
    var key_left = 37;
    var key_right = 39;
    if ( window.DOMParser ) {
　　　var   key = e.which;  
    } else if ( window.ActiveXObject ) {
　　　var   key = event.keyCode;  
    }
    /*alert( String.fromCharCode(key));*/
    if(key == key_right){
	to_next_annot_page();
    }
    /// @todo key_left
}   
function to_next_annot_page() {
	cur_annot = cur_annot.next();
	 while (cur_annot.length != 0){
	     var next_annot_page = new Number(cur_annot.data('page'));
	     //@@?
	     if(cur_page.toString() != next_annot_page.toString()){
		 //find the first different next annot page
		 cur_page = next_annot_page;
		 get_page(cur_page);
		 console.log("cur_page:");
		 console.log(cur_page.toString());
		 break;
	     }
	    cur_annot = cur_annot.next();
	};
	if(cur_annot.length == 0)
	    alert("the end");
}//end of to_next_annot_page
