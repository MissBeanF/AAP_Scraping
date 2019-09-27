import selenium
from selenium import webdriver
import time
from scrapy.selector import Selector
import csv
import sys

def check_close_button():
    try:
        driver.switch_to.default_content()
        # time.sleep(2)
        print("close exist", driver.find_element_by_class_name("smcx-modal-close").get_attribute("outerHTML"))
        close_button = driver.find_element_by_class_name("smcx-modal-close")     
        close_button.click()
        # time.sleep(2)
        iframe = driver.find_element_by_tag_name('iframe')
        driver.switch_to.frame(iframe)   
        # time.sleep(2) 
    except:
        print("no close button")
        iframe = driver.find_element_by_tag_name('iframe')
        driver.switch_to.frame(iframe)   
        time.sleep(2) 
 
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

    target_url = "http://www.australianautomotiveparts.com.au/catalogue.html"

    model_col_id = "DataTables_Table_4"
    year_col_id = "DataTables_Table_6"
    series_col_id = "DataTables_Table_7"
    engine_col_id = "DataTables_Table_8"
    details_col_id = "DataTables_Table_9"

    make_list = []
    model_list = []
    year_text_list = []
    start_num = 1
    if len(sys.argv) == 1:          
        print("Please input the filename")
        print("eg: py aap_bot_real.py input.csv")
        exit(1)
    elif ".csv" in sys.argv[1]: 
        input_filename = sys.argv[1] 
    else:
        print("Please input correct filename")
    
    if len(sys.argv) == 2:
        print("please input last year number in the console")
        exit(1)
    elif (sys.argv[2]).isdigit():
        start_num = sys.argv[2]
    else:
        print("input number")

    with open(input_filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            make_list.append(row[0])
            model_list.append(row[1])

    for p in range(1, len(make_list)):
        driver = webdriver.Chrome("drivers/chromedriver.exe")
        driver.get(target_url)
        time.sleep(15)

        # iframe select
        iframe = driver.find_element_by_tag_name('iframe')
        driver.switch_to_frame(iframe)
        time.sleep(5)
        make = make_list[p]
        model = model_list[p]
        make_col_id = make  
        list_filename = "input_" + make_col_id + "_" + model + ".csv" 

        # click make list
        driver.find_element_by_id(make_col_id).click()
        time.sleep(2)

        # click model list
        model_list = driver.find_elements_by_xpath('//*[@id="' + model_col_id + '"]/tbody/tr')
        for i in model_list:
            if model in i.text:
                i.click()
                time.sleep(2)
                break

        # click year list
        year_list = driver.find_elements_by_xpath('//*[@id="' + year_col_id + '"]/tbody/tr')
        year_text_list[:] = []
        for n in year_list:
            year_text_list.append(n.text)
        print("year_list_text: ", year_text_list)
        len_year = len(year_list)

        for m in range(int(start_num), len_year):
            if m >= 2:
                driver.close()
                driver = webdriver.Chrome("drivers/chromedriver.exe")
                driver.get(target_url)
                time.sleep(8)

                # iframe select
                iframe = driver.find_element_by_tag_name('iframe')
                driver.switch_to_frame(iframe)
                time.sleep(3) 

                # click make list
                driver.find_element_by_id(make_col_id).click()
                time.sleep(2)

                # click model list
                model_list = driver.find_elements_by_xpath('//*[@id="' + model_col_id + '"]/tbody/tr')
                for i in model_list:
                    if model in i.text:
                        i.click()
                        time.sleep(2)
                        break
                year_list = driver.find_elements_by_xpath('//*[@id="' + year_col_id + '"]/tbody/tr')
            print("year: ", year_list[m].text)
            print("year_number: ", m)
            if "ALL" in year_list[m].text:
                continue
            try:
                year_list[m].click()
            except:
                check_close_button()
                time.sleep(2)
                year_list[m].click()
            time.sleep(2)

            # click series list
            series_list = driver.find_elements_by_xpath('//*[@id="' + series_col_id + '"]/tbody/tr')
            for i in series_list:
                if "SHOW ALL" in i.text:
                    continue
                try:
                    i.click()
                except:
                    check_close_button()
                    time.sleep(1.5)
                    i.click()
                
                time.sleep(4)
                engine_list = driver.find_elements_by_xpath('//*[@id="' + engine_col_id + '"]/tbody/tr')
                file = open(list_filename, 'a', encoding="utf-8")
                for k in engine_list:
                    if len(engine_list) == 1:
                        time.sleep(2)
                        details_list = driver.find_elements_by_xpath('//*[@id="' + details_col_id + '"]/tbody/tr')
                        for j in details_list:
                            file.write('"' + year_list[m].text + '",' + '"' + i.text + '",' + '"' + k.text + '",' + '"' + j.text + '"\n')
                    elif len(engine_list) > 1:
                        try:
                            k.click()
                        except:
                            check_close_button()
                            time.sleep(2)
                            k.click()
                        time.sleep(2)
                        details_list = driver.find_elements_by_xpath('//*[@id="' + details_col_id + '"]/tbody/tr')
                        for j in details_list:
                            file.write('"' + year_list[m].text + '",' + '"' + i.text + '",' + '"' + k.text + '",' + '"' + j.text + '"\n')
                file.close()
            
        print("Click_Num: ", click_num)
        if click_num == 2:
            click_num = 1
            print("close driver")
            driver.close()
            time.sleep(2)
            driver = webdriver.Chrome("drivers/chromedriver.exe")
            driver.get(target_url)
            time.sleep(10)
            iframe = driver.find_element_by_tag_name('iframe')
            driver.switch_to_frame(iframe)
            time.sleep(2)
            click_lists = 0
        driver.close()


