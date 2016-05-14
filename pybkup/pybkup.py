#!/usr/bin/python

import 	os, shutil, sys, tarfile
from subprocess import call, check_call
from pprint import pprint

class EmptyFileListError(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class Bkup:
	def backup(self, backupdir, destdir, backupname, files):
		# verify destination directory exists
		if not os.path.exists(destdir):		
			os.makedirs(destdir)		
		## go to back up direcroty
		os.chdir(backupdir)

		backupfilename = backupname + '.tgz'

		## wrap it up (create g-zipped tarball)
		tar = tarfile.open(backupfilename, "w:gz")
		for name in files:	
			tar.add(name)
		tar.close()	

		shutil.move(backupfilename, os.path.join(destdir, backupfilename))


# root directories
rootdir = os.path.abspath(os.sep)
homedir = os.path.expanduser('~') 

class Cli:
	defaults = {
		'backupdir': homedir,
		'destdir': os.path.join(homedir, 'tmp'),
		'files': []
	}

	def __get_profiles(self):
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
		return profiles

	def __get_config(self, profiles, profile):
		##  set up profiles


		## validate profile name
		if not profile in profiles.keys():
			print("Error: Invalid profile, '"+profile+"'. Configured profiles are: "+', '.join(profiles.keys()))
			exit(1)
		## set up config
		config = profiles[profile]
		for key in self.defaults.keys():
			if not key in config:
				config[key] = self.defaults[key]
		if len(config['files']) == 0:
			print('* File list is empty for '+profile+' add files to the profile in ~/.bkup/config.py')
			exit(0)	
		return config	

	def run(self, profiles=None, profile=None):		
		### will create backup in ~/tmp and extract results
		debug=False

		if profiles == None:
			profiles = self.__get_profiles()

		if profile == None:
			## arguments
			if len(sys.argv) != 2:
				print("Usage: bkup <profile>. Configured profiles are: "+', '.join(profiles.keys()))
				exit(1)
			## TODO: argparse
			profile = sys.argv[1]

		config = self.__get_config(profiles, profile)


		## if debugging, use ~/tmp as destdir and clear it
		destdir = config['destdir']
		if debug:
			destdir=os.path.join(homedir, 'tmp')
			if os.path.exists(destdir):
				shutil.rmtree(destdir)

		bkup = Bkup()
		bkup.backup(config['backupdir'], destdir, profile, config['files'])

		## if debugging, go to destdir (tmp) and unzip results
		if debug:
			os.chdir(destdir)
			tar = tarfile.open(profile+'.tgz', "r:gz")
			tar.extractall()

def main():
	cli = Cli()
	cli.run()

