# instagram-scraper
Python script to download images from an Instagram profile.
It simply scrolls, collecting images links, and then downloads them all with multithreading
It requieres selenium and geckodriver (for Firefox).
The script doesnt capture images that are not visible from the page (ie when a post has multiple images, it only downloads the first one)
