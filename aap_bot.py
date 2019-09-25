import selenium
from selenium import webdriver
import time
from scrapy.selector import Selector
import csv

def click_lists(model_temp, year_temp, series_temp):
    print("click1")

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
    
    try:
        driver.switch_to.default_content()
        time.sleep(2)
        close_button = driver.find_element_by_class_name("smcx-modal-close")
        close_button.click()
        print("close exist", driver.find_element_by_class_name("smcx-modal-close").get_attribute("outerHTML"))
        time.sleep(2)
    except:
        print("no close button")
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)   
    time.sleep(2)   
    for i in year_list:
        if year_temp in i.text:
            i.click()
            time.sleep(3)
            break

    # click series list
    series_list = driver.find_elements_by_xpath('//*[@id="' + series_col_id + '"]/tbody/tr')
    for i in series_list:
        if series_temp in i.text:
            i.click()
            time.sleep(2)
            break

def click_engine(engine_temp):
    # click engine list
    engine_list = driver.find_elements_by_xpath('//*[@id="' + engine_col_id + '"]/tbody/tr')
    for i in engine_list:
        if engine_temp in i.text:
            i.click()
            time.sleep(2)

def click_details(details_temp):
    # click details list
    details_list = driver.find_elements_by_xpath('//*[@id="' + details_col_id + '"]/tbody/tr')
    for i in details_list:
        if details_temp in i.text:
            i.click()
            time.sleep(2)
            get_html()
            click_gray_menu()
    # for i in details_list:
    #     i.click()
    #     time.sleep(10)
    #     get_html()
    #     click_gray_menu()


def get_html():
    print("get html")
    click_buttons = driver.find_elements_by_class_name("expandHideMessage")
    for i in click_buttons:
        if "Click for" in i.get_attribute("outerHTML"):
            i.click()
            time.sleep(2)

    html_search = driver.find_element_by_xpath('//*').get_attribute('outerHTML')
    selector = Selector(text=html_search)

    html_Text = selector.xpath("//html").extract()
    filename = modelname + ".html"
    file = open(filename, 'a', encoding="utf-8")
    for a in html_Text:
        for b in a.split(">"):
            file.write(b + ">")
            file.write('\n')
    file.close()
    time.sleep(3)


def click_gray_menu():
    print("click gray menu")
    parts_list = driver.find_elements_by_xpath('//*[@id="partSection"]/div[2]/div/div/ul/li')
    print(parts_list)
    for part_menu in parts_list:
        print(222222, part_menu)
        part_menu.click()
        get_html()
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
    global click_num
    global modelname

    target_url = "http://www.australianautomotiveparts.com.au/catalogue.html"

    model_col_id = "DataTables_Table_4"
    year_col_id = "DataTables_Table_6"
    series_col_id = "DataTables_Table_7"
    engine_col_id = "DataTables_Table_8"
    details_col_id = "DataTables_Table_9"

    make_list = []
    model_list = []
    year_list = []
    series_list = []
    engine_list = []
    details_list = []

    
    
    with open('input.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            make_list.append(row[0])
            model_list.append(row[1])
            year_list.append(row[2])
            series_list.append(row[3])
            engine_list.append(row[4])
            details_list.append(row[5])


    click_num = 0
    
    driver = webdriver.Chrome("drivers/chromedriver.exe")
    driver.get(target_url)
    time.sleep(10)
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to_frame(iframe)
    time.sleep(2)

    for i in range(1, len(make_list)+1):
        make = make_list[i]
        model = model_list[i]
        year = year_list[i]
        series = series_list[i]
        engine = engine_list[i]
        details = details_list[i]
        make_col_id = make
        click_num += 1
        print("Click_Num: ", click_num)
        if click_num == 5:
            print("close driver")
            driver.close()
            driver = webdriver.Chrome("drivers/chromedriver.exe")
            driver.get(target_url)
            time.sleep(10)
            iframe = driver.find_element_by_tag_name('iframe')
            driver.switch_to_frame(iframe)
            time.sleep(2)
        modelname = make_col_id + "-" + model + "-" + year + "-" + series + "-" + str(click_num)   
        click_lists(model, year, series)
        time.sleep(1)
        click_engine(engine)
        time.sleep(1)
        click_details(details)

    # driver.close()


