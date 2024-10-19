import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize EdgeDriver with EdgeDriverManager
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

# Visit the webpage to scrape
driver.get("https://www.flipkart.com/laptops/a~buyback-guarantee-on-laptops-/pr?sid=6bo%2Cb5g&amp;amp;amp;amp;amp;amp;amp;amp;amp;uniq=")

# Wait for the product grid to load
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'yKfJKb.row')))
    content = driver.page_source  # Get the page content after it is fully loaded
finally:
    driver.quit()  # Close the browser

# Parse the content with BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# Lists to store scraped data
products = []
prices = []
ratings = []

# Extract the product information
for a in soup.findAll('div', attrs={'class':'yKfJKb row'}):  # Outer div class for product container
    name = a.find('div', attrs={'class':'KzDlHZ'})  # Product Name
    price = a.find('div', attrs={'class':'Nx9bqj _4b5DiR'})  # Price
    rating = a.find('div', attrs={'class':'XQDdHH'})  # Rating

    # Debug: Print extracted information
    print(f"Name: {name.text.strip() if name else 'N/A'}, Price: {price.text.strip() if price else 'N/A'}, Rating: {rating.text.strip() if rating else 'N/A'}")
    
    if name and price:
        products.append(name.text.strip())
        prices.append(price.text.strip())
        ratings.append(rating.text.strip() if rating else 'No rating')

# Create a DataFrame and save the data to a CSV file
df = pd.DataFrame({'Product Name': products, 'Price': prices, 'Rating': ratings})
df.to_csv('products.csv', index=False, encoding='utf-8')

print("Web scraping completed and data saved to products.csv.")
