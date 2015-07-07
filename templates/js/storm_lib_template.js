// JavaScript Document
var userAgent = navigator.userAgent.toLowerCase();
var ie6 = /msie 6/.test(userAgent);
var ie7 = /msie 7/.test(userAgent);
var ie8 = /msie 8/.test(userAgent);
var ie = /msie /.test(userAgent);


function isArray(value) {
	return value && typeof value === 'object' && value.constructor == Array;
};

/*!
 * jQuery Cookie Plugin v1.4.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2013 Klaus Hartl
 * Released under the MIT license
 */
(function (factory) {
	if (typeof define === 'function' && define.amd) {
		// AMD
		define(['jquery'], factory);
	} else if (typeof exports === 'object') {
		// CommonJS
		factory(require('jquery'));
	} else {
		// Browser globals
		factory(jQuery);
	}
}(function ($) {

	$.cookie = function(cname, cvalue, exdays) {
		if (cvalue === undefined) {
			var name = cname + "=";
			var ca = document.cookie.split(';');
			for(var i=0; i<ca.length; i++) 
			  {
			  var c = $.trim(ca[i]);
			  if (c.indexOf(name)==0) return c.substring(name.length,c.length);
			}
			return "";
		};
		if (cvalue == null) exdays = -30;
		else if (exdays == undefined) exdays = 30;
		var d = new Date();
		d.setTime(d.getTime()+(exdays*24*60*60*1000));
		var expires = "expires="+d.toGMTString();
		document.cookie = cname + "=" + cvalue + "; " + expires;
	}

}));

function clone(data, params) {
	function isArray(value) {
		return value && typeof value === 'object' && value.constructor == Array;
	};
	function isDate(value) {
		return value && typeof value === 'object' && value.constructor == Date;
	};
	
	if (data == null) return null;
	if (data == undefined) return undefined;
	if (isDate(data)) return data;
	
	var res = isArray(data) ? [] : {};
	if (isArray(data)) {
		for (var i in data) {
			if (typeof data[i] === 'object') res[i] = clone(data[i], params); else res[i] = data[i];
		};
	} else {
		for (var i in data) {
			if (params && params.indexOf(i) < 0) continue;
			if (typeof data[i] === 'object') res[i] = clone(data[i]); else res[i] = data[i];
		};
	};
	return res;
};

function cloned(data, params) {
	function isArray(value) {
		return value && typeof value === 'object' && value.constructor == Array;
	};
	function isDate(value) {
		return value && typeof value === 'object' && value.constructor == Date;
	};
	
	if (data == null) return null;
	if (data == undefined) return undefined;
	if (isDate(data)) return data;
	
	var res = isArray(data) ? [] : {};
	if (isArray(data)) {
		for (var i in data) {
			if (typeof data[i] === 'object') res[i] = cloned(data[i], params); else res[i] = data[i];
		};
	} else {
		for (var i in data) {
			if (params && params.indexOf(i) >= 0) continue;
			if (typeof data[i] === 'object') res[i] = cloned(data[i]); else res[i] = data[i];
		};
	};
	return res;
};

if (!Array.prototype.indexOf) {
	Array.prototype.indexOf = function(obj, start) {
		for (var i = (start || 0), j = this.length; i < j; i++) {
			if (this[i] === obj) { return i; };
		};
		return -1;
	};
};

function define_once(exp) {
	var n = exp.split("=");
	var vn = n[0].replace(/(^\s*)|(\s*$)/g, "");
	if (window[vn] == undefined) {
		eval("window." + vn + " = " + n[1].replace(/(^\s*)|(\s*$)/g, ""));
	};
};

function loadXMLString(txt) {
	try {
		var xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
		xmlDoc.async = "false";
		xmlDoc.loadXML(txt);
		return xmlDoc;
	} catch (e) {
		try {
			var parser = new DOMParser();
			var xmlDoc = parser.parseFromString(txt, "text/xml");
			return xmlDoc;
		} catch (e) {
		};
	};
};

var _template_url_data = {};

