# Builds index.html by embedding engine.py, so the page and the repo show the same Python.
import html
engine = open('engine.py').read()
tpl = open('template.html').read()
open('index.html','w').write(tpl.replace('%%ENGINE%%', html.escape(engine)))
print('built', len(engine), 'chars of python embedded')
