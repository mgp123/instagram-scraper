import os, sys, time, argparse
from selenium import webdriver
import requests
import concurrent.futures

folder = ""

def getParameters():
	ap = argparse.ArgumentParser()
	ap.add_argument("url", help="Instagram url to scrap from")
	ap.add_argument("folder", help="Created folder name")
	ap.add_argument("-n", help="Number of images to download", default = 5000,  type=int)	
	ap.add_argument("--noThreading", help="Dont use multithreading for image download", default = False, const=True, action='store_const')	


	args = vars(ap.parse_args())
	return args["url"], args["folder"], args["n"], args["noThreading"]


def getImageLinks(url, n):
	print("Starting browser...")

	options = webdriver.FirefoxOptions()
	options.add_argument('--headless')
	driver = webdriver.Firefox(firefox_options = options)

	driver.get(url)
	print("Im on Instagram")

	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


	time.sleep(2)


	## some pages differ in the show more button xpath for some reason
	try:
		showMoreButton = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[3]/div[1]/div/button")
	except Exception as e:
		try:
			showMoreButton = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[2]/div[1]/div/button")
		except Exception as e:
			driver.quit()
			raise e


	showMoreButton.click()
	print("Pressed show more publications button")
	time.sleep(2)

	print("Scrolling...")

	last_height = driver.execute_script("return document.body.scrollHeight")
	image_links = []

	finished_scrolling = False 

	while (not finished_scrolling) and len(image_links) < n:
		images = driver.find_elements_by_class_name("FFVAD")
		images = map(lambda image: image.get_attribute("src"), images)
		images = filter(lambda image: not image in image_links, images )
		image_links = image_links + list(images)

		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)

		current_height = driver.execute_script("return document.body.scrollHeight")
		finished_scrolling = current_height == last_height

		last_height = current_height
	
	image_links = image_links[: min(n, len(image_links))] 	

	print("Got {} image links". format(len(image_links)))
	driver.quit()
	print("Browser closed")

	return image_links

def downloadImageLinked(image_url):
   r = requests.get(image_url, stream=True)
   path = folder + "/" + image_url.split("/")[-1]
   if r.status_code == 200:
       with open(path, 'wb') as f:
           for chunk in r:
               f.write(chunk)


def createFolder(folder):
	try:
		os.mkdir(folder)
	except FileExistsError:
		return


def sequentialImageDownload(image_links):	
	counter = 1
	for link in image_links:
		path = folder + "/" + str(counter)
		downloadImageLinked(link)	
		counter += 1


def multithreadedImageDownload(image_links):
	with concurrent.futures.ThreadPoolExecutor() as executor:
		executor.map(downloadImageLinked, image_links)



url, folder, n, noThreading = getParameters()


image_links = getImageLinks(url,n)
createFolder(folder)


print("Downloading images...")
if noThreading:
	sequentialImageDownload(image_links)
else:
	multithreadedImageDownload(image_links)

print("Done!")