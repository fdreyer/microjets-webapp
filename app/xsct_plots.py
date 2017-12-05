#!/usr/bin/env python
#
# plot pt integrated cross section as a function of R
#

import matplotlib.pyplot as plt
import re, numpy, string
from matplotlib.ticker import ScalarFormatter

# size to use for latex format
ltxsize = 14

def main():
    norm = 'LO'
    headers = ['NLO','NLO_mult','NLO.LLR_mB','NNLO.LLR_multB']
    fig = plot_vpt(0.2, 0.0, 1.0, False, headers, norm)
    fig.savefig('xsct_v_pt.png')
    fig = plot_vR(False, 0.0, 1.0, False, headers, norm)
    fig.savefig('xsct_v_R.png')
    plt.close(fig)

# this is taken from Gavin Salam's hfile.py
def get_array(file, regexp=None):
  """
  Returns a 2d array that contains the next block of numbers in this
  file (which can be a filehandle or a filename) 
  
  - if a regexp is provided, then first that is searched for
  - Subsequently, any line starting with a non-numeric character is ignored
  - The block ends the first time a blank line is encountered
  
  For data in the form
  
   1  1
   2  4
   3  9
  
  the resulting array will have the following contents
  
       array[:,0] = [1, 2, 3]
       array[:,1] = [1, 4, 9] 
  
  """
  # if file is a string, assume it's a filename, otherwise a filehandle
  if (isinstance(file,basestring)) : file = open(file, 'r')
  if (regexp != None)              : search(file,regexp)
  
  lines = []    # temporary store of lines, before conversion to array
  started = False
  while True:
    line = file.readline()
    if (not line)               : break        # empty line = end-of-file
    line = string.rstrip(line)                 # strips trailing blanks, \n
    line = string.lstrip(line)                 # strips leading blanks
    if (not line) :
      if (started) : break                     # empty line = end-of-block
      else         : continue                  
    if (not re.match('[-0-9]', line)) : continue
    lines.append(line)                         # collect the line
    started = True
  # do some basic error checking
  if (len(lines) < 1):
    raise Error("Block in get_array had 0 useful lines")
  # now we know the size, transfer the information to a numpy ndarray
  ncol = len(string.split(lines[0]))                
  num_array = numpy.empty( (len(lines), ncol) )
  for i in range(len(lines)):
    num_array[i,:] = string.split(lines[i])
  return num_array

    
# this is taken from Gavin Salam's hfile.py
def search(filehandle, regexp):
  """ looks through the file described by handle until it finds the regexp
  that's mentioned"""
  while True:
    line = filehandle.readline()
    if (line == "") : break        # empty line = end-of-file
    if (re.search(regexp,line)) : return filehandle
  return None

def rstr(R):
    "return the R value as a string with appropriate format"
    Rstr = '%1.1f' % (R)
    if (R < 0.1):
        Rstr = '%1.2f' % (R)
    return Rstr
    
def get_Rarray(fn, ymin, narrowband, header):
    "get array of cross section for different R values"
    hist_name=header
    if narrowband and exist_narrowband(header):
        hist_name='%s_narrowband' % (hist_name)
    hist_name='%s_y_%.1f' % (hist_name, ymin)
    #print (hist_name)    
    return get_array(fn,hist_name)

def exist_narrowband(header):
    "return true if header has both correlated and uncorrelated scale variation"
    if header in ['NLO_mult','NLO.LLR_mB','NNLO.LLR_multB','NNLO_mult']:
        return True
    return False

def get_ptarray(fn, R, ymin, narrowband, value):
    "get array of cross section for different pt values"
    Rstr=rstr(R)
    if (value == 'NLOPS' or value == 'NLOPS_hw6'):
        hist_name = 'R%s-y%1.1f-%1.1f' % (Rstr, ymin, ymin+0.5)
        return get_array(fn,hist_name)
    hist_name = 'y%1.1f-R%s-R01.0-allscales' % (ymin, Rstr)
    fh = open(fn, 'r')
    search(fh,hist_name)
    colnames=fh.readline().split()
    colcent,colmin,colmax = get_colname(value, narrowband)
    #print fn, hist_name
    icent = colnames.index(colcent)
    imin  = colnames.index(colmin)
    imax  = colnames.index(colmax)
    array=get_array(fh)
    #print colnames[icent], colnames[imin], colnames[imax]
    fh.close()
    return array[:,[0,1,2,icent,imin,imax]]

