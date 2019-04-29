import requests


def get_coordinates(city_name):
    try:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            'geocode': city_name,
            'format': 'json'
        }
        # отправляем запрос
        response = requests.get(url, params)
        # получаем JSON ответа
        json = response.json()
        # получаем координаты города (там написаны долгота(longitude),
        # широта(latitude) через пробел).
        # Посмотреть подробное описание JSON-ответа можно
        # в документации по адресу
        # https://tech.yandex.ru/maps/geocoder/
        coordinates_str = json['response']['GeoObjectCollection'][
            'featureMember'][0]['GeoObject']['Point']['pos']
        # Превращаем string в список, так как точка -
        # это пара двух чисел - координат
        a = list(map(float, coordinates_str.split()))
        # Вернем ответ
        return a
    except Exception as e:
        return e


def createFunction(e, f):
    a, b = int(e), int(f)
    c = - a - b
    if c < 0:
        s = str(c) + "x"
    elif c == 0:
        s = ""
    else:
        s = "+" + str(c) + "x"
    res = s
    c = a * b
    if c < 0:
        s = str(c)
    elif c == 0:
        s = ""
    else:
        s = "+" + str(c)
    return "x^2" + res + s

