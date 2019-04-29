from flask import Flask, request
import logging
import json
from random import choice
from fuctions import *

places = ("Пирамиды_Гизы", "Пирамиды_Гизы")

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        sessionStorage[user_id] = {
            "counter": 0,
            'game_started': False  # здесь информация о том, что пользователь начал игру. По умолчанию False
        }
        res['response']['text'] = \
            'Здравствуйте! Давайте сышаем в игру! Я загадываю место, а вы'+\
            ' отгадываете его координаты, решая уравнения. Если решите все '+\
            'правильно - я расскажу вам об этом месте!'
        res['response']['buttons'] = [
                        {
                            'title': 'сыграть',
                            'hide': True
                        },
                        {
                            'title': 'Нет',
                            'hide': True
                        }
                    ]
        return
    if not sessionStorage[user_id]['game_started']:
        if 'сыграть' in req['request']['nlu']['tokens']:
            sessionStorage[user_id]['game_started'] = True
            sessionStorage[user_id]['counter'] += 1
            sessionStorage[user_id]['место'] = choice(places)
            play_game(res, req)
        elif 'нет' in req['request']['nlu']['tokens']:
            res['response']['text'] = 'Ну и ладно!'
            res['end_session'] = True
        else:
            res['response']['text'] = 'Не поняла ответа! Так да или нет?'
            res['response']['buttons'] = [
                {
                    'title': 'сыграть',
                    'hide': True
                },
                {
                    'title': 'Нет',
                    'hide': True
                }
            ]
    else:
        if sessionStorage[user_id]['counter'] == 3:
            res['response']['text'] = 'Молодец! Вот твоя награда!'
            res['response']['buttons'] = [{
                        "title": "Награда",
                        "url": "https://ru.wikipedia.org/wiki/"+
                        sessionStorage[user_id]['место'],
                        "hide": True
                    }]
            res['end_session'] = True
        else:
            if ''.join(sessionStorage[user_id]['curAns']) in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['counter'] += 1
                play_game(res, req)
            else:
                res['response']['text'] = 'Извините, но вы проиграли'
                res['end_session'] = True
    return


def get_cities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value']:
                cities.append(entity['value']['city'])
    return cities


def play_game(res, req):
    user_id = req['session']['user_id']
    place = sessionStorage[user_id]['место']
    loc = list(map(lambda x:''.join(str(x).split(',')), list(map(lambda x:''.join(str(x).split('.')), get_coordinates(place)))))
    sessionStorage[user_id]['curAns'] = sorted(list(map(lambda x: x[(sessionStorage[user_id]['counter'] - 1)*2:sessionStorage[user_id]['counter']*2], loc)))
    res['response']['text'] = \
        'Запиши слитно корни этого уравнения в порядке возрастания: '+\
        createFunction(sessionStorage[user_id]['curAns'][0],
                       sessionStorage[user_id]['curAns'][1])+' ответ: '+str(sessionStorage[user_id]['curAns'][0])+str(sessionStorage[user_id]['curAns'][1])


if __name__ == '__main__':
    app.run()
