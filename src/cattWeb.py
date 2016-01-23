from jinja2 import Environment, FileSystemLoader
import os
import time
import shutil
import glob
import subprocess
import logging

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = '../out'
OUT_FILE = 'index.html'
TEMPLATE_FILE = 'catt_template.html'
T_FMT = '%a, %d %b %Y %H:%M:%S'
PHOTO_FILE = 'img/lastphoto.jpg'
WEB_HOST = 'elva@xaphan'
WEB_HOST_PATH = '/var/www/catt'

class cattWeb(Environment):

	def __init__(self):
		Environment.__init__(self,loader=FileSystemLoader(THIS_DIR),trim_blocks=True)
		self.CWtemplate = self.get_template(TEMPLATE_FILE)
		
	def update(self,cattI):
		htmldict = {}
		htmldict['html_time'] = time.strftime(T_FMT)
		htmldict['title'] = 'cattWeb'

		htmldict['cam'] = {'latest':cattI.cam.lastphoto, 'latesttime':cattI.cam.lastphototime}

		htmldict['oldstats'] = cattI.oldstat
		htmldict['stats'] = cattI.todaystat
		with open(os.path.join(OUT_PATH,OUT_FILE),'w') as f:
			f.write(self.CWtemplate.render(htmldict))

		#Copy the files
		if cattI.cam.lastphoto:
			shutil.copy(cattI.cam.lastphoto,os.path.join(OUT_PATH,PHOTO_FILE))
		else:
			try:			
				os.remove(os.path.join(OUT_PATH,PHOTO_FILE))
			except OSError:
				pass
		scp_return = subprocess.call(['scp','-r']+glob.glob(os.path.join(OUT_PATH,'*'))+[WEB_HOST+':'+WEB_HOST_PATH],stderr=subprocess.PIPE,stdout=subprocess.PIPE)
		if scp_return:
			logging.error('Failed to copy web page to server')



