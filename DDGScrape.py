""" This Module uses selenium to get images and image url's from Duck Duck Go's image search. Only works with brave and chrome browser currently"""

from urllib.parse import unquote
from time import sleep
from html import escape
from selenium import webdriver
from requests import get as requests_get
from re import findall

def search(query, brave=False):
    """ Query Duck Duck Go to get a generator list of URLs for the queries images, if you use Brave browser, 
    set brave=True to get selenium to work, otherwise only works with Chrome"""
    
    # Use default chrome options if not using brave
    option = webdriver.ChromeOptions()
    if brave: 
        option.binary_location = r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
    driver = webdriver.Chrome(options=option)
    
    query = escape(query)
    
    # Should work for all queries
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
    
def save_image(path, urls, image_name="image", original_name=False):
    """ Saves image from url to path under the image name. A list of URL's is saved as image_name[i] where i is the index in the list
        path works relative to current path or by absolute path, in both cases exclude the final backslash or the path wont work"""
    

    # For individual img URL's
    if type(urls) == type(str()):
        img_data = requests_get(urls).content
        if original_name==True:
                image_name= findall("[0-9a-z.\-_%,&#]+.jpg", urls)[0][:-4]
        with open(f'{path}{image_name}.jpg', 'wb') as handler:
            handler.write(img_data)
            handler.close()
    
    # For lists of img URL's
    elif type(urls) in (type(list()), type(tuple())):
        for i, url in enumerate(urls):
            img_data = requests_get(url).content
            if original_name==True:
                image_name= findall("[0-9a-z.\-_%,&#]+.jpg", url)[0][:-4]
                i=""
            with open(f'{path}{image_name}{i}.jpg', 'wb') as handler:
                handler.write(img_data)
                handler.close()
    
    # Reject it if its not a tuple, list or string.
    else:
        raise TypeError("Error: Input URL format needs to be a string or a list of strings")

def search_and_save(path, query, image_name="image", brave=False, original_name=False):
    """All in one, Searches and then saves all images at chosen path with image_name as the base name, set brave to true if you use brave browser"""
    imgs = list(search(query, brave=brave))
    save_image(path, imgs, image_name=image_name, original_name=original_name)
    
if __name__ == '__main__':
    imgs_urls = list(search('face'))
    print(imgs_urls)