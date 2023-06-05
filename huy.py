import sys
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

with open('proxies.txt', 'r') as file:
    proxies = file.read().splitlines()

def check_proxy(proxy):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'--proxy-server=socks4://{proxy}')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--disable-dev-shm-usage')

        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get('https://minecraft.org.ua/minecraft-servers/Helix-Vanilla/536')

            button_locator = (By.CSS_SELECTOR, 'button.mc-button:nth-child(2)')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(button_locator))

            button = driver.find_element(*button_locator)
            button.click()

            return proxy

    except Exception as e:
        return proxy


results = []

with tqdm(total=len(proxies)) as pbar:
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        threads = executor.map(check_proxy, proxies)
        
        for result in threads:
            pbar.update(1)
