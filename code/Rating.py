from code.Info import Urlinfo, Codeinfo
from code.SSLpatch import no_ssl_verification

import pandas as pd
import requests
import urllib3

from bs4 import BeautifulSoup
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urllib3.disable_warnings()


def get_kis():
    kis_url = Urlinfo.kis_url
    kis_code = Codeinfo.kis_code

    # 한국신용평가 발행사 등급 크롤링
    kis_result = pd.DataFrame(columns=['평가사', '발행사', '종류', '등급', 'Outlook', '평가일', '업데이트일'])

    i = 1

    for issuer in kis_code:

        response = requests.get(kis_url + kis_code[issuer], verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        for tag in soup.select("div.list>ul>li"):

            result_list = ["한국신용평가",
                           issuer,
                           tag.select_one("dl>dt").get_text().strip(),
                           tag.select_one("dd>strong").get_text(),
                           tag.select("dd")[1].get_text()[17:],
                           tag.select("dd")[2].get_text()[3:].replace(".", "-"),
                           date.today()
                           ]

            kis_result.loc[i] = result_list

            i += 1

    return kis_result


def get_kr():

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    kr_url = Urlinfo.kr_url
    kr_code = Codeinfo.kr_code

    # 한국기업평가 발행사 등급 크롤링
    kr_result = pd.DataFrame(columns=['평가사', '발행사', '종류', '등급', 'Outlook', '평가일', '업데이트일'])

    i = 1

    with no_ssl_verification():
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        for issuer in kr_code:

            url = kr_url + kr_code[issuer]
            driver.get(url)
            driver.maximize_window()

            table = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mySheet9-table > tbody  div > div.GMPageOne > table > tbody")))
            rows = table.find_elements(by=By.CSS_SELECTOR, value="tr")[1:]

            for row in rows:

                type = row.find_elements(by=By.CSS_SELECTOR, value="td")[1].text
                rating = row.find_elements(by=By.CSS_SELECTOR, value="td")[5].text
                outlook = row.find_elements(by=By.CSS_SELECTOR, value="td")[6].text
                eval_date = row.find_elements(by=By.CSS_SELECTOR, value="td")[3].text

                result_list = ["한국기업평가",
                               issuer,
                               type,
                               rating,
                               outlook,
                               eval_date.replace(".", "-"),
                               date.today()
                               ]

                kr_result.loc[i] = result_list

                i += 1

        driver.quit()

    return kr_result


def get_nice():

    nice_url = Urlinfo.nice_url
    nice_code = Codeinfo.nice_code

    # 나이스신용평가 발행사 등급 크롤링
    nice_result = pd.DataFrame(columns=['평가사', '발행사', '종류', '등급', 'Outlook', '평가일', '업데이트일'])

    i = 1

    for issuer in nice_code:

        response = requests.get(nice_url + nice_code[issuer], verify=False)

        soup = BeautifulSoup(response.text, 'html.parser')

        soup = soup.select("#tabOverview > div.tbl_type99 > table")[0]

        for tag in soup.select("tbody>tr"):

            result_list = ["나이스신용평가",
                           issuer,
                           tag.select("td")[0].get_text(),
                           tag.select("td")[6].get_text(),
                           tag.select("td")[7].get_text(),
                           tag.select("td")[8].get_text().replace(".", "-"),
                           date.today()
                           ]

            nice_result.loc[i] = result_list

            i += 1

    return nice_result


if __name__ == "__main__":

    print(get_nice())

    print(get_kr())

    print(get_kis())
