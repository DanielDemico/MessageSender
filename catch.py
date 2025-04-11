import re
from playwright.sync_api import Page, expect, sync_playwright
import time
import uuid 
import requests
import threading 
from concurrent.futures import ThreadPoolExecutor, as_completed


def catch_leads(target,city,limit):
    def separate_elements(element_a):
        for element in element_a:
            hrefs_list.append(element.get_attribute('href'))
    hrefs_list = []
    users = {}
    def try_catch_element(xpath,page):
        try:
            x = page.locator(xpath).text_content()
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
                
                paths = [path_name,path_end,path_site,path_tel]
                
                users = {
                        id_user: {
                        "name": name,
                        "site":site,
                        "telefone":tel,
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
        # def multiple_catcher(worker,task_id, href_list):
        #     with ThreadPoolExecutor(max_workers=3) as inner_executor:
        #         results = list(inner_executor.map(catch_users, hrefs_list))
                
        #     return results
        # hrefs_list = hrefs_list[:limit]
        # max_workers = 3 
        
        # with ThreadPoolExecutor(max_workers=max_workers) as executor:
        #     futures = []
            
        #     chunk_size = len(hrefs_list) // max_workers +1
        #     href_chunks = [hrefs_list[i:i + chunk_size] for i in range(0, len(hrefs_list), chunk_size)]
            
        #     for i, c in enumerate(href_chunks):
        #         future = executor.submit(
        #             multiple_catcher,
        #             f"Worker => {i+1}",
        #             i,
        #             c
        #         )
        #         futures.append(future)
            
        #     for future in futures:
        #         results = future.result()
        #         print(f"Resultado: {results}")
          






leads = catch_leads("Escritório de contabilidade","Marilia",5)
