# DuckDuckGo Image Scraper

This python module is just meant to make downloading images from duck duck go much easier.
You can use the search function to generate a list of URL's from the search query.
This query is parsed so treat the search as you would in duckduckgo.

Currently only works if you have Chrome or Brave browser installed in default directories.

It also includes a general function to save images as jpg from any input URL or URL list.
Last it has a search_and_save() function which combines the query & save for convenience.

Note the standard DuckDuckGo image search contains about 100 image URLs, so if you want less 
than that, do not use the combined function. Rather, use the query and save functions separately 
and just modify the query list to your liking before sending it to the save function.
