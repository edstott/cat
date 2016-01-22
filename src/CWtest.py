import cattWeb
import datetime
from bunch import bunchify

STATS_DICT = {'fed':0.0, 'pir_trig':0, 'date':datetime.date.today(), 'tweets':0, 'start_weight':0.0, 'end_weight':0.0}

CW = cattWeb.cattWeb()

data = bunchify({'cam':{'lastphoto':None,'lastphototime':None}, 'oldstat':[STATS_DICT,STATS_DICT],'todaystat':STATS_DICT})

CW.update(data)