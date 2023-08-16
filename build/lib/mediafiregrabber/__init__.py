import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import aiohttp
import asyncio
import os
import urllib.parse

def name(url):
    if "mediafire.com/folder/" in url:
            print(f"Error While Downloading {url}, Folders are not supported yet!")
    else:
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
            print(f"[{response.status_code}] Failed to Fetch Information")
            return [], None

def size(url):
    if "mediafire.com/folder/" in url:
            print(f"Error While Downloading {url}, Folders are not supported yet!")
    else:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            ul_element = soup.find('ul', class_='details')
            li_elements = ul_element.find_all('li')
            
            # File Size
            file_size = li_elements[0].find('span').text
            return file_size
        else:
            print(f"[{response.status_code}] Failed to Fetch Information")
            return [], None

def uploaddate(url):
    if "mediafire.com/folder/" in url:
            print(f"Error While Downloading {url}, Folders are not supported yet!")
    else:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            ul_element = soup.find('ul', class_='details')
            li_elements = ul_element.find_all('li')
            
            # File Size
            uploaded_date = li_elements[1].find('span').text
            return uploaded_date
        else:
            print(f"[{response.status_code}] Failed to Fetch Information")
            return [], None

def format(url):
    if "mediafire.com/folder/" in url:
            print(f"Error While Downloading {url}, Folders are not supported yet!")
    else:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # File Format
            div_element = soup.find('div', class_='filetype')
            file_type = div_element.find('span').text
            return file_type

        else:
            print(f"[{response.status_code}] Failed to Fetch Information")
            return [], None
    
def uploadregion(url):
    if "mediafire.com/folder/" in url:
            print(f"Error While Downloading {url}, Folders are not supported yet!")
    else:
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
            print(f"[{response.status_code}] Failed to Fetch Information")
            return [], None

def downloadlink(url):
    if "mediafire.com/folder/" in url:
            print(f"Error While Downloading {url}, Folders are not supported yet!")
    else:
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
            print(f"[{response.status_code}] Failed to Fetch Information")
            return [], None

def info(url, LoadFilesAndFolders=False):
    if "mediafire.com/folder/" in url:

        pattern = r'/([^/]+)/([^/]+)/([^/]+)$'
        matches = re.search(pattern, url)
        if matches:
            folderid = matches.group(2)
            foldername = matches.group(3)

            response = requests.get(f"https://www.mediafire.com/api/1.4/folder/get_info.php?folder_key={folderid}&response_format=json")

            if response.status_code == 200:
                json_content = response.json()
                downloaddir = json_content['response']['folder_info']['name'].strip()

            if LoadFilesAndFolders == True:

                foldercount = 0
                folder_paths = []
                filecount = 0
                file_paths = []

                async def fetch_folder_content(session, folderkey, name, parent_path=""):
                    nonlocal foldercount, filecount, folder_paths, file_paths  # Declare non-local variables
                    requrl = f"https://www.mediafire.com/api/1.4/folder/get_content.php?r=megafire&content_type=folders&filter=all&order_by=name&order_direction=asc&chunk=1&version=1.5&folder_key={folderkey}&response_format=json"
                    async with session.get(requrl) as response:
                        if response.status == 200:
                            json_content = await response.json()
                            folders = json_content['response']['folder_content']['folders']
                            tasks = []
                            for folder in folders:
                                folder_path = f"{parent_path}/{folder['name']}" if parent_path else folder['name']
                                folder_paths.append(folder_path)
                                foldercount += 1
                                task = asyncio.create_task(fetch_folder_content(session, folder['folderkey'], folder['name'], folder_path))
                                tasks.append(task)
                            await asyncio.gather(*tasks)
                            
                            # Fetch file content
                            requrl_files = f"https://www.mediafire.com/api/1.4/folder/get_content.php?r=megafire&content_type=files&filter=all&order_by=name&order_direction=asc&chunk=1&version=1.5&folder_key={folderkey}&response_format=json"
                            async with session.get(requrl_files) as response_files:
                                if response_files.status == 200:
                                    json_files = await response_files.json()
                                    files = json_files['response']['folder_content']['files']
                                    for file in files:
                                        file_path = f"{parent_path}/{file['filename']}" if parent_path else "./" + file['filename']
                                        file_paths.append(file_path)
                                        filecount += 1
                                else:
                                    print(f"[{response_files.status}] Failed to Fetch File Information")
                        else:
                            print(f"[{response.status}] Failed to Fetch Information")

                async def main():
                    async with aiohttp.ClientSession() as session:
                        await fetch_folder_content(session, folderid, foldername)
            
                asyncio.run(main())

            data = {
                "folderkey": json_content['response']['folder_info']['folderkey'],
                "name": json_content['response']['folder_info']['name'],
                "description": json_content['response']['folder_info']['description'],
                "created": json_content['response']['folder_info']['created'],
                "privacy": json_content['response']['folder_info']['privacy'],
                "file_count": filecount if 'filecount' in locals() else None,
                "files": file_paths if 'file_paths' in locals() else None,
                "folder_count": foldercount if 'foldercount' in locals() else None,
                "folders": folder_paths if 'folder_paths' in locals() else None,
                "revision": json_content['response']['folder_info']['revision'],
                "owner_name": json_content['response']['folder_info']['owner_name'],
                "avatar": json_content['response']['folder_info']['avatar'],
                "created_utc": json_content['response']['folder_info']['created_utc']
            }

            return data
    else:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            filename = None
            filename_div = soup.find('div', class_='filename')
            if filename_div:
                filename = filename_div.get_text()
            else:
                filename = None

            ul_element = soup.find('ul', class_='details')
            li_elements = ul_element.find_all('li')
            
            file_size = li_elements[0].find('span').text
            
            div_element = soup.find('div', class_='filetype')
            file_type = div_element.find('span').text

            uploaded_date = li_elements[1].find('span').text

            p_element = soup.find('p', string=re.compile(r'This file was uploaded from'))
            text = p_element.get_text()
            match = re.search(r'from\s+(.*?)\s+on', text)
            if match:
                region = match.group(1)

            download_link = None
            for anchor in soup.find_all('a', href=True):
                if re.match(r'^https?://download', anchor['href']):
                    download_link = anchor['href']
            file_info = {
                "filename": filename,
                "file_size": file_size,
                "file_type": file_type,
                "uploaded_date": uploaded_date,
                "region": region,
                "download_link": download_link
            }
            return file_info
        else:
            print(f"[{response.status_code}] Failed to Fetch Information")
            return [], None
          
