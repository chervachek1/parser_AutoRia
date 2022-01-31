import openpyxl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


def get_info():
    wb = openpyxl.Workbook()
    wb.create_sheet(title='Лист1', index=0)
    sheet1 = wb['Лист1']

    url = 'https://auto.ria.com/uk/search/?indexName=auto&categories.main.id=1&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page=0&size=50'

    ser = Service('C:/Users/kusmi/Desktop/Data Science/allegrolocalnie/chromedriver.exe')
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(service=ser, options=op)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    all_url = soup.find_all('div', class_='content-bar')
    x = 1
    for url1 in all_url:
        href = url1.find('a', class_='m-link-ticket').get('href')
        driver.get(href)
        driver.execute_script("window.scrollTo(0,900)")
        try:
            driver.find_element(By.CSS_SELECTOR, "#phonesBlock > div > span > a").click()
            href_soup = BeautifulSoup(driver.page_source, 'lxml')
            name = href_soup.find('div', class_='seller_info mb-15').find('h4', class_='seller_info_name bold').text
            numbers = href_soup.find('div', class_='list-phone').find_all('a')
            sheet1[f'A{x}'] = name
            sheet1[f'C{x}'] = href
            for number in numbers:

                real_number = number.get('data-value')
                if sheet1[f"B{x}"].value == 'None':
                    sheet1[f'B{x}'] = real_number
                else:
                    sheet1[f'B{x}'] = f'{sheet1[f"B{x}"].value} \n {real_number}'
            num = str(sheet1[f'B{x}'].value).replace('None', ' ')
            sheet1[f'B{x}'] = num
            x+=1
        except:
            pass
    wb.save('autoria.xlsx')

def main():
    get_info()


if __name__ == '__main__':
    main()
