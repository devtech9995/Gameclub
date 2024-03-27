import pandas as pd
import math
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By

# start Xvfb
display = Display(visible=0, size=(800, 600))
display.start()
exit(0)

# create Chrome webdriver
driver = webdriver.Chrome()
driver.get("https://gameclub.jp/")

element = driver.find_element(By.CLASS_NAME, "btm-add-content")

# stop Xvfb
driver.quit()
display.stop()



googlesheetid='1uXXG0LjOf6xIr3mqimVH6Kcwkj-tYZ_oLOpgYlQJAnA'
sheetname='Gameclub.jp'
url=f"https://docs.google.com/spreadsheets/d/{googlesheetid}/gviz/tq?tqx=out:csv&sheet={sheetname}"
content=pd.read_csv(url)

for index in range(5):
    # print(content.iloc[index, 11])
    # print(isinstance(content.iloc[index, 11], (int, float)))
    if not math.isnan(content.iloc[index, 10]):
    #     print(index)
        print(content.iloc[index, 10])
        
