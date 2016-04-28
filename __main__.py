#!/usr/bin/python

import hashlib, os, shutil, sys, tarfile
from subprocess import call, check_call
from pprint import pprint
from cypher import Cypher


### will create backup in ~/tmp and extract results
debug=True

# root directories
rootdir = os.path.abspath(os.sep)
homedir = os.path.expanduser('~') 


##### encryption proof of concept


tmpdir = os.path.join(homedir, 'tmp')
os.chdir(os.path.join(homedir, 'tmp'));
filename = 'home.tgz'

# get password
password = 'foobar'
# encrypt password
hashed = hashlib.md5(password).hexdigest()
offset = len(encrypted)

# get file contents
filecontents = open(filename).read()
# encode file contents based on password
cypher = Cypher(password)
encodedfile = cypher.encode(filecontents)

# concatenate encrypted password with encoded file
simplecrypt = hashed + encodedfile

with open(filename+'.sc', "w") as text_file:
    text_file.write(simplecrypt)

## opening
# separate hashed password from encoded file (based on length of hashed password)
# verify hashed password is same as user supplied when hashed
# use password to decode encoded file

exit()

#####



### set up app directory, if not set up
appdir = os.path.join(homedir, '.bkup')
if not os.path.exists(appdir):
	print('* Creating ~/.bkup directory')
	os.makedirs(appdir)
    
# create template config file, if it does not exist
configfile = os.path.join(appdir, 'config')
template="""import os

homedir = os.path.expanduser('~') 

profiles = {
	'home': {
		'backupdir': homedir,
		'destdir': os.path.join(homedir, 'tmp'),
		'files': [
		]
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
	if os.path.exists(destdir):
		shutil.rmtree(destdir)

# verify destination directory exists		
os.makedirs(destdir)

## go to back up direcroty
os.chdir(config['backupdir'])


## wrap it up (create g-zipped tarball)
tar = tarfile.open(backupfile, "w:gz")
for name in config['files']:	
	tar.add(name)
tar.close()


## move archive to destination
shutil.move(backupfile, os.path.join(destdir, backupfilename))


## if debugging, go to destdir (tmp) and unzip results
if debug:
	os.chdir(destdir)
	tar = tarfile.open(backupfilename, "r:gz")
	tar.extractall()
