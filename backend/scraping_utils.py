from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import re

def extract_tagline(title: str) -> str:
    driver = webdriver.Chrome()
    driver.get("https://www.imdb.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"{title}")
    search_box.send_keys(Keys.RETURN)

    home_url = driver.find_element(By.CLASS_NAME, "ipc-metadata-list-summary-item__t").get_attribute("href")
    home_url = home_url.split("?")[0]
    driver.get(f"{home_url}taglines/")
    time.sleep(2)
    try:
        tagline = driver.find_element(By.CLASS_NAME, "ipc-html-content-inner-div").text
        return tagline
    except:
        return ""
    
