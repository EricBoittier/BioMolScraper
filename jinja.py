from jinja2 import Template
import os

def make_index_template(BioMolScraper):

	lines = open(os.path.join("templates", "index_template.html")).readlines()
	print(lines)

	s = ""
	for x in lines:
		s += x

	t = Template(s)

	two_or_more = []
	for pdb in BioMolScraper.ordered_pdbs_by_available_residues:
		print(BioMolScraper.pdbs[pdb]["molecules"])
		if len(BioMolScraper.pdbs[pdb]["molecules"]) >= 2:
			two_or_more.append(pdb)


	return t.render(obj=BioMolScraper, pdbs=BioMolScraper.pdbs, two_or_more=two_or_more)

def make_pdb_template(pdb):

	lines = open(os.path.join("templates", "pdb_template.html")).readlines()
	print(lines)

	s = ""
	for x in lines:
		s += x

	t = Template(s)

	return t.render(pdb=pdb)

