from __future__ import division,print_function
import sys
sys.dont_write_bytecode =True

# Copyright (c) <year>, <copyright holder>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# Lib.py

## Principles

### Shareable

+ Code starts with some open source license statement.
+ Code stored in some downloadable public space (e.g. Github).
+ Coded in some widely used language (e.g. Python) with extensive 
  on-line tutorialsl e.g. [Stackoverflow.com](http://stackoverflow.com/questions/tagged/python).

### Readable

#### Succinct

Not arcane, but lots of little short and useful code snippets.


#### Commented

Comments tell a story. Describe each function in terms
of some idiom (small thing) or pattern (larger thing)
describing something that someone else other than
the programmer might actually care about

Code written to be included into a two column paper:

+ All comments written in multiline strings and in 
  Pandoc style markdown.
      + File contains only one H1 header.
+ No line longer than 52 characters.  Which means
  for a language like Python:
    + _Self_ replaced with "_i_".
    + Indented with two characters.

### Sensible

Using Python 2.7 (cause of compatability issues).
Adopt the future `print` and `division`
functions. Do not write spurious _.pyc_ files.
For examples of the use of these idioms, see top of this file.

### Demo-able

A code file X.py may have an associated file Xeg.py
containing examples, demo, litle tutorials on how to use X.py.
If functions in Xeg.py are decorated with  `@go`, then
those functions will run just as a side-effect of loading that code. 
And if those functions print True and False then you can generate the world's
smallest test suite just by counting the percent True and Falses

"""
def go(f,ignoreErrors=True):
  doc= '# '+f.__doc__+"\n" if f.__doc__ else ""
  s='|'+'='*40 +'\n'
  print('\n==|',f.func_name + ' ' + s+doc)
  if ignoreErrors:
    try:
      f()
    except:
      print('Demo function',f,' did not crash: False')
  else: f()
  return f
"""

## Misc Utilities

### The Container Idiom

Just a place to store and update named slots.
When printed, any slot starting with "_"
is not shown. Any slot that is a function
name is displayed using it's function name.

"""
class o:
  def __init__(i,**d) : i.add(**d)
  def add(i,**d) : i.__dict__.update(**d); return i
  def __repr__(i) :
    f = lambda z: z.__class__.__name__ == 'function'
    name   = lambda z: z.__name__ if f(z) else z
    public = lambda z: not "_" is z[0]
    d    = i.__dict__
    show = [':%s=%s' % (k,name(d[k])) 
            for k in sorted(d.keys()) if public[k]]
    return '{'+' '.join(show)+'}'
"""

## The Settings Idiom

+ All  settings are stored in some global space so 
     + Optimizers have one place to go to adjust settings;
     + We have one place to go and print the options;
+ These settings can be set from multiple places all over the code
  using  a function decorated with "_@setting_".

"""
the=o()

def setting(f):
  def wrapper(**d):
    tmp = the[f.__name__] = f(**d)
    return tmp
  return wrapper
"""

For example, my code can now contain functions decorated by @setting
and all their values can be accessed via (e.g.) `the.GENIC.k`'or updated 
via (e.g.) `GENIC(k=100)`.

"""
@setting
def GENIC(**d): 
  def halfEraDivK(z): 
    return z.opt.era/z.opt.k/2
  return o(
    k     = 10,
    era   = 1000,
    buffer= 500,
    tiny  = halfEraDivK,
    num   = '$',
    klass = '=',
    seed  = 1).add(**d)
"""

@the
def ROWS(**d): return o(
  skip="?",
  sep  = ',',
  bad = r'(["\' \t\r\n]|#.*)'
  ).add(**d)
"""

## Misc stuff

### Random Stuff 

"""
rand= random.random
rseed= random.seed

def shuffle(lst): random.shuffle(lst); return lst
"""

### Print Stuff

`Say` prints without new lines.

"""
def say(**lst): print(', '.join(map(str,lst)),end="")
"""

`G` prints long numbers with just a few decimal places.
 
"""
def g(lst,n=3):
  for col,val in enumerate(lst):
    if isinstance(val,float): val = round(val,n)
    lst[col] = val
  return lst
"""

`Printm` prings a list of lists, aligning each column.

"""
def printm(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)

def data(row):
  for col in w.num:
    val = row[col]
    w.min[col] = min(val, w.min.get(col,val))
    w.max[col] = max(val, w.max.get(col,val))

"""

## The Era Pattern

Run over the data using a window of size _era_.  For
each era, shuffle the data order. Return one row at
a time. Flag if this is the first row. Return 
at least _want_ number of rows.

"""
def era(file, n=0):
  def chunks():
    chunk = []
    for row in rows(file):
      chunk += [row]
      if len(chunk) > the.ERA.size:
        yield chunk
        chunk=[]
    if chunk: yield chunk
  for chunk in chunks():
    for row in shuffle(chunk):
      n += 1
      yield n==0,row
      if n > the.ERA.want: return
  if n < the.ERA.want:
    for first,row in era(file,n):
      yield first,row
"""

## The Table Pattern

The first row contains header info. All other rows are data.
Yield all rows, after updating header and row data information.

"""

def table(file):
  t= t or o(nums=[],sym[],ords=[])
  for first, row in era(file):
    if first:
      header(row,t)
    else:
      data(row,t)
      yield t,row

def header(row,t):
  def numOrSym(val):
    return w.num if w.opt.num in val else w.sym
  def indepOrDep(val):
    return w.dep if w.opt.klass in val else w.indep
  for col,val in enumerate(row):
    numOrSym(val).append(col)
    indepOrDep(val).append(col)
    w.name[col] = val
    w.index[val] = col

def indep(w,cols):
  for col in cols:
    if col in w.indep: yield col

def rows(file):
  o = the.Rows
  def atom(x):
    try : return int(x)
    except ValueError:
       try : return float(x)
       except ValueError : return x
  def lines(): 
    n,kept = 0,""
    for line in open(file):
      now   = re.sub(w.bad,"",line)
      kept += now
      if kept:
        if not now[-1] == w.sep:
          yield n, map(atom, kept.split(w.sep))
          n += 1
          kept = "" 
  todo = None
  for n,line in lines():
    todo = todo or [col for col,name 
                    in enumerate(line) 
                    if not w.skip in name]
    yield n, [ line[col] for col in todo ]

def fuse(w,new,n):
  u0,u,dob,old = w.centroids[n]
  u1 = 1
  out = [None]*len(old)
  for col in w.sym:
    x0,x1 = old[col], new[col]
    out[col] = x1 if rand() < 1/(u0+u1) else x0
  for col in w.num:
    x0,x1= old[col], new[col]
    out[col] = (u0*x0 + u1*x1)/ (u0+u1)
  w.centroids[n] = (u0 + u1,u+u1, dob, out)

def more(w,n,row):
  w.centroids += [(1,1,n,row)]


def less(w,n) :
  b4 = len(w.centroids)
  w.centroids = [(1,u,dob,row) 
                 for u0,u,dob,row in w.centroids 
                 if u0 > w.opt.tiny(w)]
  print("at n=%s, pruning %s%% of clusters" % (
         n,  int(100*(b4 - len(w.centroids))/b4)))

def nearest(w,row):
  def norm(val,col):
    lo, hi = w.min[col], w.max[col]
    return (val - lo ) / (hi - lo + 0.00001)
  def dist(centroid):
    n,d = 0,0
    for col in indep(w, w.num):
      x1,x2 = row[col], centroid[col]
      n1,n2 = norm(x1,col), norm(x2,col)
      d    += (n1 - n2)**2
      n    += 1
    for col in indep(w, w.sym):
      x1,x2 = row[col],centroid[col]
      d    += (0 if x1 == x2 else 1)
      n    += 1
    return d**0.5 / n**0.5
  lo, out = 10**32, None
  for n,(_,_,_,centroid) in enumerate(w.centroids):
    d = dist(centroid)
    if d < lo:
      lo,out = d,n
  return out

def report(w,clusters):
  cols = w.index.keys()
  header = sorted(w.name.keys())
  header= [w.name[i] for i in header]
  matrix = [['gen','caughtLast',
              'caughtAll','dob'] + header]
  caught=0
  for m,(u0,u,dob,centroid) in enumerate(clusters):
    if u0 > w.opt.tiny(w):
      caught += u0
      matrix += [[m+1,u0,u,dob] + g(centroid,2)]
  print("\ncaught in last gen =%s%%\n" %
        int(100*caught/w.opt.era))
  printm(matrix)
  options = cached()
  for x in options: print(x,options[x])
  print("")

def genic(src='data/diabetes.csv',opt=None):
  w = o(num=[], sym=[], dep=[], indep=[],
        centroids=[],
        min={}, max={}, name={},index={},
        opt=opt or genic0())
  for n, row in table(src,w):
    data(w,row)
    if len(w.centroids) < w.opt.k:
      more(w,n,row)
    else:
      fuse(w,row,nearest(w,row))
      if not (n % w.opt.era):
        less(w,n)
  return w,sorted(w.centroids,reverse=True)

def _genic( src='data/diabetes.csv'):
  if len(sys.argv) == 2:
    src= sys.argv[1]
  opt=genic0(k=8)
  seed(opt.seed)
  report(*genic(src,opt)) 

if __name__ == '__main__': _genic()

"""
data/diabetes2.csv (1.5M records).
caught in last gen =77%

gen | caughtLast | caughtAll | dob     | $preg | $plas  | $pres | $skin | $insu  | $mass | $pedi | $age  | =class        
1   | 205        | 390       | 1571001 | 2.04  | 97.08  | 65.03 | 23.25 | 52.6   | 29.19 | 0.35  | 24.14 | testednegative
2   | 146        | 2408      | 1560001 | 3.77  | 117.73 | 74.08 | 0.79  | 3.86   | 31.04 | 0.4   | 31.84 | testedpositive
3   | 119        | 824       | 1566001 | 7.54  | 142.17 | 78.47 | 7.53  | 16.58  | 29.72 | 0.46  | 52.1  | testednegative
4   | 109        | 252       | 1571002 | 2.39  | 145.63 | 73.09 | 30.13 | 201.47 | 34.58 | 0.35  | 28.57 | testednegative
5   | 106        | 2690      | 1554001 | 8.03  | 106.6  | 76.56 | 32.07 | 64.18  | 34.63 | 0.41  | 40.84 | testednegative
6   | 85         | 654       | 1569002 | 1.62  | 118.5  | 70.76 | 33.44 | 119.23 | 36.16 | 0.93  | 26.23 | testedpositive
genic0 {:buffer=500 :era=1000 :k=8 :klass== :num=$ :seed=1 :tiny=halfEraDivK}
rows0 {:bad=(["\' \t\r\n]|#.*) :sep=, :skip=?}

real	3m25.949s
user	3m7.403s
sys	0m2.315s
"""
