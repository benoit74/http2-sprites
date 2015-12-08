#print "Loading BrowserMod Proxy Bindings"
#from browsermobproxy import Server
print "Loading Selenium webdriver"
from selenium import webdriver
print "Loading other libraries"
import json
import datetime
import dateutil.parser
import pytz
import sys
import time
#print "Loading BrowserMob Proxy libraries"
#server = Server("/Library/Python/2.7/site-packages/browsermob_proxy-0.7.1-py2.7.egg")

#print "Starting server"
#server.start()

#print "Creating proxy"
#proxy = server.create_proxy()

pages = ['SpriteSet', 'Individual-100Percent', 'Individual-80Percent', 'Individual-50Percent', 'Individual-30Percent', 'Individual-10Percent']
modes = ['http1', 'http2']
browsers = ['Firefox', 'Chrome']


allValues = []
for page in pages:
	for mode in modes:
		for browser in browsers:
			allValues.append("{0},{1},{2}".format(page,mode,browser))

for iteration in range(100):
	iValue = 0
	for pageIdx, page in enumerate(pages):	
		for modeIdx, mode in enumerate(modes):	
			print "#########################"
			print "      {0} - {1} : Iteration {2}".format(page, mode, iteration)
			print "#########################"
			
			for browser in range(2):
				done = False
				while not (done):
					if browser == 0:
						print "Loading Firefox and setting proxy"
						profile  = webdriver.FirefoxProfile()
#						profile.set_proxy(proxy.selenium_proxy())
						driver = webdriver.Firefox(firefox_profile=profile)
					else:
						print "Loading Chrome and setting proxy"
						chrome_options = webdriver.ChromeOptions()
#						chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
						driver = webdriver.Chrome(chrome_options = chrome_options)

#					print "Starting new HAR"
#					proxy.new_har()
					
					url = "https://{0}.sprites.octo.com/sprites/{1}.html".format(mode, page)
					print "Loading {0}".format(url)
					try:
						driver.get(url)
						element = driver.find_element_by_id("imgTiming")
						duration = element.get_attribute('innerHTML')
					except:
						print "Unexpected error:", sys.exc_info()[0]
					print "Computing total time"
					
#					total = 0
#					globalStart = pytz.UTC.localize(datetime.datetime.max)
#					globalEnd = pytz.UTC.localize(datetime.datetime.min)
#					for entry in proxy.har['log']['entries']:
#						start = dateutil.parser.parse(entry['startedDateTime'])
#						durationMs = datetime.timedelta(milliseconds=int(entry['time'])) 
#						end = start + durationMs
#						if (start < globalStart) :
#							globalStart = start
#						if (end > globalEnd) :
#							globalEnd = end
#						total += entry['time']

#					total = (globalEnd - globalStart).total_seconds()
					
					allValues[iValue] += ",{0}".format(duration);
					iValue += 1
#					print "Total : {0} s".format(total)
					print "Total : {0} s".format(duration)
#					print "Saving HAR"
					
					if browser == 0:
						label = "firefox";
					else:
						label = "chrome";	
#					with open('data-{0}-{1}-{2}-{3}.json'.format(page,mode,label,iteration), 'w') as outfile:
#					    json.dump(proxy.har, outfile)

					print "Stopping driver"
					driver.quit()
					done = True
#print "Stopping server"
#server.stop()

	print "Writing Summary file"
	fd = open('summary.csv','w')
	for value in allValues:
		value += "\n"
		fd.write(value)
	fd.close()