function loadContent(url) {
	if (_template_url_data[url] != undefined) {
		return _template_url_data[url];
	}
	var content;
	$.ajax(url + "?r=1.04", {
		async: false,
		success: function(data) {
			content = data;
		},
		error:function(data, textStatus, errorThrown){
			alert(textStatus + " " + errorThrown);
		}
	});
	_template_url_data[url] = content;
	return content;
};

function createStyleSheet(txt, path, format) {
	if (format == undefined) format = false;
	if (format) txt = formatPath(txt, path);
	var styleNode = document.createElement("style");
	styleNode.type = "text/css";
	if (styleNode.styleSheet) {
		styleNode.styleSheet.cssText = txt
	} else {
		styleNode.appendChild(document.createTextNode(txt));
	}
	var head = document.getElementsByTagName("head")[0];
	head.appendChild(styleNode);
};

function loadStyleSheet(src, path) {
	var content = loadContent(src);
	if (content == undefined) return;
	createStyleSheet(content, path, true);
};

function createScript(txt, path, format) {
	if (format == undefined) format = false;
	if (format) txt = formatPath(txt, path);
	var scriptNode = document.createElement("script");
	scriptNode.type = "text/javascript";
	scriptNode.text = txt;
	var head = document.getElementsByTagName("head")[0];
	head.appendChild(scriptNode);
};

function loadScript(src, path) {
	var content = loadContent(src);
	if (content == undefined) return;
	createScript(content, path, true);
};

function getAttribute(object, name) {
	if (typeof(object) == "string") {
		var i = object.indexOf(name + "=");
		if (i < 0) return null;
		i = object.indexOf("\"", i) + 1;
		return object.substring(i, object.indexOf("\"", i));
	} else {
		return object.attr(name);
	};
};

function setAttribute(object, name, value) {
	if (typeof(object) == "string") {
		var i = object.indexOf(name + "=");
		if (i < 0) {
			i = object.indexOf(">");
			return object.substr(0, i) + " " + name + "=\"" + value + "\"" + object.substr(i);
		} else {
			i = object.indexOf("\"", i) + 1;
			return object.substr(0, i) + value + object.substr(object.indexOf("\"", i));
		};
	} else {
		return object.attr(name, value);
	};
};

function replaceCode(content, code) {
	//if (content == "") return code;
	var p = code.indexOf("<content");
	if (p == -1) p = code.indexOf("<CONTENT");
	if (p == -1) return code;
	code = code.replace(/content/ig, "div");
	p = code.indexOf(">", p) + 1;
	return code.substr(0, p) + content + code.substr(p);
}

function removeWrapper(content) {
	var wrapper = content.match(/<div[\D\d]*?wrapper[\D\d]*?>/i);
	if (wrapper) {
		var s = content.replace(wrapper, "");
		var i = s.lastIndexOf("</div>");
		s = s.substr(0, i) + s.substr(i + 6);
		return s;
	}
	return content;
};

function isRelativePath(path) {
	return path.indexOf(":") < 0;
};

function addPath(type, content, path) {
	var results = content.match(eval('/' + type + '=\\"[\\D\\d]*?\\"/ig'));
	if (results) {
		for (var i = 0; i < results.length; i++) {
			var s = results[i];
			var start = s.indexOf(type + "=\"") + type.length + 2;
			var end = s.indexOf("\"", start);
			var name = s.substring(start, end);
			if (isRelativePath(name)) content = content.replace(s, s.substr(0, start) +  path + s.substr(start));
		};
	};
	return content;
};

function addPathForURL(content, path) {
	var results = content.match(/url\([\D\d]*?\)/g);
	if (results) {
		for (var i = 0; i < results.length; i++) {
			var s = results[i];
			var start = s.indexOf("url(") + 4;
			var end = s.indexOf(")", start);
			var name = s.substring(start, end);
			if (isRelativePath(name)) content = content.replace(s, s.substr(0, start) +  path + s.substr(start));
		};
	};
	return content;
};

