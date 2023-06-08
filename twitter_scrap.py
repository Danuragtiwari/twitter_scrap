import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


# Write to CSV file
def write_to_csv(data, filename):
    fieldnames = data.keys()


    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)
        
        
        
        
def scrape_twitter_profile(url):
    options = Options()
    options.add_argument("--headless")  

    # Set path to your ChromeDriver executable
    chromedriver_path = r'C:\Users\hello\AppData\Local\Programs\Python\Python311\Scripts\chromedriver.exe'

    service = Service(chromedriver_path)

    driver = webdriver.Chrome(service=service, options=options)
    # driver.get(f"https://twitter.com/{username}")

    driver.get(url)

    # Wait for the bio element to be visible
    wait = WebDriverWait(driver, 10)
    try:
        bio_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@data-testid="UserDescription"]')))
        bio = bio_element.text
    except TimeoutException:
        bio = ''

    # Find the following count element using XPath

    try:

        following_element = driver.find_element(By.XPATH, '//div[@class="css-1dbjc4n r-1mf7evn"]//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')
        following_count = following_element.text

    except NoSuchElementException:
        following_count = '0'

    #Find the followers count element using XPath
    try:
        followers_count_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//a[contains(@href, "/followers")]//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]'))
        )
        followers_count = followers_count_element.get_attribute('textContent')
    except TimeoutException:
        followers_count = '0'
        
    except NoSuchElementException:
        followers_count = '0'

    # Find the location element using XPath
    try:
        
        location_element = driver.find_element(By.XPATH, '//span[@data-testid="UserLocation"]//span')
        location = location_element.text

        # Extract the location text
        location = location_element.text
        
    except NoSuchElementException:
        location = ''

    # Find the website element using XPath
    try:
        website_element = driver.find_element(By.XPATH, '//a[@data-testid="UserUrl"]')
        website = website_element.get_attribute("href")
        
    except NoSuchElementException:
        website = ''

    # Close the browser
    driver.quit()

    # Create a dictionary with the scraped data
    data = {
        'Bio': bio,
        'Following Count': following_count,
        'Followers Count': followers_count,
        'Location': location,
        'Website': website
       
    }

    return data

#
file_name='twitter_links.csv'
# username='whatsapp'
with open(file_name, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row[0])
        data = scrape_twitter_profile(row[0])
        # data is inserted into csv file.
        write_to_csv(data, "twitter_profile.csv")
        print(data)












# data = scrape_twitter_profile(username)
