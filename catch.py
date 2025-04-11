import re
from playwright.sync_api import Page, expect, sync_playwright
import time
import uuid 
import requests
import threading 
from concurrent.futures import ThreadPoolExecutor, as_completed

def add_whats_api(tel:str):
    n = tel.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    return f"https://wa.me/{n}"

def catch_leads(target,city,limit):
    def separate_elements(element_a):
        for element in element_a:
            hrefs_list.append(element.get_attribute('href'))
    hrefs_list = []
    users = {}
    def try_catch_element(xpath,page):
        try:
            x = page.locator(xpath).text_content(timeout=3000)
            return x
        except:
            return "Not Found"
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com/maps")
        print(page.title())
        input = page.locator('//input[@class="fontBodyMedium searchboxinput xiQnY "]')
        input.fill(f'{target},{city}')
        input.press("Enter")
        
        # Wait for the results container to be visible
        results_container = page.locator('//div[@role="feed"]')
        expect(results_container).to_be_visible()
        
        while True:
            page.evaluate('''() => {
                    const container = document.querySelector('div[role="feed"]');
                    container.scrollTop = container.scrollHeight;
                }''')
            try:
                expect(page.locator('span[class="HlvSq"]')).to_have_text("Você chegou ao final da lista.")
                break
            except:
                element_a: list = page.locator('//a[@class="hfpxzc"]').all()
                separate_elements(element_a)
                if len(element_a) >= limit:
                    print(len(element_a))
                    break 
            
        def catch_users(href):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                catch = browser.new_page()
                catch.goto(href)
                id_user = uuid.uuid4()
                
                path_name = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1'
                path_end = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div/div[2]/div[1]'
                path_site = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[4]/a/div/div[2]/div[1]'
                path_tel = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[5]/button/div/div[2]/div[1]'
                
                name = try_catch_element(path_name,catch)
                end = try_catch_element(path_end,catch)
                site = try_catch_element(path_site,catch)
                tel = try_catch_element(path_tel,catch)
                            
                users = {
                        id_user: {
                        "name": name,
                        "site":site,
                        "telefone":tel,
                        "link_wtzp": add_whats_api(tel),
                        "endereco": end}
                        }
                
            return users

        hrefs_list = hrefs_list[:limit]
        
        leads = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(catch_users, href) for href in hrefs_list]
            for future in as_completed(futures):
                leads.append(future.result())         
    return leads

        
leads = catch_leads("Escritório de contabilidade","Marilia",5)
