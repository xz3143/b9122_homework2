#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import urllib.request


# In[2]:


################PROBLEM 1.1################

#from urllib.request import Request

seed_url = "https://press.un.org/en"

urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
unpress=[]
i=1

maxNumUrl =10; #set the maximum number of urls to visit
# print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl and len(unpress)<11:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
#         print('curr_url')
#         print(curr_url)
#         print("num. of URLs in stack: %d " % len(urls))
#         print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links

            
            childUrl = tag['href'] #extract just the link

            o_childurl = childUrl
            childUrl = urllib.parse.urljoin(seed_url, childUrl)
#             print('childUrl')
#             print(childUrl)
            if seed_url in childUrl and childUrl not in seen and childUrl not in unpress and len(unpress)<11:
                urls.append(childUrl)
                seen.append(childUrl)

                try:
                    req1 = urllib.request.Request(childUrl,headers={'User-Agent': 'Mozilla/5.0'})
                    webpage1 = urllib.request.urlopen(req1).read()
                    soup1 = BeautifulSoup(webpage1)
                    anchor= soup1.find("a",hreflang="en",href="/en/press-release")
#                     print('press release')
                    if anchor is not None:
                        text = soup1.find("div", class_="field field--name-body field--type-text-with-summary field--label-hidden field__item").get_text()
                        if "crisis" in text:                           
                            unpress.append(childUrl)
#                             print('childUrl')
                            print(childUrl)
#                             print('crisis')
                except Exception as ex:
                    continue
    urls=['https://press.un.org/en/content/press-release?page='+str(i)]
    i+=1


# print(unpress)
len(unpress)


# In[5]:


################SAVE HTML SOURCE CODE################

import os
import requests


# Directory to save HTML files
output_directory = os.getcwd()

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)
i=1
# Loop through each URL in the 'press' list
for url in unpress:
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 status codes

        # Extract the filename from the URL (e.g., "page1" from "https://example.com/page1")
        filename = os.path.join('1_'+str(i) + ".txt")

        # Save the HTML content to a text file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"Saved HTML source code of {url} to {filename}")
        i+=1
    except Exception as e:
        print(f"Failed")


# In[ ]:





# In[3]:


################PROBLEM 1.2################

seed_url = 'https://www.europarl.europa.eu/news/en/press-room'
urls = [seed_url+'/page/0']    #queue of urls to crawl
seen = [seed_url+'/page/0']    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
press=[]
i=1

maxNumUrl =10; #set the maximum number of urls to visit
# print("Starting with url="+str(urls))
while len(urls) > 0 and len(press)<11:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
#         print("num. of URLs in stack: %d " % len(urls))
#         print("Trying to access= "+curr_url)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)
#         print('opened')

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage)  #creates object soup
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links

            
            childUrl = tag['href'] #extract just the link

            o_childurl = childUrl
            childUrl = urllib.parse.urljoin(seed_url, childUrl)
#             print('childUrl')
#             print(childUrl)
            if childUrl not in seen and childUrl not in press and len(press)<11:
                urls.append(childUrl)
                seen.append(childUrl)
            
                try:
                    req1 = urllib.request.Request(childUrl,headers={'User-Agent': 'Mozilla/5.0'})
                    webpage1 = urllib.request.urlopen(req1).read()
                    soup1 = BeautifulSoup(webpage1)
                    anchor= soup1.find_all('span', class_="ep_name")

                    if anchor is not None:
                        for element in anchor:
                             if element.get_text() == "Plenary session":
#                                 print('PLEN')
#                                 print(childUrl)
                                texts=''
                                text = soup1.find_all("p", class_="ep-wysiwig_paragraph")
                                for line in text:
                                    texts= texts+line.get_text()

                                if "crisis" in texts:
                                    press.append(childUrl)
#                                     print('childUrl')
                                    print(childUrl)
#                                     print('crisis')
                                    break
                                break
                except Exception as ex:

                    continue

    urls=['https://www.europarl.europa.eu/news/en/press-room/page/'+str(i)]
    i+=1


len(press)


# In[6]:


################SAVE HTML SOURCE CODE################

import os
import requests


# Directory to save HTML files
output_directory = os.getcwd()

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)
i=1
# Loop through each URL in the 'press' list
for url in press:
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 status codes

        # Extract the filename from the URL (e.g., "page1" from "https://example.com/page1")
        filename = os.path.join('2_'+str(i) + ".txt")

        # Save the HTML content to a text file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)

        print(f"Saved HTML source code of {url} to {filename}")
        i+=1
    except Exception as e:
        print(f"Failed")


# In[ ]:




