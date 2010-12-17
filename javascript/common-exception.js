/* Begin browser part */

var common_exception_fromException = function(e) {
    
    // Frame regex groups: (scope_name, file_url, line_number, column_number)
    
    //()@file:///Users/a/Desktop/foo.html:11
    var REGEX_FIREFOX = /([^@]+)@(.+):([0-9]+)()/;
    
    // at file:///Users/a/Desktop/foo.html:15:7
    // at onload (file:///Users/a/Desktop/foo.html:38:4)
    var REGEX_CHROME = /at[ ]?(.*) \(?(.+):([0-9]+):([0-9]+)\)?/;
    
    
    var TOPFRAME_BROWSERKEYS = [
        'sourceURL', 'line',
        'expressionBeginOffset', 'expressionCaretOffset', 'expressionEndOffset'];
        
    var TOPFRAME_CEKEYS = [
        'file_url', 'line_number',
        'byte_offset_start', 'byte_offset', 'byte_offset_end'];
        
    var TOPFRAME_NUMKEYS = 5;
    
    
    var ex = {};
    var stack = [];
    var topFrame = {};
    var includeTopFrame = 0;
    var i = 0;
    var lines, line, bound, m;
    
    
    // Chrome, Safari, Firefox
    if (e['name']) {
        ex['name'] = e['name'];
    }
    
    // Chrome, Safari, Firefox
    if (e['message']) {
        ex['message'] = e['message'];
    }
    
    if (e['stack']) {
        // Chrome, Firefox
        lines = e['stack'].split('\n')
        bound = lines.length;
        for (; i < bound; i++) {
            line = lines[i];
            m = line.match(REGEX_FIREFOX) || line.match(REGEX_CHROME);
            if (m) {
                stack.push({
                    // (empty groups work) and ('' is falsish), at least in FF and Chrome
                    'scope_name': m[1] || null,
                    'file_url': m[2],
                    'line_number': 1 * m[3],
                    'column_number': m[4] ? 1 * m[4] : null
                })
            }
        }
        if (stack.length > 0) {
            ex['stack'] = stack;
        }
    }
    else {
        // Safari
        for (; i < TOPFRAME_NUMKEYS; i++) {
            m = e[TOPFRAME_BROWSERKEYS[i]];
            if (m) {
                topFrame[TOPFRAME_CEKEYS[i]] = m;
                includeTopFrame = 1;
            }
        }
        if (includeTopFrame) {
            ex['stack'] = [topFrame];
        }
    }
    
    return {
        'exception': ex
    };
};

/* End browser part */


var r1 = new RegExp('at ([^ ]+) \\(([^ ]+):([0-9]+):([0-9]+)\\)');
var r2 = new RegExp('at ([^ ]+):([0-9]+):([0-9]+)');
var r3 = new RegExp('at ([^ ]+) \\((native)\\)');


var _parseLine = function(line) {
    
    // "at Object.runMain (node.js:522:24)"
    // 'at ([^ ]+) \\(([^ ]+):([0-9]+):([0-9]+)\\)'
    m = line.match(r1);
    if (m) {
        return {
            'scope_name': m[1],
            'file_path': m[2],
            'line_number': 1 * m[3],
            'column_number': 1 * m[4]
        }
    }
    
    // "at node.js:772:9"
    // 'at ([^ ]+):([0-9]+):([0-9]+)'
    m = line.match(r2);
    if (m) {
        return {
            'file_path': m[1],
            'line_number': 1 * m[2],
            'column_number': 1 * m[3]
        }
    }
    
    // "at Object.parse (native)"
    // 'at ([^ ]+) \\((native)\\)'
    m = line.match(r3);
    if (m) {
        return {
            'scope_name': m[1],
            'file_name': 'native',
        }
    }
    
    return {}
};

var fromNodeException = function(e, opt) {
    
    opt = opt || {};
    
    var stack = null;
    if (e['stack']) {
        stack = [];
        var lines = e['stack'].split('\n');
        for (var i = 1, len = lines.length; i < len; i++) {
            stack.push(_parseLine(lines[i]));
        }
    }
    
    var ce = {
        'exception': {
            'name': e['name'] || null,
            'message': e['message'] || null,
            'stack': stack
        },
        'environment': {
            "execAgent": 'NodeJS ' + process.version,
            "execPath": process.execPath,
            "args": process.argv,
            "cwd": process.cwd(),
            "pid": process.pid,
            "gid": process.getgid(),
            "uid": process.getuid()
        }
    };
    
    if (opt.request) {
        var req = opt.request;
        ce['request'] = {
            'url': req.url,
            'method': req.method,
            'headers': req.headers
        };
    }
    
    return ce;
};

var fromBrowserException = function(e, opt) {
    
    opt = opt || {};
    
    var ce = common_exception_fromException(e)
    
    ce['exception']['at'] = Date().getTime();
    
    if (opt.request) {
        var userAgent = opt.request.headers['user-agent'];
        var referer = opt.request.headers['referer'];
        ce['environment'] = ce['environment'] || {};
        if (userAgent) {
            ce['environment']['execAgent'] = ce['environment']['execAgent'] || userAgent;
        }
        if (referer) {
            ce['environment']['execUrl'] = ce['environment']['url'] || referer;
        }
    }
    
    return ce;
};


exports['fromNodeException'] = fromNodeException;
exports['fromBrowserException'] = fromBrowserException;

