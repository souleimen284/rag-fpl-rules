from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Create folder for output
os.makedirs("data", exist_ok=True)

# Headless Chrome setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

urls = [
    "https://fantasy.premierleague.com/help",
    "https://fantasy.premierleague.com/help/rules",
    "https://fantasy.premierleague.com/help/terms",
    "https://fantasy.premierleague.com/help/new",
]

all_text = ""

for url in urls:
    driver.get(url)
    time.sleep(3)  # wait for JS to load

    # Expand all collapsibles
    while True:
        # find all headers
        collapsibles = driver.find_elements(By.CSS_SELECTOR, ".accordion-header")
        # filter only collapsed sections
        collapsed = [c for c in collapsibles if "collapsed" in c.get_attribute("class")]
        if not collapsed:
            break  # all expanded
        for c in collapsed:
            try:
                c.click()
                time.sleep(0.2)  # give time to expand
            except:
                pass

    # After expanding, get all text inside content sections
    content_elements = driver.find_elements(By.CSS_SELECTOR, ".accordion-content p, .accordion-content li, .accordion-content h2, .accordion-content h3, .accordion-content h4")
    for el in content_elements:
        text = el.text.strip()
        if text:
            all_text += text + "\n"

# Save to file
with open("data/fpl_help_full_test.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("Full FPL help content saved successfully in data/fpl_help_full.txt")

driver.quit()
