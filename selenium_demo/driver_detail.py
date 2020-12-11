# coding=utf-8

from selenium import webdriver
import pandas as pd
import numpy as np
import xlrd
from time import sleep
import traceback
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path=r'D:\Soft\Python-3.7.4.0\scripts\chromedriver.exe')
# 隐士等待
# driver.implicitly_wait(5)
options = webdriver.ChromeOptions()
options.add_argument('Cookie=JSESSIONID=7EF6089BAB5DD1399A9B4DC879AE8A4B; yhdh=79667012-1')
options.add_argument('Upgrade-Insecure-Requests=1')
options.add_argument('Host=122.224.89.228:9003')
options.add_argument('Referer=http://122.224.89.228:9003/zdc/jsrcx.spr?act=toList')

driver.get('http://122.224.89.228:9003/zdc/loginNomal.spr')
# 在后面添加cookie
driver.add_cookie(
    {'name': 'JSESSIONID', 'value': '7EF6089BAB5DD1399A9B4DC879AE8A4B', 'domain': '122.224.89.228', 'path': '/zdc'})
driver.add_cookie({'name': 'yhdh', 'value': '79667012-1', 'domain': '122.224.89.228', 'path': '/zdc'})

df = pd.DataFrame(
    columns=['证件号码', '档案编号', '驾驶人照片', '证件名称', '姓名', '性别', '出生日期', '准驾车型', '发证机关', '驾驶证状态', '初次领证日期', '下一体检日期', '初次发证机关',
             '驾证期限', '有效期始', '有效期至', '累计积分', '超分日期', '下一清分日期', '证芯编号', '从业日期', '记录状态', '审验日期', '管理部门', '驾校名称'])


def to_list():
    url = 'http://122.224.89.228:9003/zdc/jsrcx.spr?act=toList'
    driver.get(url)

    for page_num in range(1, 21):
        for i in range(1, 11):
            try:
                # 显示标签等待
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/table')))
                table = driver.find_element_by_xpath('/html/body/div[2]/div/table')
                # 一行
                tr = table.find_elements_by_tag_name('tr')[i]

                tds = tr.find_elements_by_tag_name('td')
                view = tds[-1]
                view.find_element_by_tag_name('a').click()
                detail(page_num * 10 + i)
                # 点击返回
                driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr[7]/td/input').click()
            except Exception as e:
                print(e)
        # 点击下一页
        try:
            page_control_div = driver.find_element_by_xpath('/html/body/div[3]/form/div')
            page_controls = page_control_div.find_elements_by_tag_name('a')
            for control in page_controls:
                text = control.text
                if '下一页' in text:
                    control.click()
                    break
        except Exception as e:
            print(e)


def detail(row_num):
    # driver.get('http://122.224.89.228:9003/zdc/jsrcx.spr?act=toDetaile&xh=15916575&isdel=')
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'drvInfForm')))
    form = driver.find_element_by_name('drvInfForm')
    trs = form.find_elements_by_tag_name('tr')
    row = []
    for tr in trs[:10]:
        tds = tr.find_elements_by_tag_name('td')
        for td in tds:
            align = td.get_property('align')
            text = td.text
            if align != 'center':
                row.append(text.strip())

    print(row)
    df.loc[row_num] = row


if __name__ == '__main__':
    to_list()
    print(df)
    df.to_excel(r'C:\Users\heyon\Desktop\driver_detail.xlsx',index=None)
