#!/usr/bin/python3

import os
import sys

needed_files = set()

for l in sys.stdin:
    if 'openat' not in l: continue
    if 'ENOENT' in l: continue
    l = l.split()
    if l[1].startswith('openat'):
        l = l[1:]
    needed_files.add(l[1])

cwd = os.getcwd()
prefix = 'venv/share/wenv/win64/dosdevices/c:/python-3.7.4.stable/'

needed_files = [os.path.normpath(f[1:-2]) for f in needed_files]
needed_files = [f[len(cwd)+1:] for f in needed_files if f.startswith(cwd)]
needed_files = {f for f in needed_files if f.startswith(prefix)}

existing_files = {os.path.join(root, name)[len(cwd)+1:]
                  for root, dirs, files in os.walk(cwd + '/' + prefix[:-1])
                  for name in files}

prune_dirs = ('PySide2',
              # 'numpy',  # numpy version depends on the python version, so don't trust our usage
              )
existing_files = {f
                  for d in prune_dirs
                  for f in existing_files
                  if ('/' + d + '/') in f}

delete_files = set([f for f in existing_files if f not in needed_files])

# which files are needed but don't exist?
#print([f for f in needed_files if f not in existing_files])
#print('existing', len(existing_files), 'delete', len(delete_files), 'needed', len(needed_files))

print('# AUTOGENERATED FILE')
print('# Removes excess files from PySide2 etc that are not needed for this program')
if len(delete_files) < len(existing_files) - 20:
    for f in sorted(delete_files):
        if ' ' not in f:
            print('rm venv/%s' % f[len(prefix):].replace('cpython-37', 'cpython-310'))
else:
    print(len(delete_files), len(existing_files))
