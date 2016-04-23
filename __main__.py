#!/usr/bin/python

import os, shutil, sys
from subprocess import call, check_call
from pprint import pprint

homedir = os.path.expanduser('~') 

appdir = os.path.join(homedir, '.bkup')

configfile = os.path.join(appdir, 'config')

tmpdir = os.path.join(appdir, 'tmp')
if not os.path.exists(tmpdir):
    os.makedirs(tmpdir)

# ### clear the destination directory prior to each run (caveat emptor)
# cleardestdir=True

# ## file name (no path) of gunzipped tarball
# backupfile='home.tgz'
# ## backup directory
# backupdir=homedir
# ## where to move tgz file
# destdir=os.path.join(homedir, 'tmp')

def write_list_to_file(fl, ls):
	with open(fl, 'w') as out_file:
	    out_file.write('\n'.join(ls))

def write_lists_to_files(file2list):
	for fl, ls in enumerate(file2list):
		print(fl)
		write_list_to_file(fl, ls)

defaults = {
	'cleardestdir': True,
	'backupfile': 'home.tgz',
	'backupdir': homedir,
	'destdir': os.path.join(homedir, 'tmp'),
	'includes': ['./.git-completion.bash','./.gitconfig','./test/a','./test/one.txt','./test/b/c.txt','./Code/provision/'],
	'excludes': ['./test/a/b.txt', '*.git']
}

sys.path.append(os.path.dirname(os.path.expanduser(configfile)))
from config import config

pprint(config)

# config={}

# config.update(defaults)

## include patterns
# includefile=os.path.join(homedir, '.backup-include')
# includes = ['./.git-completion.bash','./.gitconfig','./test/a','./test/one.txt','./test/b/c.txt','./Code/provision/']
includefile=os.path.join(tmpdir, 'include')
write_list_to_file(includefile, config['includes'])

## exclude patterns
# excludefile=os.path.join(homedir, '.backup-exclude')
# excludes=['./test/a/b.txt', '*.git']
excludefile=os.path.join(tmpdir, 'exclude')
write_list_to_file(excludefile, config['excludes'])

# write_lists_to_files({
# 	includefile: includes,
# 	excludefile: excludes
# })

## tar commands based on tar implemntation (gnu or bsd)
tar_gnu_str="tar -czvf "+config['backupfile'] +" --files-from="+includefile+" --exclude-from=" + excludefile
tar_gnu=tar_gnu_str.split(' ')
# tar_gnu=['tar', '-czvf', config['backupfile'], '--files-from='+includefile,  '--exclude-from='+excludefile]

tar_bsd="tar -czvf $backupfile --include-from=$includefile --exclude-from=$excludefile"



if config['cleardestdir']:
	# rm -rf $destdir/*
	shutil.rmtree(config['destdir'])
	os.mkdir(config['destdir'])

# ## go to back up direcroty
# cd $backupdir
os.chdir(config['backupdir'])


pprint(tar_gnu_str)
# ## wrap it up (create g-zipped tarball)
# $tar_gnu || $tar_bsd
call(tar_gnu)

# ## move archive to destination
# mv $backupfile ['destdir']/
shutil.move(config['backupfile'], config['destdir'])

# #### this part is for debugging, you could impement backup rotations, etc. here

# cd ['destdi']r
os.chdir(config['destdir'])

# ## extract the archive
# tar xzvf $backupfile
call(["tar", "xzvf", config['backupfile']])

# remove tmp dir
shutil.rmtree(tmpdir)