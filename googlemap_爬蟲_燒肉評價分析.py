from selenium import webdriver       #pip install selenium
from bs4 import BeautifulSoup    # pip install beautifulsoup4
import time
from selenium.webdriver.common.keys import Keys
import pyautogui                      #pip install pyautogui
from selenium.webdriver import ActionChains
from pynput.keyboard import Key, Controller #pip install pynput
import pandas as pd
import requests
from selenium.webdriver.common.by import By
from pathlib import Path
import urllib    #pip install urllib
import os
def make_dir():
    ccco1 = ['南屯區']
    try:
        for skfd in range(len(ccco1)):
            dis_name = '台中'+ccco1[skfd]+'燒肉_data'
            dis_name1 = '台中'+ccco1[skfd]+'燒肉_images'
            os.mkdir(dis_name)
            os.mkdir(dis_name1)
    except:
        pass
#make_dir()  #在本地端創資料夾
ccco = ['南屯區']
for jie in range(len(ccco)):
    District = '台中'+ccco[jie]+'燒肉'
    def find_data():
        driver = webdriver.Chrome("chromedriver.exe")
        translation_a = urllib.parse.quote(District)
        driver.get('https://www.google.com.tw/maps/search/' + translation_a + '/@24.1397463,120.6131116,14z/data=!3m1!4b1?hl=zh-TW')
        for h in range(1, 3):
            element = driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]/div/a')            
            actionChains = ActionChains(driver)
            actionChains.context_click(element).send_keys(Keys.ARROW_DOWN).perform()
            time.sleep(5)
            keyboard = Controller()
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            time.sleep(3)
            for j in range(5):
                time.sleep(1)
                pyautogui.press('pgdn')
            #分析網頁
            soup = BeautifulSoup(driver.page_source)
            href1 = soup.find_all('a', {'class': 'hfpxzc'})
            href_link_list = []
            title_list = []
            for i in href1:
                href_link = i.get('href')
                title = i.get('aria-label')
                href_link_list.append(href_link)
                title_list.append(title)
                print(href_link_list)
                print(title_list)
            find_star = soup.find_all('span', {'class': 'ZkP5Je'})
            star_list = []
            for r in find_star:
                star_list.append(r.text.split('(')[0].replace(',', ''))
            print(star_list)
            find_comm = soup.find_all('span', {'class': 'UY7F9'})
            comm_list = []
            for kk in find_star:
                try:
                    comm_list.append(kk.text.split('(')[1].replace(')', ''))
                except:
                    comm_list.append(kk.text.split('(')[0])
            print(comm_list)
            df = pd.DataFrame()
            df['店名'] = title_list
            df['網址'] = href_link_list
            df['星級'] = star_list
            df['評論'] = comm_list
            df.to_csv(District + '_data/' + str(h) + '商家網址連結.csv', index=False, encoding='utf-8-sig')
    find_data()  #顯示網頁
def marge_data():
    excel_dir = Path('C:\\Users\jason\Desktop\Python程式語言實作\googlemap美食\\'+District+'_data')
    excel_files = excel_dir.glob('*.csv')
    df = pd.DataFrame()
    for xls in excel_files:
        data = pd.read_csv(xls, sep=',' )
        df = df.append(data)
    df.to_csv(District+"_商家網址連結.csv", encoding='utf-8-sig', index=False, sep=',')
#marge_data()


def select_data():
    df = pd.read_csv(District + '_商家網址連結.csv')
    df['評論'] = df['評論'].replace('沒有評論', '0')
    df['星級'] = df['星級'].replace('沒有評論', '0')
    df['評論'] = df['評論'].str.replace(',', '')
    df['星級'] = df[['星級']].astype(float)
    df['評論'] = df[['評論']].astype(int)
    df = df[(df["評論"] > 500) & (df["星級"] > 4.0)]
    df['回復'] = ''
    df['地址'] = ''
    df.to_csv(District + '_篩選4.0評論.csv', encoding='utf-8-sig', index=False)
#select_data()


def get_address():
    df = pd.read_csv(District + '_篩選4.0評論.csv')
    link = list(df['網址'])
    for i in range(len(link)):
        driver = webdriver.Chrome("chromedriver.exe")
        driver.get(link[i])
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]').click()
        time.sleep(2)
        soup2 = BeautifulSoup(driver.page_source)
        address = soup2.find('div', {'class': 'Io6YTe fontBodyMedium'}).text
        time.sleep(3)
        for j in range(2):
            time.sleep(0.5)
            pyautogui.press('pgdn')
        time.sleep(3)
        soup1 = BeautifulSoup(driver.page_source)
        comm = soup1.find_all('div', {'class': 'tBizfc fontBodyMedium'})
        comm_list = []
        for ww in comm:
            comm_list.append(ww.text.replace(' 位評論者', '').replace('"', '').replace('   ', '').replace('  ', ''))
        print(comm_list)
        df.loc[i, '回復'] = str(comm_list)
        df.loc[i, '地址'] = str(address)
        df.to_csv(District + '_抓取留言.csv', encoding='utf-8-sig', index=False)
        time.sleep(2)
