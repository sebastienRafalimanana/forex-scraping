import asyncio
import time
from bs4 import BeautifulSoup
import aiohttp

async def fetch_and_parse(url, headers):
  async with aiohttp.ClientSession() as session:
    async with session.get(url, headers=headers) as response:
      response.raise_for_status()
      html = await response.read()
      return BeautifulSoup(html, 'html.parser')
  
async def scraping_strategies(document:BeautifulSoup):
    import pandas as pd
    calendar = document.find("table",class_="calendar__table")
    
    #Extract columns
    header_elements = document.find('thead').find_all('th')
    headers = []
    for element in header_elements:
        text = element.get_text(strip=True)
        if element.find('a'):
            text = text.replace('Time Options', '')
        headers.append(text)
        
    # Extract data 
    data = []
    for row in document.find('tbody').find_all('tr')[1:]:
        row_data = []
        for cell in row.find_all('td'):
            text = cell.text.strip()
            if cell.find('a'):
                text = text.replace('Subscribe to', '')
            row_data.append(text)
        data.append(row_data)

    # Create the pandas DataFrame with the extracted headers as column names
    df = pd.DataFrame(columns=headers)
    print(df)
    print(calendar)
    
    

async def main():
  url = "https://www.forexfactory.com/calendar"
  headers = {"Accept": "*/*", "User-Agent": "Thunder Client (https://www.thunderclient.com)"}

  try:
    print("Fetch forexfactory...")
    start_time = time.time()
    scraped_document = await fetch_and_parse(url, headers)
    end_time = time.time()
    print(f"Fetched in {end_time - start_time:.2f} seconds")
    await scraping_strategies(scraped_document)  
  except aiohttp.ClientError as e:
    print(f"Error: {e}")
    
loop = asyncio.get_event_loop()
loop.create_task(main())
