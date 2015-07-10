var ROOT_PATH = "";
var FOLDER_PATH = "../";

var navdata = [
	{title:"首页", href:"home.html"},
	{title:"通知公告", href:"javascript:void(0)"},
	{title:"招标公告", href:"javascript:void(0)"},
	{title:"中标公告", href:"javascript:void(0)"},
	{title:"招标预告", href:"javascript:void(0)"},
	{title:"变标公告", href:"javascript:void(0)"},
	{title:"政策法规", href:"javascript:void(0)"},
	{title:"供应商名单", href:"javascript:void(0)"}
];

function setnavdata(nav, index) {
	nav.data(navdata);
	if (index !== undefined) nav.navindex(index);
};

var TIME_FIELD = [
	{title:"08:00-09:00"},
	{title:"10:00-11:00"},
	{title:"12:00-14:00"},
	{title:"14:00-15:30"},
	{title:"21:00-22:00"}
];
function getTimeField(index) {
	if (index >= 0) return TIME_FIELD[index].title;
	return "08:00-09:00";
};
function getTimeFieldIndex(title) {
	for (var i = 0; i < TIME_FIELD.length; i++) {
		if (TIME_FIELD[i].title == title) return i;
	};
	return -1;
};
function getDate(date) {
	var d = date.split('-');
	return new Date(d[0], d[1] - 1, d[2])
};
var o1, o2, o3, o4;
if (typeof jQuery != 'undefined') {
	$(document).ajaxError(function(event, jqxhr, settings, exception) {
		if (jqxhr.status == 401) {
			window.location.href = 'login.html';
		};
	});
}

function tofixed(value, digit) {
	if (digit == undefined) digit = 2;
	var s = Math.round(value * Math.pow(10, digit)) + "";
	while (s.length < digit + 1) s = "0" + s;
	eval("s = s.replace(/(.{" + (s.length - digit) + "})/, '$1\.')");
	return s;
};

function getUrlParam(name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
	var r = window.location.search.substr(1).match(reg);  //匹配目标参数
	if (r != null) return decodeURI(r[2]); return null; //返回参数值
};
function date2str(x, y) {
	if (!x) return "";
	if (y == undefined) y = "yyyy-MM-dd";
	var z = {y:x.getFullYear(), M:x.getMonth()+1, d:x.getDate(), h:x.getHours(), m:x.getMinutes(), s:x.getSeconds()};
	return y.replace(/(y+|M+|d+|h+|m+|s+)/g,function(v) {return ((v.length>1?"0":"")+eval('z.'+v.slice(-1))).slice(-(v.length>2?v.length:2))}); 
};
function updateMenus(menus, path) {
	for (var i = 0; i < menus.length; i++) {
		menus[i].href = path + menus[i].href;
		if (menus[i].children != undefined) {
			updateMenus(menus[i].children, path);
		};
	};
};
function selectMenu(menus, id) {
	for (var i = 0; i < menus.length; i++) {
		if (menus[i].id == id) {
			menus[i].selected = true;
			return true;
		};
		if (menus[i].children != undefined) {
			if (selectMenu(menus[i].children, id)) return true;
		};
	};
	return false;
};
function getFileId(files) {
	var id;
	if (files && files.length > 0) {
		id = files[0].id;
	};
	return id;
};
function getFileIds(files) {
	var ids = [];
	if (files) {
		for (var i = 0; i < files.length; i++) {
			ids.push(files[i].id);
		};
	};
	return ids;
};

function num2cur(number) {
	var n = (tofixed(number, 2)) + "";
	var reg = /(\d{1,3})(?=(\d{3})+(?:$|\.))/g;
	return n.replace(reg, "$1,");
};
function null2str(value) {
	return value == null ? "" : value;
};

function showobj(obj) {
	var s = "";
	for (var i in obj) {
		s += i + ": " + obj[i] + "\n";
	};
	alert(s);
};

function post(url, data, success) {
	$.ajax({
		url: url,
		contentType:"application/json; charset=UTF-8",
		type: "POST",
		dataType:"json",
		data: JSON.stringify(data),
		success: success,
		error: function(data) {
			processNetError(data);
		}
	});
};

function get(url, success) {
	$.ajax({
		url: url,
		type: "GET",
		success: success,
		error: function(data) {
			processNetError(data);
		}
	});
};

var global = {};

var JSON = function () {
    var m = {
            '\b': '\\b',
            '\t': '\\t',
            '\n': '\\n',
            '\f': '\\f',
            '\r': '\\r',
            '"' : '\\"',
            '\\': '\\\\'
        },
        s = {
            'boolean': function (x) {
                return String(x);
            },
            number: function (x) {
                return isFinite(x) ? String(x) : 'null';
            },
            string: function (x) {
                if (/["\\\x00-\x1f]/.test(x)) {
                    x = x.replace(/([\x00-\x1f\\"])/g, function(a, b) {
                        var c = m[b];
                        if (c) {
                            return c;
                        }
                        c = b.charCodeAt();
                        return '\\u00' +
                            Math.floor(c / 16).toString(16) +
                            (c % 16).toString(16);
                    });
                }
                return '"' + x + '"';
            },
            object: function (x) {
                if (x) {
                    var a = [], b, f, i, l, v;
                    if (x instanceof Array) {
                        a[0] = '[';
                        l = x.length;
                        for (i = 0; i < l; i += 1) {
                            v = x[i];
                            f = s[typeof v];
                            if (f) {
                                v = f(v);
                                if (typeof v == 'string') {
                                    if (b) {
                                        a[a.length] = ',';
                                    }
                                    a[a.length] = v;
                                    b = true;
                                }
                            }
                        }
                        a[a.length] = ']';
                    } else if (x instanceof Object) {
                        a[0] = '{';
                        for (i in x) {
                            v = x[i];
                            f = s[typeof v];
                            if (f) {
                                v = f(v);
                                if (typeof v == 'string') {
                                    if (b) {
                                        a[a.length] = ',';
                                    }
                                    a.push(s.string(i), ':', v);
                                    b = true;
                                }
                            }
                        }
                        a[a.length] = '}';
                    } else {
                        return;
                    }
                    return a.join('');
                }
                return 'null';
            }
        };
    return {
        copyright: '(c)2005 JSON.org',
        license: '/web/20060206022229/http://www.crockford.com/JSON/license.html',
/*
    Stringify a JavaScript value, producing a JSON text.
*/
        stringify: function (v) {
            var f = s[typeof v];
            if (f) {
                v = f(v);
                if (typeof v == 'string') {
                    return v;
                }
            }
            return null;
        },
/*
    Parse a JSON text, producing a JavaScript value.
    It returns false if there is a syntax error.
*/
        parse: function (text) {
            try {
                return !(/[^,:{}\[\]0-9.\-+Eaeflnr-u \n\r\t]/.test(
                        text.replace(/"(\\.|[^"\\])*"/g, ''))) &&
                    eval('(' + text + ')');
            } catch (e) {
                return false;
            }
        }
    };
}();



