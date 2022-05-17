import pandas as pd
import requests
from bs4 import BeautifulSoup
from code.Info import Urlinfo, Codeinfo
import urllib3
from datetime import date

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

    kr_url = Urlinfo.kr_url
    kr_code = Codeinfo.kr_code

    # 한국기업평가 발행사 등급 크롤링
    kr_result = pd.DataFrame(columns=['평가사', '발행사', '종류', '등급', 'Outlook', '평가일', '업데이트일'])

    i = 1

    for issuer in kr_code:

        response = requests.get(kr_url + kr_code[issuer], verify=False)

        soup = BeautifulSoup(response.text, 'html.parser')

        soup = soup.select_one("div.detail_grid_row div.table_type4")

        for tag in soup.select("#tabcont1 div >table>tbody>tr"):

            result_list = ["한국기업평가",
                           issuer,
                           tag.select_one("td.border_none").get_text(),
                           tag.select("td")[4].get_text(),
                           tag.select("td")[5].get_text(),
                           tag.select("td.date")[0].get_text().replace(".", "-"),
                           date.today()
                           ]

            kr_result.loc[i] = result_list

            i += 1

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