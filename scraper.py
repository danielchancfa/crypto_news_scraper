from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from config import BOT_TOKEN, CHAT_ID


def send_telegram_message(chat_id, text, bot_token):
    """Sends a message to a Telegram chat via bot."""
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={text}'

    response = requests.get(send_text)
    return response.json()

# Get telegram bot_token and chat_id from config.py
bot_token = BOT_TOKEN
chat_id = CHAT_ID

# Set up Chrome options
chrome_options = Options()

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()

# The cointelegraph target URL
cointelegraph_url = 'https://cointelegraph.com/category/latest-news'

# Navigate to the URL
driver.get(cointelegraph_url)

# # get the page html
# cointelegram_html = driver.page_source

# Find all article elements
articles = driver.find_elements(By.XPATH, '//li[@data-testid="posts-listing__item"]')
# Extract and print titles and URLs of articles
for article in articles:
    try:
        time_change = article.find_element(By.XPATH, 'article//div/time').text
        #send telegram message if the news pop up within 1 hour
        if 'MINUTES' in time_change:

            title = article.find_element(By.XPATH, 'article//a/span').text
            
            link = article.find_element(By.XPATH, 'article/a').get_attribute('href')
            
            author = article.find_element(By.XPATH, 'article//div[@class="post-card-inline__meta"]/p/a/span').text

            source = 'Cointelegram'
            
            message = f'Title: [{title}]({link}) \nAuthor: {author}\nSource: {source}'
            
            send_telegram_message(chat_id, message, bot_token)
            print(message)
    except Exception as e:
        print("Error extracting information from one of the articles:", e)
    
# Close the browser
driver.quit()
