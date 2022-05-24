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
