from code.Rating import get_kr, get_nice, get_kis
import multiprocessing
import xlwings as xw
from datetime import datetime


def func_for_multi(name):
    if name == "kr":
        return get_kr()
    elif name == "nice":
        return get_nice()
    elif name == "kis":
        return get_kis()


def update_excel():

    name_list = ['kr', 'nice', 'kis']

    pool = multiprocessing.Pool(processes=3)
    result = pool.map(func_for_multi, name_list)

    kr_result = result[0]
    nice_result = result[1]
    kis_result = result[2]

    pool.close()
    pool.join()

    kr_result = kr_result[['발행사', '종류', '등급', '평가일']]
    nice_result = nice_result[['발행사', '종류', '등급', '평가일']]
    kis_result = kis_result[['발행사', '종류', '등급', '평가일']]

    load_wb = xw.Book.caller()
    load_ws_2 = load_wb.sheets["summary"]
    my_values = load_ws_2.range('A5:P22').value
    load_ws_2.range('W5').value = my_values

    load_ws_1 = load_wb.sheets["rawdata"]
    load_ws_1.range('A3:N100').clear()
    load_ws_1.range("A2").value = kis_result
    load_ws_1.range("F2").value = kr_result
    load_ws_1.range("K2").value = nice_result

    last_updated = datetime.now()
    load_ws_1.range("P1").value = last_updated.strftime("%Y-%m-%d %H:%M")

    return


if __name__ == "__main__":
    xw.Book(r"\\172.31.1.222\Deriva\자동화\Ratings.xlsm").set_mock_caller()
    update_excel()
