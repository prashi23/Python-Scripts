from lxml import etree, html

import csv
import json
import os
import re
import sys
import urllib

class RedBusScrapper(object):

	def __init__(self):
		try:
			f = open('redbus_locations.txt')
#			print "\nIn Try (--init--) (redbus_locations.txt)"
			self._destinations = eval(f.read())
#			print "self._destinations (__init__) : " , self._destinations
		except:
#			print "\nIn Except (--init--) (redbus_locations.txt)"
			self._destinations = {}
		try:
			f = open('redbus_routes.txt')
#			print "\nIn Try (__init__) (redbus_routes.txt)"		
			self._routes = eval(f.read())
#			print "self._routes (__init__) : " , self._routes
		except:
#			print "\nIn Except (--init--) (redbus_routes.txt)"
			self._routes = {}


	def save(self):
#		print 'Saving'
		output = open('redbus_locations.txt', 'w')
#		print "self._destinations (save) : " , self._destinations
		output.write(str(self._destinations))
		output.close()
#		print "self._routes (save): " , self._routes
		output = open('redbus_routes.txt', 'w')
		output.write(str(self._routes))
		output.close()


	def _get_tree_from_url(self, url):
		if not url:
			return
		if url.startswith('/'):
			url = "http://www.redbus.in" + url
#		print url , " in _get_tree_from_url"
		urlstr = url.replace('/', '_')
		try:
#			print "\nIn Try (_get_tree_from_url)"
			f = open("dump/%s" % urlstr, 'r')
			doc = html.fromstring(f.read())
			tree = etree.ElementTree(doc)
			print 'Found'
		except:
#			print "\nIn Except (_get_tree_from_url)"
			print "Error:", sys.exc_info()[0]
#			print 'Downloading'
			tree = html.parse(url)
#			print "Tree :- " , tree
			if not tree:
				print "\nFalling back"
				tree = html.parse(url)
			output = open("dump/%s" % urlstr, 'w')
			output.write(html.tostring(tree))
			output.close()
		return tree


	def _get_data_from_url(self, url):
		if not url:
			return
#		print url
		urlstr = url.replace('/', '_')
		try:
			f = open("dump/%s" % urlstr, 'r')
			data = f.read()
			print 'Found'
		except:
			print "Error:", sys.exc_info()[0]
			print 'Downloading'
			try:
				data = urllib.urlopen(url).read()
			except:
				data = urllib.urlopen(url).read()
			output = open("dump/%s" % urlstr, 'w')
			output.write(data)
			output.close()
		return data


	def _parse_row(self, row):
		company = row['travelsName']
		bus_type = row['busType']
		dep_time = row['departureTimeString']
		arr_time = row['arrivalTimeString']
		duration = row['duration']
		seats = row['noOfseatsAvailable']
		price = row['faresList']
		return (company, bus_type, dep_time, arr_time, duration, seats, price)


	def _parse_results_page(self, url):
		results = []
		data = self._get_data_from_url(url)
		if data.find('data') == -1:
			return []
		jsond = json.loads(data.split('data:')[1][:-1])
		for row in jsond:
			row_result = self._parse_row(row)
			print row_result
			results.append(row_result)
		return results


	def _parse_directory_page(self, url):
		tree = self._get_tree_from_url(url)
		pairs = tree.findall("//a[@class='blueTextSmall']")
		for pair in pairs:
			link = pair.get('href')
#			print "\nLink (_parse_directory_page) : " , link
			tuples = link.split('/')
			src = tuples[-2]
#			print "Src (_parse_directory_page) : " , src
			dest = tuples[-1]
#			print "Dest (_parse_directory_page) : " , dest
			
#			print "self._destinations.has_key[src]" , self._destinations.has_key(src)
#			print "self._destinations.has_key[dest]" , self._destinations.has_key(dest)

			if (self._destinations.has_key(src)) and (self._destinations.has_key(dest)):
				route = (self._destinations[src], src, self._destinations[dest], dest)
				if route not in self._routes:
					print 'Adding ' + str(route)
					self._routes.append(route)


	def get_routes(self):
#		print "\nIn get_routes"
		for i in xrange(1,2):
#			url = 'http://www.redbus.in/bus-tickets/routes-%d.aspx' % i
			url = 'http://www.redbus.in/BusDirectory/%d' % i
#			print "\nURL(get_routes) : " , url
			self._parse_directory_page(url)
#			print "\nself._parse_directory_page(url) : " , self._parse_directory_page(url)
#		print "self._routes(in get_routes): " , self._routes
		return self._routes



	def save2(self,tokens):
		output = open ("src-dest.txt" , 'w')
		#self._destinations = eval(output.read())
		output.write (str (tokens))
		output.close


	def _parse_city_page(self, url):
		tree = self._get_tree_from_url(url)
		divs = tree.findall("//div[@class='seoCityTd']")
		for div in divs:
			text = div.text_content()
			#print text
			if text.find('bus tickets') == -1:
				continue
			tokens = text.replace(' bus tickets', '').split(' to ')
			print tokens
			self.save2(tokens)
			if not self._destinations.has_key(tokens[0]):
				continue
			src_key = self._destinations[tokens[0]]
			if not self._destinations.has_key(tokens[1]):
				continue
			dest_key = self._destinations[tokens[1]]
			route = (src_key, tokens[0], dest_key, tokens[1])
			if route not in self._routes:
			  	print 'Adding ' + str(route)
			  	self._routes.append(route)


	def _parse_cities_page(self, url):
		tree = self._get_tree_from_url(url)
		pairs = tree.findall("//a[@class='blueTextSmall']")
		for pair in pairs:
			link = pair.get('href')
			self._parse_city_page(link)
#			print "Link (in _parse_cities_page) : " , link


	def get_cities(self):
		list_range = ['directory'] + [str(x) for x in range(1, 2)]
		operator_url = "http://www.redbus.in/buses/cities-%s.aspx"
		for char in list_range:
			url = operator_url % char
#			print "url (in get_cities) : " , url
			self._parse_cities_page(url)


	def ensure_symmetry(self):
		other_routes = []
		for route in self._routes:
			src_key = route[0]
			src = route[1]
			dest_key = route[2]
			dest = route[3]
			reverse_route = (dest_key, dest, src_key, src)
			if reverse_route not in self._routes:
				print str(reverse_route) + " not found"
				other_routes.append(reverse_route)
		self._routes += other_routes


	def write_to_csv(self):
		with open('redbus_buses.csv', 'w') as c:
		  writer = csv.writer(c)
		  writer.writerow(['Route', 'Company', 'Type', 'Departure', 'Arrival', 'Duration', 'Seats', 'Price'])
		  for route in self._routes:
		    url = "http://www.redbus.in/booking/SearchResultsJSON.aspx?" \
			  "fromcityid=%d&fromcityname=%s&tocityid=%d&tocityname=%s" \
			  "&doj=06-dec-2012&bustype=any" % (route[0], route[1], route[2], route[3])
		    route_str = "%s-%s" % (route[1], route[3])
		    buses = self._parse_results_page(url)
		    for bus in buses:
			writer.writerow([route_str] + list(bus))
		c.close()


def main():
	parser = RedBusScrapper()
	parser.get_routes()
	parser.get_cities()
	parser.ensure_symmetry()
	parser.save()
	parser.write_to_csv()
	return 1


if __name__ == "__main__":
	sys.exit(main())
