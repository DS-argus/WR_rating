import json

def get_token(target:str) -> str:
    loc = r"C:\Users\Wooriam\Documents\idpw\idpw.json"

    with open(loc, 'r') as file:
        dat = json.load(file)

    return dat['sql'][target]


if __name__ == "__main__":
    print(get_token('id'))
    print(get_token('pw'))
