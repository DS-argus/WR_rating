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

    return a1, a2, a3


if __name__ == "__main__":
    kr, nice, kis = get_ratings()

    print(kr)
    print(nice)
    print(kis)
