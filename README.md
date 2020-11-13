# instagram-scraper
Python script to download images from an Instagram profile.

It simply scrolls, collecting images links, and then downloads them all with multithreading

Requieres selenium and geckodriver (for Firefox).

The script doesnt capture images that are not visible from the page (ie when a post has multiple images, it only downloads the first one)

````
usage: instaScraper.py [-h] [-n N] [--noThreading] url folder

positional arguments:
  url            Instagram url to scrap from
  folder         Created folder name

optional arguments:
  -h, --help     show this help message and exit
  -n N           Number of images to download
  --noThreading  Dont use multithreading for image download
````
