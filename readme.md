# bkup

Trying to simplify backups. 

Requires config file at ~/.bkup/config.py, for example:

	import os

	homedir = os.path.expanduser('~') 

	profiles = {
		<name>: {								# name of profile
			'backupdir': <path>,				# directory to pull backups from
			'destdir': <path>,					# where to put tarball
			'files': <list>,					# files/directories to include
		},
		...
	}

You can then backup (as a gzipped tarball) configured files/directories from <name>'s <backupdir> to <name>'s <destdir> via
	
	cd /path/to/bkup
	python . <name>