def get_style(header):
    "give a unique color/pattern for each line"
    edgecolor, pattern = {
        'NLO'             : ('#38B0DE',' '),
        'NLO_mult'        : ('#37BC61','xx'),
        'NLO.LLR_mB'      : ('#ff6020','\\'),
        'NLOPS'           : ('#000080','xx'),
        'NLOPS_hw6'       : ('#2F4F4F','xx'),
        'pseudo_NNLO'     : ('#9932CC',' '),
        'NNLO_mult'       : ('#608341','x'),
        'NNLO.LLR_multB'  : ('red'    ,'\\\\')
    }.get(header, ('black','/'))
    color='none'
    alpha=1.0
    if (pattern == ' '):
        alpha=0.3
        color=edgecolor
        edgecolor='none'
    return edgecolor,pattern,color,alpha

def get_key(header):
    "get a key for the legend"
    return{
        'NLO_mult'       : 'NLO mult.',
        'NLO.LLR_mB'     : 'NLO+LL$_R$',
        'NLOPS'          : 'POWHEG+Py8',
        'NLOPS_hw6'      : 'POWHEG+Hw6',
        'pseudo_NNLO'    : 'NNLO$_R$',
        'NNLO_mult'      : 'NNLO$_R$ mult.',
        'NNLO.LLR_multB' : 'NNLO$_R$+LL$_R$',
    }.get(header,header)

def get_colname(value, narrowband):
    "get the column name corresponding to value"
    s='alt_'
    if narrowband:
        s=''
    return{
        'LO' : \
         ('lo_exact_central','lo_exact_min','lo_exact_max'),
        'NLO' : \
         ('nlo_exact_central','nlo_exact_min','nlo_exact_max'),
        'NLO_mult' : \
         ('nlo_mult_central','nlo_mult_'+s+'min','nlo_mult_'+s+'max'),
        'NLO.LLR_mB' : \
         ('matched_mB_central','matched_mB_'+s+'min','matched_mB_'+s+'max'),
        'pseudo_NNLO' : \
         ('pseudo_nnlo_central','pseudo_nnlo_min','pseudo_nnlo_max'),
        'NNLO_mult' : \
         ('nnlo_mult_central','nnlo_mult_'+s+'min','nnlo_mult_'+s+'max'),
        'NNLO.LLR_multB' : \
         ('matched_nnlo_mB_central','matched_nnlo_mB_'+s+'min','matched_nnlo_mB_'+s+'max')
    }.get(value, ('central','min','max'))
 
def filename_vR(header, highpt, K):
    "get the filename corresponding to a given header and K value"
    fnhead = 'integrated'
    if highpt:
        fnhead = 'high_pt'
    filename = 'data/%s_xsct_simple.dat' % (fnhead)
    if (K > 1.0):
        filename = 'data/%s_xsct_simple_K%3.f.dat' % (fnhead, K*100)
    if (header=='NLOPS' or header=='NLOPS_hw6'):
        filename = 'data/%s_xsct_NLOPS_simple.dat' % (fnhead)
    return filename

def filename_vpt(header, R, y, K):
    "get the filename corresponding to a given header and bin"
    Rstr = rstr(R)
    filename = 'y%1.1f-R%s' % (y, Rstr)
    if (header=='NLOPS'):
        filename = 'data/dijet-powheg-FSR-ISR.res'
    elif (header=='NLOPS_hw6'):
        filename = 'data/dijet-powheg-herwig6-FSR-ISR.res'
    elif (K > 1.0):
        filename = 'data/matched-extended-K%3.f/%s' % (K*100,filename)
    else:
        filename = 'data/matched-extended/%s' % (filename)
    return filename
   
