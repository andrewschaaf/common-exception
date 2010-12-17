
import re, time


def fromExceptionText(text):
    #<pre>
    #Traceback (most recent call last):
    #  File "test.py", line 15, in <module>
    #    main()
    #  File "test.py", line 11, in main
    #    f()
    #  File "test.py", line 8, in f
    #    g()
    #  File "test.py", line 5, in g
    #    raise Exception('OMG NOES')
    #Exception: OMG NOES
    #</pre>
    
    #<pre>
    #  File "<stdin>", ...
    #</pre>
    
    t1 = time.time()
    
    ex = {}
    
    lines = re.split(r'(?:(?:\n)|(?:\r\n?))', text.strip())
    m = re.search(r'([^:]+):? ?(.*)', lines[-1])
    
    assert lines[0] == 'Traceback (most recent call last):'
    assert len(lines) % 2 == 0
    
    ex['name'] = m.group(1)
    if m.group(2):
        ex['message'] = m.group(2)
    
    ex['stack'] = []
    for i in range((len(lines) - 2) / 2):
        fileLine = lines[2 * i + 1]
        codeLine = lines[2 * i + 2]
        m = re.search(r'File "(.*)", line ([0-9]+)(?:, in )?(.*)', fileLine)
        ex['stack'].append({
            'file_path': m.group(1),
            'line_number': int(m.group(2)),
            'scope_name': m.group(2) if m.group(2) else None,
            'line': codeLine.lstrip(),
        })
    
    return {
        'exception': ex,
        'ms_to_create': int((time.time() - t1) * 1000),
    }



def fromCurrentException():
    raise NotImplementedError


