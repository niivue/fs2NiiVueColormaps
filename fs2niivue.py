#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Convert FreeSurfer text color tables to NiiVue format
#Example 
# python lut2niivue.py /path/to/text/files

import numpy as np
import codecs, json, os
import sys
import glob

def lut2niivue(fsname):
    file1 = open(fsname, 'r')
    lines = file1.readlines()
    mxIdx = 0;
    validLines = [];
    for line in lines:
      if len(line) < 1:
        continue;
      if line.startswith('#'):
        continue;
      #each line should have six items:
      # index, name, R, G, B, A
      items = line.split()
      if len(items) < 6:
        continue;
      idx = int(items[0]);
      mxIdx = max(mxIdx, idx);
      validLines.append(line)

    js = {'R': [], 'G': [], 'B': [], 'A': [], 'I': [], 'labels': []}
    #fill all slots, as valid lines may be sparse and skip indices
    for i in range(mxIdx + 1):
      js['labels'].append('');
      js['R'].append(0);
      js['G'].append(0);
      js['B'].append(0);
      js['A'].append(255);
      js['I'].append(i);
    js['A'][0] = 0;
    for line in validLines:
      items = line.split()
      idx = int(items[0])
      js['labels'][idx] = items[1]
      js['R'][idx] = int(items[2])
      js['G'][idx] = int(items[3])
      js['B'][idx] = int(items[4])
      #js['A'][idx] = int(items[5])

    fnm = os.path.splitext(fsname)[0]+'.json'
    print(fnm)
    with open(fnm, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(json.dumps(js, indent=4, sort_keys=False, ensure_ascii=False))

if __name__ == '__main__':
    """Convert FreeSurfer colormaps to NiiVue
    Parameters
    ----------
    fname : str
        path to FreeSurfer files
    """
    pth = os.getcwd()
    if len(sys.argv) > 1:
        pth = sys.argv[1]
    os.chdir(pth)
    for file in glob.glob("*.txt"):
        fname = os.path.join(pth, file);
        lut2niivue(fname)
