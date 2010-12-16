
## Intro

*Common Exception* is a cross-language standard for representing an exception as a JSON object.

All fields are optional, and setting a field to <code>null</code> is considered equivalent to omitting it.

<pre>
{
    "name": "...",
    "message": "...",
    "stack": [
        {// most recent stack frame first
            "file_name": "",
            "file_path": "..."
            "file_url": "..."
            "file_sha1": "",        // hex
            "line_number": 100,     // 1-based
            "column_number": 23,    // 1-based
            "byte_offset_start": ,  // #bytes before relevant part
            "byte_offset": ,        // in [byte_offset_start, byte_offset_end]
            "byte_offset_end": ,    // byte_offset_start + len(relevant part)
            "scope_name": "",
            "line": "...line 100...",
            "lines_before": [..., "...98...", "...99..."],
            "lines_after": ["...101...", ...],
            "locals": {
                // Values intended to be human-readable, not machine-readable
                // Represent values as strings however you see fit, e.g.
                "i": "1729",
                "s": "'9000-char unicode gets trunca'...",
                "s": "b'9000-byte data gets trunca'...",
                "x": "&lt;__main__.Foo instance at 0x10057e128&gt;",
                "y": "[1, {2: \"foo\"}]",
            }
...
</pre>


This lets powerful open-source exception servers, e.g.

* [exception-server](https://github.com/andrewschaaf/exception-server)

and JavaScript widgets, e.g.

* exception-server's ExceptionWidget

focus on including awesome features, rather than a batallion of parsers.

## Integration Overview

### Python
<pre>
import common_exception
...
ce = common_exception.fromExceptionText(text)
...
except Exception:
    ce = common_exception.fromCurrentException()
</pre>

* Note: incomplete implementation not yet posted.

### Ruby

TODO

### JavaScript (NodeJS)
<pre>
var common_exception = require('common_exception');
...
var ce = common_exception.fromBrowserException(e);
...
catch(e) {
    var ce = common_exception.fromNodeException(e);
</pre>

### JavaScript (Browser)

<pre>
// Include <a href="https://github.com/andrewschaaf/common-exception/raw/master/javascript/browser-ce.min.js">browser-ce.min.js</a> (667 bytes) in your code's <a href="http://www.slideshare.net/jeresig/building-a-javascript-library/19">wrapper function</a>.
// It's of the form "var common_exception_fromException=..."
// so "common_exception_fromException" should minify easily
// e.g. with <a href="http://code.google.com/closure/compiler/">Closure Compiler</a>'s simple mode
// But if you're a JS size fanatic <i>&lt;high five!&gt;</i> you might want to just JSON
// the brower's exception and let your exception server convert it to CE
...
catch(e) {
    var ce = common_exception_fromException(e);
</pre>

<table style="border-spacing: 0;">
    <tr>
        <th></th>
        <th>Chrome</th>
        <th>Safari</th>
        <th>Firefox</th>
        <th>IE</th>
        <th>Opera</th>
    </tr>
    <tr>
        <td style="text-align: right">name</td>
<!-- Chrome--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!-- Safari--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!--Firefox--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!--     IE--><td style="text-align: center; background: #FFFFFF;">?</td>
<!--  Opera--><td style="text-align: center; background: #FFFFFF;">?</td>
    </tr>
    <tr>
        <td style="text-align: right">message</td>
<!-- Chrome--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!-- Safari--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!--Firefox--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!--     IE--><td style="text-align: center; background: #FFFFFF;">?</td>
<!--  Opera--><td style="text-align: center; background: #FFFFFF;">?</td>
    </tr>
    <tr>
        <td style="text-align: right"># frames</td>
<!-- Chrome--><td style="text-align: center; background: #C0F5BC;">all</td>
<!-- Safari--><td style="text-align: center; background: #F6F0A6;"><b>one</b></td>
<!--Firefox--><td style="text-align: center; background: #C0F5BC;">all</td>
<!--     IE--><td style="text-align: center; background: #FFFFFF;">?</td>
<!--  Opera--><td style="text-align: center; background: #FFFFFF;">?</td>
    </tr>
    <tr>
        <td style="text-align: right">file_url</td>
<!-- Chrome--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!-- Safari--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!--Firefox--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!--     IE--><td style="text-align: center; background: #FFFFFF;">?</td>
<!--  Opera--><td style="text-align: center; background: #FFFFFF;">?</td>
    </tr>
    <tr>
        <td style="text-align: right">line_number</td>
<!-- Chrome--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!-- Safari--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!--Firefox--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!--     IE--><td style="text-align: center; background: #FFFFFF;">?</td>
<!--  Opera--><td style="text-align: center; background: #FFFFFF;">?</td>
    </tr>
    <tr>
        <td style="text-align: right">column_number</td>
<!-- Chrome--><td style="text-align: center; background: #C0F5BC;">yes</td>
<!-- Safari--><td style="text-align: center; background: #F6F0A6;"><b>via offset</b></td>
<!--Firefox--><td style="text-align: center; background: #EAAFAE;"><b>no</b></td>
<!--     IE--><td style="text-align: center; background: #FFFFFF;">?</td>
<!--  Opera--><td style="text-align: center; background: #FFFFFF;">?</td>
    </tr>
</table>


## Efficient encodings

### Protobuf

TODO common_exception.proto

### Thrift

TODO common_exception.thrift

