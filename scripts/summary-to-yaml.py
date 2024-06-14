#!/usr/bin/env python
# Convert from the Summary.md file to yaml, for writing the course config file
# requires pyyaml: pip install pyyaml

import datetime
import re

import yaml

UNIT = re.compile(r"^- \[(?P<name>[^\]]+)\]\((?P<path>[^\)]+)\)")
LESSON = re.compile(r"^\s+- \[(?P<name>[^\]]+)\]\((?P<path>[^\)]+)\)")

units = []
unit = None
with open("src/SUMMARY.md") as file:
    summary = file.readlines()
    for line in summary:
        u = UNIT.match(line)
        if u:
            if unit:
                units.append(unit)
            unit = {}
            unit["name"] = u.group("name")
            unit["activities"] = []
            unit["activities"].append(
                {
                    "name": "Introduction",
                    "path": "src/" + u.group("path"),
                    "type": "lesson",
                    "kind": "GENERAL",
                    "workload": 60,
                    "publish": False,
                }
            )
            continue
        l = LESSON.match(line)
        if l and unit:
            name = l.group("name")
            is_assignment = any(
                s in name.lower()
                for s in [
                    "assessment",
                    "assignment",
                    "homework",
                    "problem set",
                    "project",
                ]
            )
            activity = {
                "name": name,
                "path": "src/" + l.group("path"),
                "type": "lesson",
                "kind": "GENERAL",
                "workload": 60,
                "publish": False,
            }
            if is_assignment:
                activity["type"] = "assignment"
                activity["kind"] = "ASSIGNMENT"
                activity["due"] = datetime.date(2024, 12, 31)
                activity["grade_weight"] = 0

            unit["activities"].append(activity)
    units.append(unit)


# pyyaml needs lots of help to print yaml the normal way
class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


print(
    yaml.dump(
        {
            "name": "COURSE NAME",
            "code": "COURSE CODE",
            "term": "TERM (e.g. July-2024)",
            "about_path": "path to course description",
            "units": units,
        },
        sort_keys=False,
        Dumper=MyDumper,
    )
)
