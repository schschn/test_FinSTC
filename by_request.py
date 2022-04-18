import requests
import pandas as pd

url = 'http://localhost:5000/crud'


# примеры post/create запроса
def sample_post():
    # post запрос без параметров
    params = {'vintage': '', 'price': '', 'dealer_name': '', 'car_name': '', 'purchase_date': '',}
    post = requests.post(url, params=params)
    print('\n > post запрос без параметров: \n |', post.text)

    # post запрос с буквенным значением параметра цены
    params = {'vintage': '1', 'price': 'llOOO', 'dealer_name': 'Dmitro Gordon',
              'car_name': 'Toyota Camri', 'purchase_date': '2014-11-06'}
    post = requests.post(url, params=params)
    print('\n > post запрос с буквенным значением параметра цены: \n |', post.text)

    # post запрос с успешным выполнением
    params = {'vintage': '1', 'price': '110000', 'dealer_name': 'Dmitro Gordon',
              'car_name': 'Toyota Camri', 'purchase_date': '2014-11-06'}
    post = requests.post(url, params=params)
    print('\n > post запрос с успешным выполнением: \n |', post.text)


# примеры get/retrieve запроса
def sample_get():
    # get запрос без параметров
    get = requests.get(url)
    print('\n > get запрос без параметров: \n', pd.DataFrame(get.json()))

    # get запрос с параметрами
    params = {'dealers': ['Teddy Pendergrass'], 'cars': ['DMC DeLorean']}
    get = requests.get(url, params=params)
    print('\n > get запрос с параметрами: \n', pd.DataFrame(get.json()))

    # get запрос с одним параметром
    params = {'dealers': ['Teddy Pendergrass']}
    get = requests.get(url, params=params)
    print('\n > get запрос с одним параметром: \n', pd.DataFrame(get.json()))

    # get запрос с неправильным параметром вернёт всю базу
    params = {'shmealers': ['Teddy Shpendergrass']}
    get = requests.get(url, params=params)
    print('\n > get запрос с неправильным параметром вернёт всю базу: \n', pd.DataFrame(get.json()))


# примеры update/put запроса
def sample_update():
    # update запрос с ошибкой без указания id
    params = {'price': '123456'}
    put = requests.put(url, params=params)
    print('\n > update запрос без указания id: \n |', put.text)

    # update запрос с успешным выполнением
    params = {'id': '5', 'price': '1'}
    put = requests.put(url, params=params)
    print('\n > update запрос с успешным выполнением: \n |', put.text)


# примеры delete запроса
def sample_delete():
    # delete запрос с ошибкой
    params = {'id': 'qwerty'}
    delete = requests.delete(url, params=params)
    print('\n > delete запрос с ошибкой: \n |', delete.text)

    # delete запрос с успешным выполнением (при наличии такой строки)
    params = {'id': 5}
    delete = requests.delete(url, params=params)
    print('\n > delete запрос с успешным выполнением: \n |', delete.text)



# sample_get()
# sample_post()
# sample_update()
# sample_delete()