def plot_vR(highpt, ymin, K, narrowband, headers, norm):
    "plot the figure with R as x axis"
    fig=plt.figure(facecolor='white',figsize=(9,7))
    ax=fig.gca()
    ax.set_xlabel(r'$R$', size=ltxsize)
    ax.set_ylabel(r'$\sigma/\sigma^\mathrm{LO}$', size=ltxsize)
    ax.set_xscale('log')
    fn = filename_vR(norm, highpt, K)
    norm = get_Rarray(fn, ymin, narrowband, norm)[:,1]
    for header in headers:
        fn = filename_vR(header, highpt, K)
        Rvec = get_Rarray(fn, ymin, narrowband, header)
        ecol, pat, col, alp = get_style(header)
        key=get_key(header)
        if (header=='NLOPS' or header=='NLOPS_hw6'):
            plt.plot(Rvec[:,0], Rvec[:,1]/norm, linewidth=2.0,
                     color=col if col!='none' else ecol, label=key)
        else:
            plt.fill_between(Rvec[:,0], Rvec[:,2]/norm, Rvec[:,3]/norm, alpha=alp,
                             facecolor=col, hatch=pat, edgecolor=ecol, label=key)
            plt.plot(Rvec[:,0], Rvec[:,1]/norm, linewidth=2.0,
                     color=col if col!='none' else ecol)
    plt.grid(True)
    ax.set_xlim(0.08,1.)
    ax.set_ylim(0.0,1.6)
    ax.set_xticks([0.1,0.2,0.4,0.6,1])
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.legend(loc='lower right')
    xnote = 0.085
    ynote = 1.51
    dy = 0.08
    ptbin = get_ptbin(ymin, highpt)
    ptstr = r'$%i < p_t[\mathrm{GeV}] < %i$' % (ptbin[0],ptbin[1])
    ystr = '|y| < %1.1f' % (ymin+0.5)
    if (ymin > 0.0):
        ystr = '%1.1f < %s' % (ymin, ystr)
    ystr = r'$%s$' % (ystr)
    ax.annotate(ptstr,(xnote,ynote), size=ltxsize)
    ax.annotate(ystr, (xnote,ynote-dy), size=ltxsize)
    ax.annotate(r'$K = %1.2f$' % (K), (xnote, ynote-2*dy), size=ltxsize)
    return fig

def plot_vpt(R, ymin, K, narrowband, values, norm):
    "plot the figure with pt as x axis"
    fig=plt.figure(facecolor='white',figsize=(10,8))
    ax=fig.gca()
    ax.set_xlabel(r'$p_t$',size=ltxsize)
    ax.set_ylabel(r'$\sigma/\sigma^\mathrm{LO}$',size=ltxsize)
    ax.set_xscale('log')
    fn = filename_vpt(norm, R, ymin, K)
    norm = get_ptarray(fn, R, ymin, narrowband, norm)[:,3]
    for val in values:
        fn = filename_vpt(val, R, ymin, K)
        ptvec = get_ptarray(fn, R, ymin, narrowband, val)
        ecol, pat, col, alp = get_style(val)
        key=get_key(val)
        if (val=='NLOPS' or val=='NLOPS_hw6'):
            plt.plot(ptvec[:,1], ptvec[:,3]/norm, linewidth=2.0,
                     color=col if col!='none' else ecol, label=key)
        else:
            plt.fill_between(ptvec[:,1], ptvec[:,4]/norm, ptvec[:,5]/norm, alpha=alp,
                             facecolor=col, hatch=pat, edgecolor=ecol, label=key)
            plt.plot(ptvec[:,1], ptvec[:,3]/norm, linewidth=2.0,
                     color=col if col!='none' else ecol)
    plt.grid(True)
    ptmin,ptmax = get_ptrange(ymin)
    ax.set_ylim(0.0,1.8)
    ax.set_xticks([100,200,500,1000,2000])
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.set_xlim(ptmin,ptmax)
    xnote = ptmin*pow(ptmax/ptmin,0.975) #adjust automatically to log scale
    ynote = 1.7
    dy = 0.09
    ystr = '|y| < %1.1f' % (ymin+0.5)
    if (ymin > 0.0):
        ystr = '%1.1f < %s' % (ymin, ystr)
    ystr = r'$%s$' % (ystr)
    ax.annotate(r'$R = %s$' % (rstr(R)),(xnote,ynote), size=ltxsize, ha='right')
    ax.annotate(ystr, (xnote,ynote-dy), size=ltxsize, ha='right')
    ax.annotate(r'$K = %1.2f$' % (K), (xnote, ynote-2*dy), size=ltxsize, ha='right')
    ax.legend(loc='upper left')
    return fig

def get_ptrange(y):
    if (y > 2.0):
        return 100.0, 500.0
    elif (y > 1.5):
        return 100.0,1000.0
    return 100.0,2000.0

def get_ptbin(y, highpt):
    if (y > 2.0):
        ptbin = [376.0, 478.0]
    elif (y > 1.5):
        ptbin = [642.0, 894.0]
    elif (y > 1.0):
        ptbin = [894.0, 1992.0]
    elif (y > 0.5):
        ptbin = [1012.0, 1992.0]
    elif (y > 0.0):
        ptbin = [1310.0, 1992.0]
    else:
        ptbin = [1530.0, 1992.0]
    if not highpt:
        ptbin[0] = 100.0
    return ptbin

if __name__ == '__main__':
    main()

