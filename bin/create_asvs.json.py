#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from codecs import open
from unicodedata import name as uni_name
import csv
import json


class FixtureCreator(object):

    """
    FixtureCreator

    Open a csv file
    """

    def __init__(self, csv_file):
        self.DEBUG = True
        self.categories = {}
        self.levels = []
        self.requirements = []
        self.rows = []
        self.csv_file = open(csv_file, encoding='utf-8')
        """
        self.csv = csv.reader(self.csv_file,
                              delimiter=',',
                              quotechar='"')
        """
        self.reader = csv.DictReader(self.csv_file, skipinitialspace=True)
        headers = self.reader.fieldnames

        self.csv_to_rows()
        self.create_categories()
        self.create_requirements()
        self.create_levels()

    def __del__(self):
        """Close the csv file"""
        self.csv_file.close()

    def _replace_char(self, variable, char=None, new_char=None):
        """Replace unicode character with something else"""
        if char is None:
            char = u'\u2713'
        if new_char is None:
            new_char = "Y"
        if uni_name(variable) == uni_name(char):
            return new_char
        return variable

    def csv_to_rows(self):
        """Put the contents of the csv in rows"""
        for row in self.reader:
            """Replace unicode character"""
            if row.get("Level 1"):
                row["Level 1"] = self._replace_char(row.get("Level 1"))
            if row.get("Level 2"):
                row["Level 2"] = self._replace_char(row.get("Level 2"))
            if row.get("Level 3"):
                row["Level 3"] = self._replace_char(row.get("Level 3"))
            self.rows.append(row)

    def create_categories(self):
        for row in self.rows:
            item = dict(en=row["Detailed Verification Requirement"])
            if row["ID"].startswith("V") and "section" not in item:
                index = int(row["ID"][1:])
                self.categories[index] = item

    def _get_category_pk(self, version):
        for k, x in enumerate(self.categories):
            if x.get("version") == "V1":
                return k+1

    def create_requirements(self):
        for row in self.rows:
            if not row["ID"].startswith("V"):
                chapterNr = row["ID"].split(".")[0]
                nr = row["ID"].split(".")[1]
                levels = []
                if row.get("Level 1") == "Y":
                    levels.append(1)
                if row.get("Level 2") == "Y":
                    levels.append(2)
                if row.get("Level 3") == "Y":
                    levels.append(3)
                title_dict = dict(en=row["Detailed Verification Requirement"])
                self.requirements.append(dict(
                                         chapterNr=chapterNr,
                                         nr=nr,
                                         levels=levels,
                                         title=title_dict))

    def create_levels(self):
        self.levels.append(dict(en="Oppertunistic"))
        self.levels.append(dict(en="Standard"))
        self.levels.append(dict(en="Advanced"))

    def create_json_file(self):
        json_file = {}
        json_file["chapterNames"] = {}
        json_file["levelNames"] = {}
        json_file["requirements"] = []

        for key in self.categories:
            """Create chapterNames json"""
            item = self.categories[key]
            json_file["chapterNames"][key] = item
        for lvl, item in enumerate(self.levels):
            """Create levelNames json"""
            json_file["levelNames"][lvl + 1] = item
        for req in self.requirements:
            json_file["requirements"].append(req)
        return json.dumps(json_file, sort_keys=True, indent=4)

if __name__ == "__main__":
    p = Path("src/asvs_v3_xls.csv")
    file_path = Path.resolve(p)
    fc = FixtureCreator(str(file_path))
    o = Path("src/asvs_v3.json")
    out_file = open(str(Path.resolve(o)), "w")
    out_file.write(fc.create_json_file())
