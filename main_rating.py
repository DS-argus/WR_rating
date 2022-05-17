from code.Rating import get_kr, get_nice, get_kis
import multiprocessing


def func_for_multi(name):
    if name == "kr":
        return get_kr()
    elif name == "nice":
        return get_nice()
    elif name == "kis":
        return get_kis()


def get_ratings():
    """
    pool.map() 에 실행 함수의 결과가 list 형태로 저장됨 -> pool이 close되면 사라지니 다른 변수에 저장해두고 활용
    """

    name_list = ['kr', 'nice', 'kis']

    pool = multiprocessing.Pool(processes=3)
    result = pool.map(func_for_multi, name_list)

    a1 = result[0]
    a2 = result[1]
    a3 = result[2]

    pool.close()
    pool.join()

    print(a1)
    print(a2)
    print(a3)
    """
    MSSQL에 저장
    업데이트 날짜를 추가하여 계속해 데이터가 누적되도록 작성
    약 일주일 주기로 필요한 날 이전에 업데이트 되도록. ex) 제안서 작성하는 전날

    TABLE : drv.rating

    FIELD = [AGENCY VARCHAR(20) NOT NULL PRIMARY KEY, 
            ISSUER VARCHAR(20) NOT NULL PRIMARY KEY,
            TYPE VARCHAR(20) NOT NULL PRIMARY KEY, 
            RATING VARCHAR(20) NOT NULL, 
            OUTLOOK VARCHAR(20), 
            EVAL_DATE VARCHAR(20) NOT NULL
            UPDATE_DATE VARCHAR(20) NOT NULL PRIMARY KEY] 

    """


if __name__ == "__main__":
    get_ratings()
