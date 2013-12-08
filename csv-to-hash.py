#!/usr/bin/env python

import json
import sys
import csv


def iterfile(fp):
    for el in fp:
        nel = ""
        for char in el:
            if char == "\x00":
                continue
            nel += char
        yield nel

numbers = [
    'Phone 1 - Value',
    'Phone 2 - Value',
]


def cleanup(thing):
    thing = thing.replace(" ", "")
    thing = thing.replace(".", "")
    thing = thing.replace("(", "")
    thing = thing.replace(")", "")
    thing = thing.replace("-", "")
    thing = thing.replace("+", "")
    thing = thing[-10:]
    return thing


people = {}

with open(sys.argv[1], 'rb') as csvfile:
    spamreader = csv.DictReader(iterfile(csvfile))
    for row in spamreader:
        for phone in [row.get(x, None) for x in numbers]:
            if phone is None:
                continue

            phone = cleanup(phone.strip())
            if phone == "":
                continue

            people[phone] = "{first} {last}".format(
                first=row.get("Given Name", "unknown"),
                last=row.get("Family Name", "unknown"),
            )

print json.dumps(people)
