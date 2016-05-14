import unittest, os, shutil, datetime, time, tarfile
from bkup.bkup import Bkup, Cli

counter = 0

class BkupTest(unittest.TestCase):
	def setUp(self):
		self.helpers = Helpers()
		self.__tmpdir = self.helpers.get_tempdir('bkup')
		os.mkdir(self.__tmpdir)
		self.bkup = Bkup()
		self.__srcdir = os.path.join(self.__tmpdir, 'src')
		os.mkdir(self.__srcdir)
		self.__dstdir = os.path.join(self.__tmpdir, 'dst')

	def tearDown(self):
		shutil.rmtree(self.__tmpdir)
		pass	

	def testBackupFiles(self):
		filename1 = 'foo.txt'
		filename2 = '.bar'
		## add files to directory
		self.helpers.write_file(os.path.join(self.__srcdir, filename1), 'foo bar baz')
		self.helpers.write_file(os.path.join(self.__srcdir, filename2), 'bada bing')
		files = [filename1, filename2]
		## backup
		archivefile = self.__backup(files)
		## extract
		self.__extract()

		# verify files are backed up
		ls = os.listdir(self.__dstdir)
		for name in files:
			self.assertTrue(name in ls)	

	def testBackupDirectory(self):
		dirname = 'foo'
		filename1 = 'bar.txt'
		filename2 = '.baz'		
		srcdirpath = os.path.join(self.__srcdir, dirname)
		os.mkdir(srcdirpath)
		self.helpers.write_file(os.path.join(srcdirpath, filename1), 'foo bar baz')
		self.helpers.write_file(os.path.join(srcdirpath, filename2), 'bada bing')
		files = [dirname]

		archivefile = self.__backup(files)

		self.__extract()
		destdir = os.path.join(self.__dstdir, dirname)
		self.assertTrue(os.path.exists(destdir))
		self.assertTrue(os.path.isdir(destdir))

		ls = os.listdir(destdir)
		for name in [filename1, filename2]:
			self.assertTrue(name in ls)			



	def __backup(self, files, name='test'):
		self.bkup.backup(self.__srcdir, self.__dstdir, name, files)  
		archivefile = os.path.join(self.__dstdir, name+'.tgz')
		## verify archive file is created and is gzip
		self.assertTrue(os.path.exists(archivefile))
		self.assertTrue(tarfile.is_tarfile(archivefile))
		return archivefile	

	def __extract(self, name='test'):	
		os.chdir(self.__dstdir)
		tar = tarfile.open(name+'.tgz', "r:gz")
		tar.extractall()



class Helpers:
	__rootdir = os.path.abspath(os.sep)

	def get_tempdir(self, name):
		global counter
		tmpdir = os.path.join(self.__rootdir, 'tmp', name+'-test-'+self.__get_datetime_string()+'-'+str(counter))
		counter = counter + 1
		return tmpdir

	def __get_datetime_string(self):
		ts = time.time()
		return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%S')

	def write_file(self, path, content):
		with open(path, 'wb') as file1:
			file1.write(content)		

if __name__ == '__main__':
    unittest.main()			