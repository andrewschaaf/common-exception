
import re, time, sys, os, warnings, traceback, json


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
    
    t1_ms = int(time.time() * 1000)
    
    # TODO: heed warning at http://docs.python.org/library/sys.html#sys.exc_info
    exc_type, exc_value, tback = sys.exc_info()
    
    if exc_type is None:
        return None
    
    ex = {'at': t1_ms}
    
    # name
    ex['name'] = unicode(exc_type.__name__)
    
    # message
    try:
        with warnings.catch_warnings(record=True) as w:
            ex['message'] = exc_value.message
    except Exception:
        ex['message'] = repr(exc_value)
    
    
    reversed_frames = []
    while tback is not None:
        locs = tback.tb_frame.f_locals
        frame = {
            'file_path': tback.tb_frame.f_code.co_filename,
            'scope_name': tback.tb_frame.f_code.co_name,
            'line_number': tback.tb_lineno,
            'locals': dict((k, shortRepr(locs[k])) for k in locs)
        }
        tback = tback.tb_next
        reversed_frames.append(frame)
    
    ex['stack'] = list(reversed(reversed_frames))
    
    return {
        'exception': ex,
        'ms_to_create': int(time.time() * 1000) - t1_ms,
        'environment': {
            'execAgent': 'Python ' + json.dumps(sys.version_info),
            'execPath': sys.executable,
            'args': sys.argv,
            'cwd': os.getcwd(),
            'pid': os.getpid(),
            'gid': os.getgid(),
            'uid': os.getuid(),
        }
    }


def shortRepr(x, maxlen=50):
    s = repr(x)
    if len(s) > maxlen:
        s = s[:maxlen - 3] + '...'
    return s


'''

traceback.h
    typedef struct _traceback {
        PyObject_HEAD
        struct _traceback *tb_next;
        struct _frame *tb_frame;
        int tb_lasti;
        int tb_lineno;
    } PyTracebackObject;

frameobject.h
    typedef struct _frame {
        PyObject_VAR_HEAD
        struct _frame *f_back;	/* previous frame, or NULL */
        PyCodeObject *f_code;	/* code segment */
        PyObject *f_builtins;	/* builtin symbol table (PyDictObject) */
        PyObject *f_globals;	/* global symbol table (PyDictObject) */
        PyObject *f_locals;		/* local symbol table (any mapping) */
        PyObject **f_valuestack;	/* points after the last local */
        /* Next free slot in f_valuestack.  Frame creation sets to f_valuestack.
           Frame evaluation usually NULLs it, but a frame that yields sets it
           to the current stack top. */
        PyObject **f_stacktop;
        PyObject *f_trace;		/* Trace function */

        /* If an exception is raised in this frame, the next three are used to
         * record the exception info (if any) originally in the thread state.  See
         * comments before set_exc_info() -- it's not obvious.
         * Invariant:  if _type is NULL, then so are _value and _traceback.
         * Desired invariant:  all three are NULL, or all three are non-NULL.  That
         * one isn't currently true, but "should be".
         */
        PyObject *f_exc_type, *f_exc_value, *f_exc_traceback;

        PyThreadState *f_tstate;
        int f_lasti;		/* Last instruction if called */
        /* Call PyFrame_GetLineNumber() instead of reading this field
           directly.  As of 2.3 f_lineno is only valid when tracing is
           active (i.e. when f_trace is set).  At other times we use
           PyCode_Addr2Line to calculate the line from the current
           bytecode index. */
        int f_lineno;		/* Current line number */
        int f_iblock;		/* index in f_blockstack */
        PyTryBlock f_blockstack[CO_MAXBLOCKS]; /* for try and loop blocks */
        PyObject *f_localsplus[1];	/* locals+stack, dynamically sized */
    } PyFrameObject;

code.h
    /* Bytecode object */
    typedef struct {
        PyObject_HEAD
        int co_argcount;		/* #arguments, except *args */
        int co_nlocals;		/* #local variables */
        int co_stacksize;		/* #entries needed for evaluation stack */
        int co_flags;		/* CO_..., see below */
        PyObject *co_code;		/* instruction opcodes */
        PyObject *co_consts;	/* list (constants used) */
        PyObject *co_names;		/* list of strings (names used) */
        PyObject *co_varnames;	/* tuple of strings (local variable names) */
        PyObject *co_freevars;	/* tuple of strings (free variable names) */
        PyObject *co_cellvars;      /* tuple of strings (cell variable names) */
        /* The rest doesn't count for hash/cmp */
        PyObject *co_filename;	/* string (where it was loaded from) */
        PyObject *co_name;		/* string (name, for reference) */
        int co_firstlineno;		/* first source line number */
        PyObject *co_lnotab;	/* string (encoding addr<->lineno mapping) See
    				   Objects/lnotab_notes.txt for details. */
        void *co_zombieframe;     /* for optimization only (see frameobject.c) */
        PyObject *co_weakreflist;   /* to support weakrefs to code objects */
    } PyCodeObject;

'''


