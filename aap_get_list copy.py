import selenium
from selenium import webdriver
import time
from scrapy.selector import Selector
import csv
import sys

def click_lists(model_temp, year_temp):
    
    # click make list
    driver.find_element_by_id(make_col_id).click()
    time.sleep(2)

    # click model list
    model_list = driver.find_elements_by_xpath('//*[@id="' + model_col_id + '"]/tbody/tr')
    for i in model_list:
        if model_temp in i.text:
            i.click()
            time.sleep(2)
            break

    # click year list
    year_list = driver.find_elements_by_xpath('//*[@id="' + year_col_id + '"]/tbody/tr')

    for i in year_list:
        if year_temp in i.text:
            i.click()
            time.sleep(3)
            break

    # click series list
    file = open(list_filename, 'a', encoding="utf-8")
    series_list = driver.find_elements_by_xpath('//*[@id="' + series_col_id + '"]/tbody/tr')
    for i in series_list:
        if "SHOW ALL" in i.text:
            continue
        i.click()
        time.sleep(3)
        engine_list = driver.find_elements_by_xpath('//*[@id="' + engine_col_id + '"]/tbody/tr')
        for k in engine_list:
            if len(engine_list) == 1:
                details_list = driver.find_elements_by_xpath('//*[@id="' + details_col_id + '"]/tbody/tr')
                for j in details_list:
                    file.write('"' + i.text + '",' + '"' + k.text + '",' + '"' + j.text + '"\n')
            elif len(engine_list) > 1:
                k.click()
                time.sleep(2)
                details_list = driver.find_elements_by_xpath('//*[@id="' + details_col_id + '"]/tbody/tr')
                for j in details_list:
                    file.write('"' + i.text + '",' + '"' + k.text + '",' + '"' + j.text + '"\n')
    file.close()

if __name__ == '__main__':
    global driver
    global target_url
    global make
    global model
    global year
    global series
    global engine
    global details
    global make_col_id
    global model_col_id
    global year_col_id
    global series_col_id
    global engine_col_id
    global details_col_id
    global make_col_list
    global model_col_list
    global year_col_list
    global series_col_list
    global engine_col_list
    global details_col_list
    global click_num
    global list_filename
    global total_count

    target_url = "https://online.aad.com.au/login.aspx"
    catalog_url = "https://online.aad.com.au/catalogue.aspx"

    model_col_id = "DataTables_Table_4"
    year_col_id = "DataTables_Table_6"
    series_col_id = "DataTables_Table_7"
    engine_col_id = "DataTables_Table_8"
    details_col_id = "DataTables_Table_9"

    make_list = []
    model_list = []

    if len(sys.argv) == 1:          
        print("Please input the filename")
        print("eg: py aap_bot_real.py input.csv")
        exit(1)
    elif ".csv" in sys.argv[1]: 
        input_filename = sys.argv[1] 
    else:
        print("Please input correct filename")
    with open(input_filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            make_list.append(row[0])
            model_list.append(row[1])
            


    click_num = 0
    
    driver = webdriver.Chrome("drivers/chromedriver.exe")
    driver.get(target_url)
    time.sleep(10)

    # login
    username = "chris.s@4x4world.com.au"
    password = "!1FS1$dWCIqj"
    username_id = "ctl00_ContentPlaceHolder1_TextBox_Code"
    password_id = "ctl00_ContentPlaceHolder1_TextBox_Password"

    driver.find_element_by_id(username_id).send_keys(username)
    time.sleep(1)
    driver.find_element_by_id(password_id).send_keys(password)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Button_Login"]').click()
    time.sleep(5)

    driver.get(catalog_url)
    time.sleep(5)

    # iframe select
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to_frame(iframe)
    time.sleep(2)

    for i in range(1, len(make_list)):
        make = make_list[i]
        model = model_list[i]
        year = "ALL"
        make_col_id = make
        click_num += 1
        print("Click_Num: ", click_num)
        if click_num == 5:
            print("close driver")
            driver.close()
            time.sleep(2)
            driver = webdriver.Chrome("drivers/chromedriver.exe")
            driver.get(target_url)
            time.sleep(10)
            driver.find_element_by_id(username_id).send_keys(username)
            time.sleep(1)
            driver.find_element_by_id(password_id).send_keys(password)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Button_Login"]').click()
            time.sleep(5)

            driver.get(catalog_url)
            time.sleep(5)
            iframe = driver.find_element_by_tag_name('iframe')
            driver.switch_to_frame(iframe)
            time.sleep(2)
        list_filename = "input_" + make_col_id + "_" + model + ".csv"
        click_lists(model, year)
        time.sleep(5)
    driver.close()


