## Chrome
<pre>
name: "ReferenceError"
message: "undef is not defined"

// 4-space. "\n"s added for clarity
stack: "ReferenceError: undef is not defined\n
    at file:///Users/a/Desktop/foo.html:11:7\n
    at file:///Users/a/Desktop/foo.html:15:7\n
    at file:///Users/a/Desktop/foo.html:24:9\n
    at file:///Users/a/Desktop/foo.html:37:141\n
    at onload (file:///Users/a/Desktop/foo.html:38:4)"

type: "not_defined"
arguments: ["undef"]
</pre>

## Safari
<pre>
name: "ReferenceError"
message: "Can't find variable: undef"

sourceURL: "file:///Users/a/Desktop/foo.html"
line: 11

sourceId: 4673926280
expressionBeginOffset: 44
expressionCaretOffset: 49
expressionEndOffset: 49
</pre>

## Firefox
<pre>
name: "ReferenceError"
message: "undef is not defined"

fileName: "file:///Users/a/Desktop/foo.html"
lineNumber: 11

// 0-space. "\n"s added for clarity
stack:"()@file:///Users/a/Desktop/foo.html:11\n
()@file:///Users/a/Desktop/foo.html:15\n
()@file:///Users/a/Desktop/foo.html:24\n
onload([object Event])@file:///Users/a/Desktop/foo.html:1\n
"
</pre>