#get_address()
def select_address():
    df = pd.read_csv(District + '_抓取留言.csv')
    df = df[df['地址'].str.contains(ccco[jie], na=False)]
    df = df[~df['店名'].str.contains('公園', na=False)]
    df = df[~df['店名'].str.contains('車站', na=False)]
    df = df[~df['店名'].str.contains('后豐鐵馬道', na=False)]
    df = df[~df['店名'].str.contains('大甲鎮瀾宮', na=False)]
    df = df[~df['店名'].str.contains('大甲鐵砧山', na=False)]
    df = df[~df['店名'].str.contains('大肚藍色公路', na=False)]
    df = df[~df['店名'].str.contains('靜宜大學', na=False)]
    df = df[~df['店名'].str.contains('弘光科技大學', na=False)]
    df = df[~df['店名'].str.contains('東勢林場遊樂區', na=False)]
    df = df[~df['店名'].str.contains('東豐自行車綠廊', na=False)]
    df = df[~df['店名'].str.contains('高鐵台中站', na=False)]
    df = df[~df['店名'].str.contains('臺中國際展覽館', na=False)]
    df = df[~df['店名'].str.contains('醫院', na=False)]
    df = df[~df['店名'].str.contains('全聯福利中心', na=False)]
    df = df[~df['店名'].str.contains('麗寶Outlet Mall', na=False)]
    df = df[~df['店名'].str.contains('台中三井OUTLET摩天輪', na=False)]
    df = df[~df['店名'].str.contains('台中港旅客服務中心', na=False)]
    df = df[~df['店名'].str.contains('高美濕地', na=False)]
    df = df[~df['店名'].str.contains('牛罵頭遺址', na=False)]
    df = df[~df['店名'].str.contains('鰲峰山觀景平台', na=False)]
    df = df[~df['店名'].str.contains('臺中市港區藝術中心', na=False)]
    df = df[~df['店名'].str.contains('菩薩寺', na=False)]
    df = df[~df['店名'].str.contains('文化園區', na=False)]
    df = df.drop_duplicates(['店名', '地址'])
    df.to_csv(District + '_篩選地址.csv', encoding='utf-8-sig', index=False)
#select_address()
def get_image():
    df = pd.read_csv(District+'_篩選地址.csv')
    link = list(df['網址'])
    for i in range(len(link)):
            driver = webdriver.Chrome("chromedriver.exe")
            driver.get(link[i])
            time.sleep(3)
            driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]').click()
            time.sleep(3)
            for j in range(2):
                time.sleep(0.5)
                pyautogui.press('pgdn')
            time.sleep(3)
            soup1 = BeautifulSoup(driver.page_source)
            comm = soup1.find_all('div', {'class': 'goAFp-ShBeI-lvvS4b-RWgCYc'})
            comm_list = []
            for ww in comm:
                comm_list.append(ww.text.replace(' 位評論者', '').replace('"', '').replace('   ', '').replace('  ', ''))
            print(comm_list)
            df.loc[i, '回復'] = str(comm_list)
            df.to_csv(District+'_抓取留言.csv', encoding='utf-8-sig', index=False)
            time.sleep(2)
            for j in range(1):
                time.sleep(0.5)
                pyautogui.press('pgup')
            time.sleep(3)
            driver.find_element(By.XPATH, '//button[@aria-label="餐飲"]').click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[1]/div[1]/div/a/div[7]').click()
            time.sleep(2)
            for j in range(5):
                time.sleep(0.5)
                pyautogui.press('pgdn')
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source)
            img = soup.find_all('div', {'class': 'U39Pmb'})
            ti = soup.find('div', {'class': 'piCU0 fontTitleLarge'}).text.replace('/', '').replace('|', '')
            img_list = []
            img_list1 = []
            for j in img:
                tes = j.get('style').strip('background-image').replace(': url("', '').replace('");', '').replace(':url(//:0)', '')
                print(tes)
                img_list.append(j.get('style').strip('background-image').replace(': url("', '').replace('");', '').replace(':url(//:0)', ''))
            for i in img_list:
                if len(i)>0:
                    img_list1.append(i)
            for p in range(len(img_list1)):
                img = requests.get(img_list1[p])
                with open(District+"_images\\" + str(ti) + str(p + 1) + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
                    file.write(img.content)
                file.close()
            print(img_list1)
            driver.close()
get_image()