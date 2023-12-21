import asyncio
from requests_html import AsyncHTMLSession
from urllib.parse import urljoin
import threading
import logging
import requests
import configparser
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, filename='logs.txt', format='%(levelname)s  %(asctime)s  %(message)s')

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)


async def get_dynamic_data(url):
    total_urls = [url]
    domain_urls = []
    pdf_urls = []
    yt_links = []
    url_count = 0

    for x in range(0, 1000):
        for url in total_urls:
        
            session = AsyncHTMLSession()
            try:
                logging.info(f'The url : {url} started....')
                headers = {
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                  }
                  
                response = await session.get(url)

                if response.status_code == 200:
                    await response.html.arender(timeout=30)

                    # Extracting title, description, category, and subcategory
                    title = response.html.find('title', first=True).text
                    description = response.html.find('meta[name="description"]', first=True).attrs.get('content', '')
                    category = ''
                    subcategory = ''

                    logging.info(f'Title       : {title}')
                    logging.info(f'Description : {description}')
                    logging.info(f'Category    : {category}')
                    logging.info(f'Subcategory : {subcategory}')

                    links = response.html.find('a')

                    for link in links:
                        href = link.attrs.get('href', '')
                        if href.startswith('/'):
                            absolute_url = urljoin("https://www.hdfcfund.com/", href[1:])
                            domain_urls.append(absolute_url)
                        elif href.startswith('https://www.hdfcfund.com/'):
                            domain_urls.append(href)
                        elif href.endswith('.pdf'):
                            pdf_urls.append(href)

                    # ... (rest of your existing code)

                    pdf_urls = list(set(pdf_urls))
                    yt_links = list(set(yt_links))

                    domain_urls = list(set(domain_urls))
                    total_urls.extend(domain_urls)
                    total_urls = list(set(total_urls))
                    total_urls = list(set(total_urls))
                    no_urls = len(total_urls)
                    domain_urls.clear()

                    url_count += 1

                    print(f'The Completed count {url_count} of {no_urls}')
                    print(f'The web crawling process {url} is Completed\n')
                    logging.info(f'The url {url} completed')
                    logging.info(f'')


                    with open('TotalUrls.txt', 'w') as file:
                        for url in total_urls:
                            file.write(url + '\n')

                    with open('PdfUrls.txt', 'w') as pdf_file:
                        for pdf_url in pdf_urls:
                            pdf_file.write(pdf_url + '\n')

                    with open('YouTubeLinks.txt', 'w') as yt_file:
                        for yt_link in yt_links:
                            yt_file.write(yt_link + '\n')

                    session.cookies.clear()
                    await session.delete(url)
                    continue
                else:
                    print(f"An error occurred while processing {url}: {response.status_code}")
                    continue

            except Exception as e:
                print(f"An error occurred while processing {url}: {e}")
                continue

    print('Crawled Completed Successfully!')

def get_index(IndexName,ServiceName,ApiKey):
    result = ""
    error = ""    

    #logFilePath = configparser.get("Logging", "LogFile")

    try:
        url = f"https://{ServiceName}.search.windows.net/indexes/{IndexName}?api-version=2019-05-06"
        headers = {
            "Content-Type": "application/json",
            "api-key": ApiKey
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        result = response.text
    except requests.exceptions.RequestException as ex:
        error = f"Error in GetIndex Data | Error Message: {str(ex)} | DateTime: {datetime.now().strftime('%m-%d-%Y %I %M')}"
        #logging_write_single_log(error, logFilePath)
    
    return error if error else result

def logging_write_single_log(message, file_path):
    with open(file_path, "a") as log_file:
        log_file.write(message + "\n")
    

async def create_index(json_data, process_log_path):
    ServiceName = configparser.get("API", "ServiceName")
    IndexName = configparser.get("API", "IndexName")    
    ApiKey = configparser.get("API", "ApiKey")
    logFilePath = configparser.get("Logging", "LogFile")

    try:
        deserialized = json.loads(json_data)
        deserialized["name"] = IndexName
        json_data = json.dumps(deserialized)

        url = f"https://{ServiceName}.search.windows.net/indexes/{IndexName}?api-version=2019-05-06"
        headers = {
            "Content-Type": "application/json",
            "api-key": ApiKey
        }

        response = requests.put(url, headers=headers, data=json_data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        index_result = response.status_code
    except requests.exceptions.RequestException as ex:
        with ex.response as error_response:
            error_message = f"AzureIndexer/CreateIndex| Error Msg={error_response.text}| DateTime: {datetime.now().strftime('%m-%d-%Y %I %M')}"
            logging_write_single_log(error_message, process_log_path)

    return index_result

def logging_write_single_log(message, file_path):
    with open(file_path, "a") as log_file:
        log_file.write(message + "\n")


async def UploadSingle(data):
    try:
        print('Upload a Single file')
    except Exception as e:
        print('Something went wrong!')





#This is the Main Method

if __name__ == "__main__":

    # config = configparser.ConfigParser()
    # config.read('AppConfig.ini')

    # ServiceName = config.get("API", "ServiceName")
    # IndexName = config.get("API", "IndexName")    
    # ApiKey = config.get("API", "ApiKey")
    # website_url = config.get("Main","Url")
    website_url = 'https://www.youtube.com/'

    # # Get Index
    # result = get_index(IndexName,ServiceName,ApiKey)

    # if result == '':

    #     NewIndex = open('Create_Index.json')
    #     jsonData = json.load(NewIndex)

    #     # Create Index
    #     result = create_index(jsonData,'')

    #     if result == 200:
    #         print('Index Created Successfully')
    # else:
    #     print('Index already created!')

    # Crawl urls
    asyncio.run(get_dynamic_data(website_url))
