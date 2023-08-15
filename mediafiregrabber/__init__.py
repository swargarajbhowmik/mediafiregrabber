import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

def name(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # File Name
        filename = None
        filename_div = soup.find('div', class_='filename')
        if filename_div:
            filename = filename_div.get_text()
        else:
            filename = None
        return filename
    else:
        print(f"Failed to Fetch Information")
        return [], None

def size(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        ul_element = soup.find('ul', class_='details')
        li_elements = ul_element.find_all('li')
        
        # File Size
        file_size = li_elements[0].find('span').text
        return file_size
    else:
        print(f"Failed to Fetch Information")
        return [], None

def uploaddate(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        ul_element = soup.find('ul', class_='details')
        li_elements = ul_element.find_all('li')
        
        # File Size
        uploaded_date = li_elements[1].find('span').text
        return uploaded_date
    else:
        print(f"Failed to Fetch Information")
        return [], None

def format(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # File Format
        div_element = soup.find('div', class_='filetype')
        file_type = div_element.find('span').text
        return file_type

    else:
        print(f"Failed to Fetch Information")
        return [], None
    
def uploadregion(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        p_element = soup.find('p', string=re.compile(r'This file was uploaded from'))
        text = p_element.get_text()
        match = re.search(r'from\s+(.*?)\s+on', text)
        if match:
            region = match.group(1)
        else:
            region = None
        return region
    else:
        print(f"Failed to Fetch Information")
        return [], None

def downloadlink(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')        
        # Download Link
        download_link = None
        for anchor in soup.find_all('a', href=True):
            if re.match(r'^https?://download', anchor['href']):
                download_link = anchor['href']

        return download_link
    else:
        print(f"Failed to Fetch Information")
        return [], None

def info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # File Name
        filename = None
        filename_div = soup.find('div', class_='filename')
        if filename_div:
            filename = filename_div.get_text()
        else:
            filename = None

        ul_element = soup.find('ul', class_='details')
        li_elements = ul_element.find_all('li')
        
        # File Size
        file_size = li_elements[0].find('span').text
        
        # File Format
        div_element = soup.find('div', class_='filetype')
        file_type = div_element.find('span').text

        # Upload Date
        uploaded_date = li_elements[1].find('span').text

        # Upload Region
        p_element = soup.find('p', string=re.compile(r'This file was uploaded from'))
        text = p_element.get_text()
        match = re.search(r'from\s+(.*?)\s+on', text)
        if match:
            region = match.group(1)

        # Download Link
        download_link = None
        for anchor in soup.find_all('a', href=True):
            if re.match(r'^https?://download', anchor['href']):
                download_link = anchor['href']

        return filename, file_size, file_type, uploaded_date, region, download_link
    else:
        print(f"Failed to Fetch Information")
        return [], None
    
def download(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # File Name
        filename = None
        filename_div = soup.find('div', class_='filename')
        if filename_div:
            filename = filename_div.get_text()
        else:
            filename = None
        
        download_link = None
        for anchor in soup.find_all('a', href=True):
            if re.match(r'^https?://download', anchor['href']):
                download_link = anchor['href']
    
        response = requests.get(download_link, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('content-length', 0))
            with open(filename, 'wb') as file, tqdm(
                desc=f"Downloading {filename}", total=total_size, unit="B", unit_scale=True
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    bar.update(len(chunk))
            print("")
        else:
            print("Failed to download the file")
    else:
        print(f"Failed to Fetch Information")
        return [], None