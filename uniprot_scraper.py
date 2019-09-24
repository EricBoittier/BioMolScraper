import requests
from lxml import html
import os
from jinja import *
import pandas as pd

"https://files.rcsb.org/download/6AX4.pdb"
"https://files.rcsb.org/pub/pdb/validation_reports/ax/6ax4/6ax4_full_validation.pdf"
"https://www.rcsb.org/pdb/explore/remediatedChain.do?structureId=6AX4&params.annotationsStr=Protein%20Modification,DSSP&chainId=A"


class BioMolScraper(object):

    def __init__(self, uniprot_id):
        self.uniprot_id = uniprot_id
        self.pdbs = {}
        self.set_pdbs()
        self.ordered_pdbs_by_available_residues = sorted(self.pdbs.keys(),
                                                         key=lambda kv: self.pdbs[kv]["first_residue"])

        self.set_directory()
        self.download_pdbs()
        self.add_pdb_info()
        print(self.pdbs.keys())

        # df = pd.DataFrame.from_dict(self.pdbs, orient='index')
        # df.to_csv(path_or_buf="./{}.csv".format(self.uniprot_id))

    def add_pdb_info(self):
        for pdb in self.pdbs.keys():

            self.pdbs[pdb]["organism"] = []
            self.pdbs[pdb]["molecules"] = []
            self.pdbs[pdb]["reference"] = None
            self.pdbs[pdb]["doi"] = None
            self.pdbs[pdb]["journal_title"] = ""
            self.pdbs[pdb]["title"] = ""

            tmp = open(os.path.join(self.uniprot_id, "{}.pdb".format(pdb)))
            lines = tmp.readlines()

            for line in lines:
                if line.__contains__(" MOLECULE:"):
                    self.pdbs[pdb]["molecules"].append(line)

                if line.startswith("TITLE"):
                    self.pdbs[pdb]["title"] += line

                if line.startswith("JRNL        TITL"):
                    self.pdbs[pdb]["journal_title"] += line

                if line.__contains__("ORGANISM_SCIENTIFIC"):
                    self.pdbs[pdb]["organism"].append(line)

                if line.__contains__("JRNL        REF "):
                    self.pdbs[pdb]["reference"] = line

                if line.__contains__("JRNL        DOI"):
                    self.pdbs[pdb]["doi"] = line.split()[-1]

    def set_directory(self, dir=None):
        if len(self.pdbs) > 0:
            if self.uniprot_id not in os.listdir():
                try:
                    os.mkdir(self.uniprot_id)
                except Exception as e:
                    print(e)
                    print("Making directory failed")

    def download_pdbs(self):
        if len(self.pdbs) > 0:
            for pdb in self.pdbs.keys():
                if pdb + ".pdb" not in os.listdir(self.uniprot_id):
                    page = requests.get("https://files.rcsb.org/download/{}.pdb".format(pdb))
                    with open(os.path.join(self.uniprot_id, pdb + ".pdb"), 'wb') as f:
                        f.write(page.content)

    def set_pdbs(self):
        print("https://www.uniprot.org/uniprot/{}".format(self.uniprot_id))
        page = requests.get("https://www.uniprot.org/uniprot/{}".format(self.uniprot_id))
        tree = html.fromstring(page.content)

        p = tree.xpath('//tr/td')
        for number, line in enumerate(p):
            line = line.text_content()

            if line.__contains__("X-ray"):
                tmp = {}
                tmp["ID"] = p[number - 1].text_content()
                tmp["resolution"] = p[number + 1].text_content()
                tmp["chains"] = p[number + 2].text_content()
                tmp["residues"] = p[number + 3].text_content()
                tmp["first_residue"] = int(p[number + 3].text_content().split("-")[0])
                tmp["last_residue"] = int(p[number + 3].text_content().split("-")[-1])

                self.pdbs[p[number - 1].text_content()] = tmp


uniprot_ids = ["P53350"]

for x in open("bast_output.txt", "r").readlines():
    if x.__contains__(">"):
        uniprot_ids.append(x.split(">")[1].split("|")[0].strip())

# uniprot_ids.remove("3bzi")


for x in uniprot_ids:
    print(x)
    b = BioMolScraper(x)
    if len(b.pdbs) > 0:
        output = open("{}.html".format(b.uniprot_id), "w")
        output.write(make_index_template(b))
