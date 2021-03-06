from csv import DictWriter, QUOTE_MINIMAL
from urllib.parse import urlencode
from lxml import etree
from os import path

BASE_PATH = "data"
FILENAME = "MIDAS_Export_1062020.xml"
OUTPUT = "lichtspiel.csv"

SCHEMA = {
	'id':		None, 
	'copy_id':	None,
	'title':	'./Titles/Title',
	'country':	'./CountryOfOrigin',
	'year':		'./YearOfProduction',
	'type':		'./FilmType',
	'length':  	'./OriginalLength',
	'crew':		'./CrewCast/Person/Name',
	'text_de': 	'./ContentDescription/Content/[@Language="default"]',
	'text_en': 	'./ContentDescription/Content/[@Language="Englisch"]',
}

MAX_ROWS = 500000

tree = etree.parse(path.join(BASE_PATH, FILENAME))

outfname = path.join(BASE_PATH, OUTPUT)

with open(outfname, 'w+', encoding="utf-8", newline='') as csvout:
	writer = DictWriter(csvout, fieldnames=SCHEMA.keys(),
		delimiter=',', quotechar='"', quoting=QUOTE_MINIMAL)
	writer.writeheader()
		
	for es in tree.findall('ExportFilms/Film')[0:MAX_ROWS]:
		obj = SCHEMA.copy()
		for k in obj:
			if obj[k] is None: continue
			n = es.find(obj[k])
			if n is None: 
				obj[k] = "" 
			else:
				obj[k] = ' '.join(n.text.strip()[0:100].splitlines())
				if len(n.text) > len(obj[k])+10: obj[k] = obj[k] + ' ...'
				if obj[k].isdigit(): obj[k] = int(obj[k])
		
		obj['id'] = int(es.get('ContentID'))
		
		copies = es.find('./Copies/Film')
		obj['copy_id'] = 0
		if copies is not None: obj['copy_id'] = int(copies.get('CopyID'))
		
		writer.writerow(obj)
		
