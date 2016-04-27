#!/usr/bin/python

import os, shutil, sys, tarfile
from subprocess import call, check_call
from pprint import pprint

### 
debug=False

rootdir = os.path.abspath(os.sep)

### set up app directory, if not set up
homedir = os.path.expanduser('~') 
appdir = os.path.join(homedir, '.bkup')
if not os.path.exists(appdir):
	print('* Creating ~/.bkup directory')
	os.makedirs(appdir)
    

configfile = os.path.join(appdir, 'config')
template="""import os

homedir = os.path.expanduser('~') 

profiles = {
	'home': {
		'backupdir': homedir,
		'destdir': os.path.join(homedir, 'tmp'),
		'files': []
	}	
}
"""
if not os.path.exists(configfile+'.py'):
	with open(configfile+'.py', "w") as text_file:
		print('* Creating ~/.bkup/config.py template file')
		text_file.write(template)


## load profiles
sys.path.append(os.path.dirname(os.path.expanduser(configfile)))
from config import profiles

## arguments
if len(sys.argv) != 2:
	print("Usage: bkup <profile>. Configured profiles are: "+', '.join(profiles.keys()))
	exit(1)


##  set up profiles
defaults = {
	'backupdir': homedir,
	'destdir': os.path.join(homedir, 'tmp'),
	'files': ['./.git-completion.bash','./.gitconfig','./test/a','./test/one.txt','./test/b/c.txt','./Code/provision/']
}
profile = sys.argv[1]
backupfilename = profile+'.tgz'
backupfile=os.path.join(rootdir, 'tmp', backupfilename)
if not profile in profiles.keys():
	print("Error: Invalid profile, '"+profile+"'. Configured profiles are: "+', '.join(profiles.keys()))
	exit(1)
config = profiles[profile]
for key in defaults.keys():
	if not key in config:
		config[key] = defaults[key]

if len(config['files']) == 0:
	print('* File list is empty for '+profile+' add files to the profile in ~/.bkup/config.py')
	exit(0)

## if debugging, use ~/tmp as destdir and clear it
destdir = config['destdir']
if debug:
	destdir=os.path.join(homedir, 'tmp')
	shutil.rmtree(destdir)
	os.mkdir(destdir)


## go to back up direcroty
os.chdir(config['backupdir'])


## wrap it up (create g-zipped tarball)
tar = tarfile.open(backupfile, "w:gz")
for name in config['files']:	
	tar.add(name)
tar.close()

## create destdir it it doesn't exist
if not os.path.exists(destdir):
	os.mkdir(destdir)

## move archive to destination
shutil.move(backupfile, os.path.join(destdir, backupfilename))


## if debugging, go to destdir (tmp) and unzip results
if debug:
	os.chdir(destdir)
	call(["tar", "xzvf", os.path.join(destdir, backupfile)])
