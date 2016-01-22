from jinja2 import Environment, FileSystemLoader
import os
import time

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = '../out/catt.html'
TEMPLATE_FILE = 'catt_template.html'
T_FMT = '%a, %d %b %Y %H:%M:%S'

class cattWeb(Environment):

	def __init__(self):
		Environment.__init__(self,loader=FileSystemLoader(THIS_DIR),trim_blocks=True)
		self.CWtemplate = self.get_template(TEMPLATE_FILE)
		
	def update(self,cattI):
		with open(OUT_FILE,'w') as f:
			htmldict = {}
			htmldict['html_time'] = time.strftime(T_FMT)
			htmldict['title'] = 'cattWeb'
			htmldict['cam'] = {'latest':cattI.cam.lastphoto, 'latesttime':cattI.cam.lastphototime}
			htmldict['oldstats'] = cattI.oldstat
			htmldict['stats'] = cattI.todaystat
			f.write(self.CWtemplate.render(htmldict))