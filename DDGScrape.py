""" This Module uses selenium to get images and image url's from Duck Duck Go's image search. Can save any url of any image or file type. Only works with brave and chrome browser currently"""

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
    file_tags = driver.find_elements_by_class_name('tile--file__img') 

    for tag in file_tags:
        src = tag.get_attribute('data-src')
        src = unquote(src)
        src = src.split('=', maxsplit=1)
        src = src[1]
        yield src
    
    driver.close()
    
def save_file(path, urls, file_name="untitled", original_name=False):
    """ Saves file from url to path under the original or chosen file name. If chosen, the file_name+index identifies the image
        for path, include the final backslash or the path wont work"""
    

    # For individual img URL's
    if type(urls) == type(str()):
        file_data = requests_get(urls).content
        if original_name==True:
            filetype = urls[-4:]
            file_name= findall(f"[0-9a-z.\-_%,&#]+{filetype}", urls)[0][:-4]
        with open(f'{path}{file_name}{filetype}', 'wb') as handler:
            handler.write(file_data)
            handler.close()
    
    # For lists of img URL's
    elif type(urls) in (type(list()), type(tuple())):
        for i, url in enumerate(urls):
            file_data = requests_get(url).content
            if original_name==True:
                filetype = url[-4:]
                file_name= findall(f"[0-9a-z.\-_%,&#]+{filetype}", url)[0][:-4]
                i=""
            with open(f'{path}{file_name}{i}{filetype}', 'wb') as handler:
                handler.write(file_data)
                handler.close()
    
    # Reject it if its not a tuple, list or string.
    else:
        raise TypeError("Error: Input URL format needs to be a string or a list of strings")

def search_and_save(path, query, file_name="image", brave=False, original_name=False):
    """All in one, Searches and then saves all images at chosen path with file_name as the base name, set brave to true if you use brave browser"""
    imgs = list(search(query, brave=brave))
    save_file(path, imgs, file_name=file_name, original_name=original_name)
    
if __name__ == '__main__':
    imgs_urls = list(search('face'))
    print(imgs_urls)