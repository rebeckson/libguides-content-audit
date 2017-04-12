#!/usr/bin/env python

"""Gets current guide data for a given institution's LibGuides site. Saves JSON response, and outputs a corresponding human-readable CSV."""

__author__ = "Rebecca Dickson"
__license__ = "MIT"
__version__ = "1.0"
__email__ = "rebeccadickson@gmail.com"


import requests
import json
import datetime
import unicodecsv as csv


# Base Libguides API url (guides)
lg_url = 'http://lgapi.libapps.com/1.1/guides'

# Querystring parameters. Add your institution's site id and key here.
params = {
	'site_id' : '[YOUR_SITE_ID]',
	'key': '[YOUR_KEY]',
	'sort_by': 'name',
	'expand': 'pages,owner,group,subjects'
}

# Make request
print('Requesting data from LibGuides API...')
r = requests.get(lg_url, params=params)
resp = r.json()
print('Received response from ' + r.url)

# Write json data to file
now = datetime.datetime.now()
now_str = ("%s-%s-%s" % (now.day, now.month, now.year))
filename = "lg_data_" + now_str + ".json"
with open(filename, 'w') as outfile:
	json.dump(resp, outfile, sort_keys = True, indent = 4)
	print('JSON response saved to ' + filename)

# Keys found in the JSON data
keys = ['id', 'name', 'url', 'friendly_url', 'description', 'owner_id', 'created', 'published', 'updated', 'redirect_url', 'status_label', 'type_label', 'count_hit']
# Fields we'll construct
new_keys = ['pages', 'subjects']
# ALL OF THE FIELDS!!! (For CSV column names)
all_fields = keys + new_keys


# Get JSON data and decode.
data = []
with open('lg_data_11-4-2017', 'r') as infile:
	d = infile.read()
	data = json.loads(d)


# Put all the things in a list.
flat_data = []
for guide in data:
	guide_data =[]
	for k in keys:
		guide_data.append(guide.get(k))
	guide_data.append(len(guide.get('pages')))
	subs = guide.get('subjects')
	names = []
	if subs is not None:
		for s in subs:
			names.append(s.get('name'))
	else:
		names.append('none')
	guide_data.append(names)
	flat_data.append(guide_data)

# Write to CSV.
now = datetime.datetime.now()
now_str = ('%s-%s-%s' % (now.day, now.month, now.year))
csv_filename = 'lg_data_' + now_str + '.csv'
with open(csv_filename, 'wb') as outfile:
	writer = csv.writer(outfile, encoding='utf-8')
	writer.writerow(all_fields)
	for line in flat_data:
		writer.writerow(line)
	print("Data parsed and saved to " + csv_filename)

