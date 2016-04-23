#!/usr/bin/python

import os, shutil, sys
from subprocess import call, check_call
from pprint import pprint

### clear the destination directory prior to each run (caveat emptor)
cleardestdir=True


homedir = os.path.expanduser('~') 

appdir = os.path.join(homedir, '.bkup')
if not os.path.exists(appdir):
    os.makedirs(appdir)

configfile = os.path.join(appdir, 'config')

tmpdir = os.path.join(appdir, 'tmp')
if not os.path.exists(tmpdir):
    os.makedirs(tmpdir)

def write_list_to_file(fl, ls):
	with open(fl, 'w') as out_file:
	    out_file.write('\n'.join(ls))

defaults = {
	'backupdir': homedir,
	'destdir': os.path.join(homedir, 'tmp'),
	'includes': ['./.git-completion.bash','./.gitconfig','./test/a','./test/one.txt','./test/b/c.txt','./Code/provision/'],
	'excludes': ['./test/a/b.txt', '*.git']
}

sys.path.append(os.path.dirname(os.path.expanduser(configfile)))
from config import profiles

if len(sys.argv) != 2:
	print("usage: bkup <profile>. Configured profiles are: "+', '.join(profiles.keys()))
	exit(1)

profile = sys.argv[1]
backupfile=profile+'.tgz'

if not profile in profiles.keys():
	print("Error: Invalid profile, '"+profile+"'. Configured profiles are: "+', '.join(profiles.keys()))
	exit(1)

config = profiles[profile]
for key in defaults.keys():
	if not key in config:
		config[key] = defaults[key]

## include patterns
includefile=os.path.join(tmpdir, 'include')
write_list_to_file(includefile, config['includes'])

## exclude patterns
excludefile=os.path.join(tmpdir, 'exclude')
write_list_to_file(excludefile, config['excludes'])

## tar commands based on tar implemntation (gnu or bsd)
tar_gnu_str="tar -czvf "+backupfile +" --files-from="+includefile+" --exclude-from=" + excludefile
tar_gnu=tar_gnu_str.split(' ')
# tar_gnu=['tar', '-czvf', backupfile, '--files-from='+includefile,  '--exclude-from='+excludefile]

# tar_bsd="tar -czvf $backupfile --include-from=$includefile --exclude-from=$excludefile"
tar_bsd_str="tar -czvf "+backupfile +" --include-from="+includefile+" --exclude-from=" + excludefile
tar_bsd=tar_bsd_str.split(' ')


if cleardestdir:
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
shutil.move(backupfile, config['destdir'])

# #### this part is for debugging, you could impement backup rotations, etc. here

# cd ['destdi']r
os.chdir(config['destdir'])

# ## extract the archive
# tar xzvf $backupfile
call(["tar", "xzvf", backupfile])

# remove tmp dir
shutil.rmtree(tmpdir)