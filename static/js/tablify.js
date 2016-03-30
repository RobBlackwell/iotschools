// Converts JavaScript objects to HTML tables.

function isObject(obj) {
    return (Object.prototype.toString.call(obj) === '[object Object]');
}

function isComposite(obj) {
    return Array.isArray(obj) || isObject(obj);
}

function isString(obj) {
    return (typeof obj) == "string";
}

function isUrlString(obj) {
    // Probably to crude
    return isString(obj) && (obj.substring(0, 4) == "http" || obj.substring(0, 1) == "/");
}

function anchorify(s) {
    return "<a href=\"" + s + "\">>></a>";
}

function toVerticalTable(obj) {
    var tbl_body = "<table>";
    
    jQuery.each(obj, function(key, value) {
	
	var tr = "<tr><td><b>" + key + "</b></td><td>" + toTable(value) + "</td></tr>";
	
	tbl_body += tr;
    });
    
    tbl_body += "</table>";
    return tbl_body;
}

function toHorizontalTable(obj) {
    var tbl_body = "<table>";
    var heading = true;
    
    jQuery.each(obj, function(key, value) {
	
	if (heading) {
	    var th = "<tr>";
	    
	    if (isComposite(value)) {
		jQuery.each(value, function(key, value) {
		    th += "<th>" + key + "</th>";
		});
	    } else {
		tr += "<th>" + value + "</th>";
	    }
	    
	    
	    th += "</tr>";
	    tbl_body += th;
	    heading = false;
	}
	
	var tr = "<tr>";
	
	if (isComposite(value)) {
	    jQuery.each(value, function(key, value) {
		tr += "<td>" + toTable(value) + "</td>";
	    });
	} else {
	    tr += "<td>" + value + "</td>";
	}
	
	
	tr += "</tr>";
	tbl_body += tr;
    });
    
    
    tbl_body += "</table>";
    return tbl_body;
    
}

function toTable(obj) {
    if (isObject(obj)) {
	return toVerticalTable(obj);
    } else if (Array.isArray(obj)) {
	if (obj.length > 1) {
	    return toHorizontalTable(obj);
	}
	else {
	    return toHorizontalTable(obj[0]);
	}
    } else if (isUrlString(obj)) {
	return anchorify(obj);
    } else {
	return obj;
    }
}


function toVerticalCSV(obj) {
    var csv = ""
    
    jQuery.each(obj, function(key, value) {
	
	var row = "\"" + key + "\",\"" + value + "\"\n";
	
	csv += row;
    });
    
    return csv;
}

function toHorizontalCSV(obj) {
    var csv = "";
    var heading = true;
    
    jQuery.each(obj, function(key, value) {
	
	if (heading) {
	    var row=""
	    
	    if (isComposite(value)) {
		jQuery.each(value, function(key, value) {
		    row += "\"" + key + "\",";
		});
	    } else {
		row += "\"" + value + "\"";
	    }
	    
	    row += "\n";
	    csv += row;
	    heading = false;
	}
	
	var row = "";
	
	if (isComposite(value)) {
	    jQuery.each(value, function(key, value) {
		row += "\"" + value + "\",";
	    });
	} else {
	    	row += "\"" + value + "\"";
	}
	
	row += "\n";
	csv += row;
    });
    
    
    return csv;
    
}
function toCSV(obj) {
    if (isObject(obj)) {
	return toVerticalCSV(obj);
    } else if (Array.isArray(obj)) {
	if (obj.length > 1) {
	    return toHorizontalCSV(obj);
	}
	else {
	    return toHorizontalCSV(obj[0]);
	}
    } 
}

