from __future__ import division,print_function
import sys
sys.dont_write_bytecode =True

"""
# Defining columns

"""
from lib import *
"""

### `Col`: Generic Columns

`Col`umns keep track of what was seen in a column.
The general idea is that:

+  _Before_ you start reading data,
   you create one `Col` for each column. 
+ _After_ the data has been read, a column can be
   `ask()`ed  for a representative on what
   values have been observed.
+  _While_ reading data, the columns peek at each
   seen value (and update their information accordingly).
   This is called `tell()`ing the column about a value.

"""
class Col:
  def tell(i,x):
    if x is None or x == the.COL.missing:
      return x
    i.n += 1
    i.tell1(i,x)
    return x
"""

Also, you can ask a `Col` for:

+ The distance between two col values (normalized 0 to 1)
+ A `logger()`; i.e
  a new column for storing things like this column.

Finally, a `Col` can tell you how `likely()` is some
value, given the `tell()`ed values of that column.

## `S`: Columns of Symbols

Tracks the frequency counts of the `tell()`ed symbols.
Can report the entropy `ent()` of that distribution
(which is a measure of the diversity of those symbols).

"""
class S(Col): 
  def __init__(i,all=None,name=''): 
    i.all = all or {}
    i.n = 0
    i.name = str(name)
  def tell1(i,x)  : 
    i.all[x] = i.all.get(x,0) + 1
  def ask(i)     : return(ask(i.all.keys()))
  def dist(i,x,y): return 0 if x==y else 1
  def norm(i,x)  : return x
  def logger(i)  : return S(name=i.name)
  def ent(i):
    e=0
    for key,value in i.all.items():
      if value > 0:
        p = value/i.n
      e -= p*log(p,2)
    return e
  def likely(i,x,prior):
    m = the.COL.m
    return (i.all.get(x,0) + m*prior)/(i.n + m)
"""
    
In `likely()`, the `prior` value is some used in a Naive Bayes
classifier (details later).


## `N`: Columns of Numbers

Numeric columns track the `lo` and `hi` of the `tell()`ed
numbers as well as their mean `mu` and standard deviation
`sd()`.

`N`s  also keep `kept()` a random sampling
of the numbers (up to a max of `the.COL.buffer` numbers).
 
"""
class N(Col):
  def __init__(i,init=[],lo=None,hi=None,name=''):
    i.n, i.lo, i.hi, i.name = 0,lo,hi,str(name)
    i._kept = [None]*the.COL.buffer
    i.mu = i.m2= 0
    map(i.tell,init)
  def ask(i)     : return i.lo + r()*(i.hi - i.lo)
  def dist(i,x,y): return i.norm(x) - i.norm(y)
  def logger(i): 
    return N(name=i.name,lo=i.lo,hi=i.hi)
  def tell1(i,x):
    if i.lo is None: i.lo = x
    if i.hi is None: i.hi = x
    i.lo, i.hi = min(i.lo,x), max(i.hi,x)
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
    l = len(i._kept)
    if r() <= l/i.n: i._kept[ int(r()*l) ]= x
  def sd(i):
    if i.n < 2: return 0
    return (max(0,i.m2)/(i.n - 1))**0.5
  def kept(i): 
    return [x for x in i._kept if x is not None]
  def norm(i,x):
    tmp =(x - i.lo) / (i.hi - i.lo + 0.00001)
    return max(0,min(tmp,1))
  def __repr__(i): 
    return '{:%s #%s [%s .. %s]}'%(
      i.name,i.n,i.lo ,i.hi)
  def likely(i,x,prior):
    return normpdf(x,i.mu.i.sd())
