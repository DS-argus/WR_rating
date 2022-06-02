from dbm.DBmssql import MSSQL
from cfgr.idpw import get_token
from code.Rating import get_kr, get_nice, get_kis

import pymssql
import pandas as pd
import multiprocessing


def func_for_multi(name):
    if name == "kr":
        return get_kr()
    elif name == "nice":
        return get_nice()
    elif name == "kis":
        return get_kis()


def get_ratings():

    name_list = ['kr', 'nice', 'kis']

    pool = multiprocessing.Pool(processes=3)
    result = pool.map(func_for_multi, name_list)

    a1 = result[0]
    a2 = result[1]
    a3 = result[2]

    pool.close()
    pool.join()

    return a1, a2, a3


class DBRating:
    def __init__(self):
        self.server = MSSQL.instance()
        self.server.login(
            id=get_token('id'),
            pw=get_token('pw')
        )

    @staticmethod
    def get_data():
        try:
            print("Get data...")
            df_kr, df_nice, df_kis = get_ratings()

        except:
            print("Error occured when crawling data")
            return

        print("Success")

        df_total = pd.concat([df_kr, df_nice, df_kis], ignore_index=True)

        return df_total

    @staticmethod
    def create_insertible(dat: pd.DataFrame):

        if dat is None:
            return None

        result = list()
        for idx in dat.index:
            seg = dat.loc[idx]
            seg[5] = seg[5].replace("-", "")
            seg[6] = seg[6].strftime("%Y%m%d")
            ins_ = tuple(seg)
            result.append(ins_)

        return result

    def run(self):
        dat = self.get_data()

        print("Inserting Data")

        insert_ = self.create_insertible(dat)

        if insert_ is None:
            return

        duples = 0
        for line in insert_:
            try:
                self.server.insert_row(
                    table_name='rating',
                    schema='drv',
                    database='WSOL',
                    col_=['AGENCY', 'ISSUER', 'TYPE', 'Rating', 'OUTLOOK', 'EVAL_DATE', 'UPDATE_DATE'],
                    rows_=[line]
                )

            except pymssql._pymssql.IntegrityError:
                print(f'{duples + 1}. [{line[0]} & {line[1]} & {line[2]} & {line[6]}] is already in the table')
                duples += 1
                continue

        print("Success")


if __name__ == "__main__":
    drt = DBRating()
    drt.run()
