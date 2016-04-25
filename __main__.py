#!/usr/bin/python

import os, shutil, sys, tarfile
from subprocess import call, check_call
from pprint import pprint

### 
debug=True


homedir = os.path.expanduser('~') 

appdir = os.path.join(homedir, '.bkup')
if not os.path.exists(appdir):
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
		text_file.write(template)


defaults = {
	'backupdir': homedir,
	'destdir': os.path.join(homedir, 'tmp'),
	'files': ['./.git-completion.bash','./.gitconfig','./test/a','./test/one.txt','./test/b/c.txt','./Code/provision/']
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



if debug:
	# rm -rf $destdir/*
	shutil.rmtree(config['destdir'])
	os.mkdir(config['destdir'])

# ## go to back up direcroty
# cd $backupdir
os.chdir(config['backupdir'])


## wrap it up (create g-zipped tarball)
tar = tarfile.open(backupfile, "w:gz")
for name in config['files']:	
	tar.add(name)
tar.close()

destdir = config['destdir']
if debug:
	destdir=os.path.join(homedir, 'tmp')

if not os.path.exists(destdir):
	os.path.mkdir(destdir)

# ## move archive to destination
shutil.move(backupfile, config['destdir'])

# #### this part is for debugging, you could impement backup rotations, etc. here

# cd destdir
if debug:
	os.chdir(config['destdir'])
	call(["tar", "xzvf", os.path.join(config['destdir'], backupfile)])
