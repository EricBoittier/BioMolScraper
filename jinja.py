from jinja2 import Template
import os

def make_index_template(BioMolScraper):

	lines = open(os.path.join("templates", "index_template.html")).readlines()
	print(lines)

	s = ""
	for x in lines:
		s += x

	t = Template(s)

	return t.render(obj=BioMolScraper, pdbs=BioMolScraper.pdbs)

def make_pdb_template(pdb):

	lines = open(os.path.join("templates", "pdb_template.html")).readlines()
	print(lines)

	s = ""
	for x in lines:
		s += x

	t = Template(s)

	return t.render(pdb=pdb)

