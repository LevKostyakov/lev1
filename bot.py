import vk_api, json, datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor



key = "6f2046b582212c540c66df24e33c2722eb9953b34255d5a0ac15cedf037a6e01ef7fccd8c15ef57eb6c8e"
# Авторизуемся как сообщество
vk = vk_api.VkApi(token=key)


def send_message(user_id, message, file_vk_url=None, keyboard=None, car = None):
    from random import randint
    vk.method('messages.send',
              {'user_id': user_id,
               "random_id": randint(1, 1000),
               'message': message,
               'attachment': file_vk_url,
               'keyboard': keyboard,
               'template': car}
              )
def send_message_chat(user_id, message, file_vk_url=None, keyboard=None, car = None):
    from random import randint
    vk.method('messages.send',
              {'chat_id': user_id,
               "random_id": randint(1, 1000),
               'message': message,
               'attachment': file_vk_url,
               'keyboard': keyboard,
               'template': car}
              )


caroysel = {
    "type": "carousel",
    "elements": [
        {
            "photo_id": "-200304763_457239022",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": "Текст кнопки ",
                    "payload": "{}"
                }
            },
                {
                    "action": {
                        "type": "open_link",
                        "link": 'https://vk.com/id328826952',
                        "label": "Текст кнопки ",
                        "payload": "{}"
                    }
                }
            ]
        },
        {
            "photo_id": "-200304763_457239026",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": "Текст кнопки 2",
                    "payload": "{}"
                }
            },
                {
                    "action": {
                        "type": "open_link",
                        "link": 'https://vk.com/id328826952',
                        "label": "Текст кнопки ",
                        "payload": "{}"
                    }
                }
            ]
        },
        {
            "photo_id": "-200304763_457239025",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": "Текст кнопки 3 ",
                    "payload": "{}"
                }
            },
                {
                    "action": {
                        "type": "open_link",
                        "link": 'https://vk.com/id328826952',
                        "label": "Текст кнопки ",
                        "payload": "{}"
                    }
                }
            ]
        }
    ]
}


caroysel = json.dumps(caroysel, ensure_ascii=False).encode('utf-8')
caroysel = str(caroysel.decode('utf-8'))


def generate_keyboard(variants, w=3):
    n = len(variants)
    x = w
    y = n // w
    if n % w:
        y += 1
    n_var = 0
    keyboard = VkKeyboard(one_time=True)
    first = True
    for i in range(y):
        if not first:
            keyboard.add_line()  # Переход на вторую строку
        first = False
        for j in range(x):
            if n_var < n:
                keyboard.add_button(variants[n_var], color=VkKeyboardColor.POSITIVE)
                n_var += 1
    return keyboard.get_keyboard()


keyboard2 = generate_keyboard(["привет", "как дела", "о себе", "карусель", "время"], w=3)

user_data = {}
upload = vk_api.VkUpload(vk)


def upl(filename):
    photo = upload.photo_messages([filename])[0]
    return 'photo{}_{}'.format(photo['owner_id'], photo['id'])


# Работа с сообщениями
longpoll = VkLongPoll(vk)
# Основной цикл
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            text = event.text.lower()
            if event.from_chat:
                user_id = event.chat_id
            else:
                user_id = event.user_id

            if user_id in user_data:
                user_data[user_id]["last_message"].append(text)
            else:
                user_data[user_id] = {"last_message": [text, ],
                                      "room": "main"}
            print(repr((text)))

            # send_message(user_id,'a',file_vk_url = upl('/home/dugeru/Desktop/unnamed.jpeg'))

            if user_data[user_id]["room"] == "main":
                if text == "привет":
                    send_message(user_id, "Привет", keyboard=keyboard2, file_vk_url = upl('memes.webp'))
                                 
                elif (text == "users") and (user_id == admin_id):

                    data_json = json.dumps(user_data, ensure_ascii=False)
                    send_message(user_id, data_json)




                elif text == "карусель":
                    send_message(user_id, "ky", car=caroysel)
                elif text == "как дела":
                    send_message(user_id, "пора", keyboard=keyboard2)
                elif text == "о себе":
                    about_user = vk.method('users.get',
                                           {'user_ids': user_id, 'fields': 'sex, city, country, followers_count'})
                    print(about_user)
                    sex = about_user[0].get('sex')
                    city = about_user[0].get('city').get('title')
                    country = about_user[0].get('country').get('title')
                    followers_count = about_user[0].get('followers_count')

                    message = "Пол: {} \nГород: {} \nСтрана: {} \nПодпичсики: {}".format(sex, city, country,
                                                                                         followers_count)
                    send_message(user_id, message, keyboard=keyboard2)

                elif text == "время":
                    x = str(datetime.datetime.now()).split('.')[0]
                    send_message(user_id, x, keyboard=keyboard2)
                elif text == "города":
                    user_data[user_id]["room"] = "game_goroda"
                    user_data[user_id]["game_data"] = ["а", []]
                    send_message(user_id, "Начинай, тебе на А", keyboard=keyboard2)


                else:
                    send_message(user_id, "ку", keyboard=keyboard2)
            elif user_data[user_id]["room"] == "game_goroda":
                last_letter, goroda = user_data[user_id]["game_data"]
                print((text[0], last_letter), (text not in goroda))
                if (text[0] == last_letter) and (text not in goroda):

                    goroda.append(text)
                    from random import choice

                    bukva = choice("йцукенгшщзззхфывапролджячсмитьбю")
                    user_data[user_id]["game_data"][0] = bukva
                    send_message(user_id, "хорошо, теперь на " + bukva.upper(), keyboard=keyboard2)
                elif (text in goroda):
                    send_message(user_id, "Такой город уже был", keyboard=keyboard2)
                else:
                    send_message(user_id, "чо", keyboard=keyboard2)