function addPathForAppendTemplate(content, path) {
	var results = content.match(/appendTemplate\([\D\d]*?\,[\D\d]*?\,[\D\d]*?\"[\D\d]*?\)/g);
	if (results) {
		for (var i = 0; i < results.length; i++) {
			var s = results[i];
			var m = s.match(/[\D\d]*?\,[\D\d]*?\,[\D\d]*?\"/);
			if (m == undefined) continue;
			var start = m[0].length;
			var end = s.indexOf("\"", start);
			var name = s.substring(start, end);
			if (isRelativePath(name)) content = content.replace(s, s.substr(0, start) +  path + s.substr(start));
		};
	};
	return content;
};

function formatPath(content, path) {
	content = addPath("src", content, path);
	content = addPath("href", content, path);
	content = addPath("template", content, path);
	content = addPathForURL(content, path);
	content = addPathForAppendTemplate(content, path);
	return content;
}


var TemplateRegister = function() {
	this._constructor();
};
TemplateRegister.prototype._constructor = function() {
	var templates = $("div[template]");
	for (var i = 0; i < templates.length; i++) {
		var template = templates.eq(templates.length - i - 1);
		var newTemplate = new TemplateDecoder(template).bodyCode;
		this._replaceBodyCode(template, newTemplate);
	};
};
TemplateRegister.prototype._replaceBodyCode = function(template, code) {
//	var contents = template.find("content");
	if (!code) return;
	var content = template.html();
	code = replaceCode(content, code);
	template.html(code);
	template.attr("template", "");
	/*
	var div = document.createElement("div");
	div.innerHTML = code;
	var dom = template.get(0);
	var attrs = dom.attributes;
	for (var i = 0; i < attrs.length; i++) {
		var attr = attrs[i];
		if (attr.specified && attr.name.toLowerCase() != "style") {
			$(div).attr(attr.name, attr.value);
		}
	}
	$(div).attr("style", template.attr("style"));
	var parent = dom.parentNode;
	template.html("");
	parent.replaceChild(div, dom);
	*/
};

var TemplateDecoder = function(template, path) {
	this._constructor(template, path);
};
TemplateDecoder.prototype._constructor = function(template, path) {
	if (path == undefined) path = "";
	var id = getAttribute(template, "id");
	var src = getAttribute(template, "template");
	this._css = getAttribute(template, "css");
	if (src == "") return;
	var content = loadContent(src);
	if (content == undefined) return;
	content = content.replace(/t_/ig, id);
	path = src.substr(0, src.lastIndexOf("/") + 1);
	content = formatPath(content, path);
	this._decodeHead(content, path);
	this._decodeBody(content, path);
};
TemplateDecoder.prototype._decodeBody = function(content, path) {
	var bodyPos = content.indexOf("<body") + 5;
	this.bodyCode = removeWrapper(content.substring(content.indexOf(">", bodyPos) + 1, content.indexOf("</body>") - 1));
	if (this._css && this._css != undefined) {
		this.bodyCode = setAttribute(this.bodyCode, "class", this._css);
	}
	//*/
	var $code = $("<div>" + this.bodyCode + "</div>");
	var $templates = $code.find("div[template]");
	if (!$templates) return;
	for (var i = 0; i < $templates.length; i++) {
		var template = $($templates[$templates.length - 1 - i]);
		var code = new TemplateDecoder(template, path).bodyCode;
		var content = template.html();
		code = replaceCode(content, code);
		template.html(code);
		template.attr("template", "");
	};
	
	this.bodyCode = $code.html();
//	alert(this.bodyCode);
//	alert(this.bodyCode);
	/*/
	var templates = this.bodyCode.match(/<[^>]*?template=[^>]*?>[^>]*?<\/div>/ig);
	if (templates) {
		for (var i = 0; i < templates.length; i++) {
			//alert(templates[i]);
			var template = templates[templates.length - 1 - i];
			var newTemplate = new TemplateDecoder(template, path).bodyCode;
			this._replaceBodyCode(template, newTemplate, path);
		};
	};
	var templates = this.bodyCode.match(/<[^>]*?template=[\D\d]*?>[\D\d]*?<\/div>/ig);
	if (templates) {
		for (var i = 0; i < templates.length; i++) {
			var template = templates[templates.length - 1 - i];
			var newTemplate = new TemplateDecoder(template, path).bodyCode;
			this._replaceBodyCode(template, newTemplate, path);
		};
	};
	this.bodyCode = this.bodyCode.replace(/<tmp/ig, "<div");
	this.bodyCode = this.bodyCode.replace(/<\/tmp>/ig, "</div>");
	//*/
};
TemplateDecoder.prototype._replaceBodyCode = function(template, code, path) {
	if (!code) return;
//	template = template.replace(/template=\"[\D\d]*?\"/i, "template=\"\"");
	var content = template.substring(template.indexOf(">") + 1, template.lastIndexOf("<"));
	//content = decodeTemplate(content, path);
	code = replaceCode(content, code);
	var str = template;//.replace(/template/ig, "div");
	var i = str.indexOf(">");
	str = "<tmp" + str.substring(4, i + 1) + code + str.substring(i + 1 + content.length, str.length - 4) + "tmp>";
	str = str.replace(/template=\"[\D\d]*?\"/i, "");
	this.bodyCode = this.bodyCode.replace(template, str);
};
TemplateDecoder.prototype._decodeHead = function(content, path) {
	var head = content.substring(content.indexOf("<head"), content.indexOf("</head>") + 7);
	var links = head.match(/<link[\D\d]*?\/?>/ig);
	var styles = head.match(/<style[\D\d]*?<\/style>/ig);
	var scripts = head.match(/<script[\D\d]*?<\/script>/ig);
	this._decodeStyleSheet(links, path);
	this._decodeStyle(styles, path);
	this._decodeScripts(scripts, path);
};
TemplateDecoder.prototype._decodeStyleSheet = function(links, path) {
	if (!links) return;
	for (var i = 0; i < links.length; i++) {
		var linkNode = loadXMLString(links[i]).documentElement;
		if (linkNode.getAttributeNode("rel").nodeValue == "stylesheet") {
			var src = linkNode.getAttributeNode("href").nodeValue;
			loadStyleSheet(src, path);
		};
	};
};
TemplateDecoder.prototype._decodeStyle = function(styles, path) {
	if (!styles) return;
	for (var i = 0; i < styles.length; i++) {
		var stylestr = styles[i];
		var styleCode = stylestr.substring(stylestr.indexOf(">") + 1, stylestr.lastIndexOf("</style>"));
		createStyleSheet(styleCode, path);
	};
};
TemplateDecoder.prototype._decodeScripts = function(scripts, path) {
	if (!scripts) return;
	 for (var i = 0; i < scripts.length; i++) {
		var scriptstr = scripts[i];
		if (scriptstr.indexOf(" src=") >= 0) {
			var scriptNode = loadXMLString(scriptstr).documentElement;
			var src = scriptNode.getAttributeNode("src").nodeValue;
			loadScript(src, path);
		} else {
			var scriptCode = scriptstr.substring(scriptstr.indexOf(">") + 1, scriptstr.lastIndexOf("</script>"));
			createScript(scriptCode, path);
		};
	 };
};
function registTemplate() {
	new TemplateRegister();
};
function decodeTemplate(template) {
	var code = $.trim(new TemplateDecoder(template).bodyCode);
	if (!code) return "";
	template = template.replace(/template=\"[\D\d]*?\"/i, "template=\"\"");
	var content = template.substring(template.indexOf(">") + 1, template.lastIndexOf("<"));
	code = replaceCode(content, code);
	var str = template;//.replace(/template/ig, "div");
	var i = str.indexOf(">");
	str = str.substr(0, i + 1) + code + str.substr(i + 1);
	return str;
};
function decodeTemplates(templatesObj) {
	var templates = templatesObj.find("div[template]");
	if (!templates) return templatesObj;
	for (var i = 0; i < templates.length; i++) {
		var template = $(templates[templates.length - 1 - i]);
		var code = new TemplateDecoder(template).bodyCode;
		var content = template.html();
		code = replaceCode(content, code);
		template.html(code);
		template.attr("template", "");
	};
	return templatesObj;
};
function appendTemplate(object, id, src, stylesheet, stylename, currentstyle) {
	if (currentstyle == undefined) currentstyle = "";
	if (stylename == undefined) stylename = "";
	if (stylesheet == undefined) stylesheet = "";
	var code = '<div id="' + id + '" class="' + stylesheet + '" css="' + stylename + '" style="' + currentstyle + '" template="' + src + '"></div>';
	$(object).append(decodeTemplate(code));
	eval('var o = ' + id);
	o.parentObject = object;
	return o;
};