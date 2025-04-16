
from concurrent.futures import ThreadPoolExecutor, as_completed
from tavily import TavilyClient
from agents import make_resume_agent

from selenium import webdriver  # Import the webdriver
from selenium.webdriver.chrome.service import Service  # Import Service for Chrome
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys 
from datetime import datetime 


def run_scraper(area:str,limit:int):
    # options.add_argument("--headless")  # Run in headless mode (no GUI)
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get("https://www.google.com/maps/")

    # Area de Texto e envia a área com a cidade    
    input_camp = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,'searchboxinput'))
    )
    input_camp.send_keys(area)
    input_camp.send_keys(Keys.ENTER)
    
    # Area com todos os links, para escrolar para baixo
    leads_camp = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
    )
    
    #Scroll para baixo de acordo com a quantidade
    def catch_quanty(lead_element:any, limit:int):
        elements = []
        while len(elements) < limit:
            elements = WebDriverWait(driver,10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,'hfpxzc'))
            )
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", lead_element)
        elements = [i.get_attribute("href") for i in elements]
        return elements[:limit]
    elements = catch_quanty(leads_camp,10)
    
    def catch_lead_informations(href,driver):
        driver.get(href)
        all_info = WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,'Io6YTe.fontBodyMedium.kR99db.fdkmkc '))
        )
        for info in all_info:
            
    
def make_resume(name:str):
    
    TAVILY_API_KEY = "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"
    tavily = TavilyClient(api_key=TAVILY_API_KEY)
    
    response = tavily.search(name)
    content = ""
    for i in response['results']:
        content += i['content']
        content += "------"
        
    print("CONTEUDO: ",content)
    return content
    
def add_whats_api(tel:str):
    n = tel.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    return f"https://wa.me/{n}"


run_scraper("Médicos, Marilia",40)

