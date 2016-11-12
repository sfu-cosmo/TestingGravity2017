#!/usr/bin/env python
# -*- coding: utf8 -*-

import re, csv
import itertools

participants = [
	# invited speakers
	["Adelberger", "Eric", "University of Washington"],
	["Allen", "Bruce", "MPI & LIGO"],
	["Brax", "Philippe", "Université Paris Saclay"],
	["Burgess", "Cliff", "McMaster/Perimeter"],
	["Burrage", "Clare", "University of Nottingham"],
	["Ferreira", "Pedro", "University of Oxford"],
	["Hui", "Lam", "Columbia University"],
	["Jain", "Bhuvnesh", "University of Pennsylvania"],
	["Joyce", "Austin", "University of Chicago"],
	#["Khoury", "Justin", "University of Pennsylvania"],
	["Maartens", "Roy", "University of Cape Town"],
	["Muller" ,"Holger", "University of California, Berkeley"],
	["Percival", "Will", "ICG, Portsmouth"],
	["Pospelov", "Maxim", "Victoria/Perimeter"],
	["Pretorius", "Frans", "Princeton University"],
	["Rham", "Claudia de", "Case Western Reserve University"],
	["Sasaki", "Misao", "Yukawa Institute for Theoretical Physics"],
	["Trodden", "Mark", "University of Pennsylvania"],
	["White", "Martin", "University of California, Berkeley"],
  	# LOC
  	["Frolov", "Andrei", "Simon Fraser University"],
  	["Pogosian", "Levon", "Simon Fraser University"],
]

table = []

def mangle(affiliation):
	affiliation = re.sub(r"Royal Astronomical Society", 'RASC', affiliation)
	affiliation = re.sub(r"University of British Columbia", 'UBC', affiliation)
	affiliation = re.sub(r"Simon Fraser (U|u)niversity", 'SFU', affiliation)
	affiliation = re.sub(r"Memorial University of Newfoundland", 'Memorial', affiliation)
	affiliation = re.sub(r"California Institut?e of Technology", 'Caltech', affiliation)
	affiliation = re.sub(r"California State University", 'CSU', affiliation)
	affiliation = re.sub(r"University of California(,|\s+at)?", 'UC', affiliation)
	affiliation = re.sub(r"University of Pennsylvania", 'UPenn', affiliation)
	affiliation = re.sub(r"Case Western Reserve", 'Case Western', affiliation)
	affiliation = re.sub(r"Perimeter.*", 'Perimeter', affiliation)
	affiliation = re.sub(r"Yukawa Institute for Theoretical Physics", 'YITP', affiliation)
	affiliation = re.sub(r"Lebedev.*", 'Lebedev', affiliation)
	affiliation = re.sub(r".*\(IKI\).*", 'IKI', affiliation)
	affiliation = re.sub(r"Universidad Austral de Chile", 'UACh', affiliation)
	affiliation = re.sub(r"American University of Afghanistan", 'AUAF', affiliation)
	affiliation = re.sub(r"\s*Universit(y|é)(\s+(of|at|de))?(\s+(the))?\s*", '', affiliation)
	affiliation = re.sub(r",?\s*Dep(ar)?t(ment)?\s+of\s+.*", '', affiliation)
	return affiliation

def grouper(n, iterable, padvalue=None):
	"grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
	return itertools.izip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def chunker(n, array, padvalue=None):
	"chunker(3, 'abcdefg', 'x') --> ('a','d','g'), ('b','e','x'), ('c','f','x')"
	l = len(array); m = (l+n-1)/n
	chunks = [array[i:min(i+m,l)] for i in range(0,l,m)]
	return itertools.izip_longest(*chunks, fillvalue=padvalue)

with open('participants.csv', 'rU') as csvfile:
	for row in csv.reader(csvfile, dialect=csv.excel):
		if row[28].lower() != 'yes': continue
		participants.append(row[4:7])

participants.sort(key = lambda p: p[0])

for p in itertools.groupby(participants):
	last,first,affiliation = p[0]
	
	# fix stuff for people who cannot spell
	if last == "Lebed": affiliation = "University of Arizona"
	if last == "Steer": affiliation = "APC, Paris"
	if last == "Khoury": affiliation = "University of Pennsylvania"
	
	# abbreviate name if it is too long
	if (len(first+last) > 24):
		first = re.sub(r'([A-Z])[a-z]+', r'\1.', first)

	table.append("%s %s (%s)" % (first, last, mangle(affiliation)))

print """<meta charset="UTF-8">
<font face="PT Sans Caption" size="6">Registered Participants:
</font>
<table>
<tbody style="vertical-align: top;">
<tr>
"""

#for row in chunker(3, table, ""):
#	print "<tr>"
#	for name in row:
#		print "<td style=\"width: 48ex;\">%s" % name

for column in grouper((len(table)+2)/3, table):
	print "<td style=\"width: 30%;\"><ul>"
	for name in column:
		if name != None: print "<li>" + name
	print "</ul></td>"

print """
</tr>
</tbody>
</table>
"""
