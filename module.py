from ast import main
from base64 import decode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas
import numpy as np

def get_csv(
        url: str,
        start_date: str = None,
        end_date: str = None,
        save_path: str = None,
        sleep_time: float = 2
    ) -> None:
    options = Options()
    options.add_argument("--disable-notifications")
    
    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome.get(url)
    chrome.maximize_window()
    
    xpath = {
        "basic_info": "/html/body/div[1]/div/div/div/div/div[5]/div[1]/div[1]/div/div[2]/nav/div/div/div[2]",
        "establish_date": "/html/body/div[1]/div/div/div/div/div[5]/div[1]/div[1]/div/div[3]/div/section[1]/div/div[12]/div/div",
        "history_value": "/html/body/div[1]/div/div/div/div/div[5]/div[1]/div[1]/div/div[2]/nav/div/div/div[3]",
        "start_date": "/html/body/div[1]/div/div/div/div/div[5]/div[1]/div[1]/div/div[4]/div/div[2]/div[1]/div/input",
        "download_button": "/html/body/div[1]/div/div/div/div/div[5]/div[1]/div[1]/div/div[4]/div/div[2]/button"
    }
    # in `basic information`, get `establish date`.
    basic_info = chrome.find_element(By.XPATH, xpath["basic_info"])
    basic_info.click()
    time.sleep(sleep_time)
    establish_date = (chrome.find_element(By.XPATH, xpath["establish_date"])).text.replace("-", "/")

    # in `history value`, download csv file.
    history_value = chrome.find_element(By.XPATH, xpath["history_value"])
    history_value.click()
    time.sleep(sleep_time)
    start_date = chrome.find_element(By.XPATH, xpath["start_date"])
    start_date.click()
    start_date.send_keys(Keys.CONTROL + "a")
    start_date.send_keys(Keys.DELETE)
    start_date.send_keys(establish_date)
    download_button = chrome.find_element(By.XPATH, xpath["download_button"])
    download_button.click()
    time.sleep(sleep_time)
    chrome.close()
    chrome.quit()
    
def read_csv(
        file_path: str
    ) -> pandas.DataFrame:
    with open(file_path, 'r', encoding="utf-8") as file:
        title = file.readline().strip('\n').split(',')
        lines = file.readlines()
        date, net_value, change, change_percent = [], [], [], []
        for line in lines:
            L = line.strip('\n').strip('%').split(',')
            
            date.append(L[0])
            
            net_value.append(np.float64(L[1]))
            
            if L[2] == 'null': change.append(np.nan)
            else: change.append(np.float64(L[2]))
            
            if L[3] == 'null': change_percent.append(np.nan)
            else: change_percent.append(np.float64(L[3]))

        return pandas.DataFrame(
                            data = {
                                title[1]: net_value,
                                title[2]: change,
                                title[3]: change_percent
                            },
                            index = date,
                        )
if __name__ == '__main__':
    # test get csv 
    url = "https://tw.stock.yahoo.com/fund/summary/F00000MB1X:FO"
    get_csv(url)
    # test read csv
    data_table = read_csv("C:/Users/User/Downloads/F00000MB1X_FO.txt")
    print(data_table.head(10))