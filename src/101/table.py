from __future__ import division,print_function
import sys
sys.dont_write_bytecode=True

from lib import *
from counts import *

@setting
def TABLE(**d): return o(
    num   = '$',
    int   = '!',
    klass = '=',
    skip  = "?",
    sep   = ',',
    more  = '>',
    less  = '<',
    bad   =  r'(["\' \t\r\n]|#.*)',
    era   = 256,
    shuffle=True,
  ).add(**d)

def memo2(f):
  name = f.__name__
  def wrapper(i,j):
    if i.cache is None:
      i.cache={}
    if id(i) > id(j):
      i,j = j,i
    key = (name, id(i), id(j))
    if not key in i.cache:
      i.cache[key] = f(i,j)
    return i.cache[key]
  return wrapper

class Row:
  id=0
  def __init__(i,cells=[],t=None):
    Row.id = i.id = Row.id + 1
    i.cache = None
    i.cells = cells
    i.table = t
    i.table.n += 1
    if t:
      for cell,value in zip(t.all,cells):
        if value is not the.TABLE.skip:
          cell += value
  def __getitem__(i,k): return i.cells[k]
  def __hash__(i)     : return i.id
  def __repr__(i): return '<'+str(i.cells)+'>'
  @memo2
  def dist(i,j):
    skip = lambda z: z == the.TABLE.skip
    n = all = 0
    for v1,v2,hdr in cells2(i,j,i.table.indep):
      if skip(v1): v1 = hdr.far(v2)
      if skip(v2): v2 = hdr.far(v1)
      if the.TABLE.skip:
        v1 = hdr.norm(v1)
        v2 = hdr.norm(v2)
      n   += 1
      all += hdr.dist(v1,v2) 
    return all**0.5 / (n+0.000001)**0.5
    
import re
def rows(file):
  def use(z): return not the.TABLE.skip in z
  def what(z):
    if the.TABLE.num in z: return float
    if the.TABLE.int in z: return int
    return noop
  def todos(line):
    return [(col,what(name)) for col,name 
            in enumerate(line) if use(name)]
  def lines(): 
    kept = ""
    for line in open(file):
      now   = re.sub(the.TABLE.bad,"",line)
      if now:
        kept += now
        if kept:
          if not now[-1] == the.TABLE.sep:
            yield kept.split(the.TABLE.sep)
            kept = "" 
  todo = None
  for line in lines():
    if todo:
      line = [ comp(line[col]) for col,comp in todo ]
    else:
      todo = todos(line)
      line = [ txt for txt in line if use(txt)]
    yield line
"""

## The Era Pattern

Run over the data using a window of size _era_.  For
each era, shuffle the data order. Return one row at
a time. Flag if this is the first row. Return 
at least _want_ number of rows.

"""
def eras(file,size=None):
  t = table0()
  size = size or the.TABLE.era
  def chunks():
    chunk = []
    for row in rows(file):
      if not t.all:
         header(row,t)
      else:
        chunk += [Row(row,t)]
        if len(chunk) >= size:
          yield chunk
          chunk=[]
    if chunk: yield chunk
  era=0
  for chunk in chunks():
    if the.TABLE.shuffle:
      chunk = shuffle(chunk)
    yield t,chunk,era
    era += 1
"""

## The Table Pattern

The first row contains header info. All other rows are data.
Yield all rows, after updating header and row data information.

"""
def table0():
  return o(num=[],sym=[],ord=[],
           more=[],less=[],klass=[],inSym=[], inNum=[],
           n=0,rows=[],
           indep=[],dep=[],all=[])

def header(row,t=None):
  t = t or table0()
  opt = the.TABLE
  t["spec"]= row
  def dep(z) :
    return  opt.klass in z or \
            opt.less  in z or  \
            opt.more  in z
  for col,txt in enumerate(row):
    (klass,at)   = ((N,t.num) if   opt.num in txt
                              else (S,t.sym))
    header       = klass()
    header.name  = txt
    header.col   = col
    at          += [header]
    (t.dep if dep(txt) else t.indep).append(header)
    if opt.klass in txt : t.klass += [header]
    if opt.more  in txt : t.more  += [header]
    if opt.less  in txt : t.less  += [header]
    t.all += [header]
  for z in t.indep:
    (t.inNum if   isinstance(z,N)
             else t.inSym).append(z)
  return t

def theKlass(t,row): return row[t.klass[0].col]

def theKlasses(t,rows):
  return [theKlass(t,row) for row in rows]

def cells(row,headers):
  for header in headers:
    cell = row[header.col]
    if cell is not the.TABLE.skip:
      yield cell,header

def cells2(row1,row2,headers):
  skip = lambda z: z == the.TABLE.skip
  for header in headers:
    v1 = row1[header.col]
    v2 = row2[header.col]
    if not (skip(v1) and skip(v2)):
      yield v1, v2, header
