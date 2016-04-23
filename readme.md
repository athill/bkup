# bkup

Trying to simplify backups. 

Requires config file at ~/.bkup/config.py, for example:

	import os

	homedir = os.path.expanduser('~') 

	profiles = {
		<name>: {								# name of profile
			'backupdir': <path>,				# directory to pull backups from
			'destdir': <path>,					# where to put tarball
			'includes': <list>,					# files/directories to include
			'excludes': <list>					# files/directories to exclude
		},
		...
	}
