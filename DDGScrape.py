""" This Module uses selenium to get images and image url's from Duck Duck Go's image search."""

from urllib.parse import unquote
from time import sleep
from html import escape
from selenium import webdriver
import requests




def search(query):
    
    option = webdriver.ChromeOptions()
    option.binary_location = r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
    driver = webdriver.Chrome(options=option)
    
    query = escape(query)
    
    # For one word queries it will be ok, for complex ones should encode first
    driver.get(f'https://duckduckgo.com/?q={query}&t=brave&iar=images&iax=images&ia=images')
    sleep(3)

    # For now it's working with this class, not sure if it will never change
    img_tags = driver.find_elements_by_class_name('tile--img__img') 

    for tag in img_tags:
        src = tag.get_attribute('data-src')
        src = unquote(src)
        src = src.split('=', maxsplit=1)
        src = src[1]
        yield src
    
    driver.close()
    
def save_image(path, urls, image_name="image"):
    """ Saves image from url to path under the image name. A list of URL's is saved as image_name[i] where i is the index in the list
        path works relative to current path or by absolute path, in both cases exclude the final backslash or the path wont work"""
        
    # For individual img URL's
    if type(urls) == type(str()):
        img_data = requests.get(urls).content
        with open(f'{path}{image_name}.jpg', 'wb') as handler:
            handler.write(img_data)
            handler.close()
    
    # For lists of img URL's
    elif type(urls) in (type(list()), type(tuple())):
        for i, url in enumerate(urls):
            img_data = requests.get(url).content
            with open(f'{path}{image_name}{i}.jpg', 'wb') as handler:
                handler.write(img_data)
                handler.close()
    
    # Reject it if its not a tuple, list or string. I dont want the stress.
    else:
        raise TypeError("Error: Input URL format needs to be a string or a list of strings")

def search_and_save(path, query, image_name="image"):
    """ Searches and then saves all images at chosen path with image_name as base name"""
    imgs = list(search(query))
    save_image(path, imgs, image_name=image_name)
    
if __name__ == '__main__':
    from pprint import pprint
    imgs_urls = list(search('boy face'))
    pprint(imgs_urls)