def download(url, save="./"):
    if not os.path.exists(save):
        os.makedirs(save)
    os.chdir(save)
    
    if "mediafire.com/folder/" in url:
        pattern = r'/([^/]+)/([^/]+)/([^/]+)$'
        matches = re.search(pattern, url)
        if matches:
            folderid = matches.group(2)
            foldername = matches.group(3)

            response = requests.get(f"https://www.mediafire.com/api/1.4/folder/get_info.php?folder_key={folderid}&response_format=json")
            if response.status_code == 200:
                json_content = response.json()
                downloaddir = json_content['response']['folder_info']['name'].strip()

            if not os.path.exists(downloaddir):
                os.makedirs(downloaddir)
            os.chdir(downloaddir)

            filesqueue = {}

            async def fetch_folder_content(session, folderkey, name, parent_path=""):
                requrl = f"https://www.mediafire.com/api/1.4/folder/get_content.php?r=megafire&content_type=folders&filter=all&order_by=name&order_direction=asc&chunk=1&version=1.5&folder_key={folderkey}&response_format=json"
                async with session.get(requrl) as response:
                    if response.status == 200:
                        json_content = await response.json()
                        folders = json_content['response']['folder_content']['folders']
                        tasks = []
                        for folder in folders:
                            folder_path = f"{parent_path}/{folder['name']}" if parent_path else folder['name']

                            if not os.path.exists(folder_path):
                                os.makedirs(folder_path)

                            task = asyncio.create_task(fetch_folder_content(session, folder['folderkey'], folder['name'], folder_path))
                            tasks.append(task)
                        await asyncio.gather(*tasks)
                        
                        # Fetch file content
                        requrl_files = f"https://www.mediafire.com/api/1.4/folder/get_content.php?r=megafire&content_type=files&filter=all&order_by=name&order_direction=asc&chunk=1&version=1.5&folder_key={folderkey}&response_format=json"
                        async with session.get(requrl_files) as response_files:
                            if response_files.status == 200:
                                json_files = await response_files.json()
                                files = json_files['response']['folder_content']['files']
                                for file in files:
                                    file_name = f"{parent_path}/" if parent_path else "./"
                                    filesqueue[file_name] = urllib.parse.unquote(file['links']['normal_download'])
                            else:
                                print(f"[{response_files.status}] Failed to Fetch File Information")
                    else:
                        print(f"[{response.status}] Failed to Fetch Information")

            async def main():
                async with aiohttp.ClientSession() as session:
                    await fetch_folder_content(session, folderid, foldername)

        else:
            print("Failed To Fetch Information.")

        asyncio.run(main())

        for path,url in filesqueue.items():
            download(url, save=path)
    else:
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
                print(f"[{response.status_code}] Failed to Process The Direct Download Link {download_link}")
        else:
            print(f"[{response.status_code}] Failed to Download The File")
            return [], None