import traceback
import zipfile


def read_dicts(file_name):
    dicts = []
    with open(file_name, 'r') as fp:
        dicts = [pwd.strip() for pwd in fp.readlines()]
    return dicts


def blast(zip_file, pwd):
    try:
        zip_file.extractall('./temp', pwd=pwd.encode())
        return pwd
    except Exception as e:
        if 'Bad password' in str(e):
            return False
        traceback.print_exc()


if __name__ == '__main__':
    dict_file = './zip_dict_1673.txt'

    zip_file = zipfile.ZipFile('./test_8606.zip')
    for password in read_dicts(dict_file):
        result = blast(zip_file, password)
        if result:
            print(f'[+] Get password:{result}')
            break
    else:
        # for循环没有被中断，则进入
        print('[-] Not Found')
