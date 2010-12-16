
import sys, os, re


def main():
    
    # Check prereqs
    if not (os.environ.get('CLOSURE_JAR') and os.path.isfile(os.environ.get('CLOSURE_JAR'))):
        fatalError('You need to get Closure Compiler and have $CLOSURE_JAR point to its .jar')
    try:
        import pj.api
    except ImportError:
        fatalError("'import pj.api' failed. Install http://pyxc.org")
    
    log('Loading...')
    with open('common-exception.js', 'rb') as f:
        js = unicode(f.read(), 'utf-8')
    js = re.search(r'/\* Begin browser part \*/(?:.|\n)+/\* End browser part \*/', js).group(0)
    
    log('Compiling...')
    js = pj.api.closureCompile(js, 'simple')
    
    log('Saving...')
    with open('browser-ce.min.js', 'wb') as f:
        f.write(js.encode('utf-8'))
    
    log('Done.')

def log(msg):
    sys.stderr.write(msg + '\n')
    sys.stderr.flush()

def fatalError(msg):
    print(msg)
    sys.exit(1)


if __name__ == '__main__':
    main()
