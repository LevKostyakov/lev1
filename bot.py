import vk_api, json, datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from city_lib import get_city
from library_with_map_stuff import do_map_stuff, proverka


key = "6f2046b582212c540c66df24e33c2722eb9953b34255d5a0ac15cedf037a6e01ef7fccd8c15ef57eb6c8e"
admin_id = 76904317
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
            "photo_id": "-200304212_457239017",
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
                        "link": 'https://vk.com/schedrov1',
                        "label": "Текст кнопки ",
                        "payload": "{}"
                    }
                }
            ]
        },
        {
            "photo_id": "-109837093_457242811",
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
                        "link": 'https://vk.com/footballru',
                        "label": "Текст кнопки ",
                        "payload": "{}"
                    }
                }
            ]
        },
        {
            "photo_id": "-109837093_457242811",
            "action": {
                "type": "open_photo"
            },
            "buttons": [{
                "action": {
                    "type": "text",
                    "label": "куукук ",
                    "payload": "{}"
                }
            },
                {
                    "action": {
                        "type": "open_link",
                        "link": 'https://vk.com/public200304212',
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
    photo = upload.photo_messages( [filename])[0]
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
                user_data[user_id] = {"last_message":[text,],
                                      "room":"main"}
            print(repr((text)))

            

            #send_message(user_id,'a',file_vk_url = upl('/home/dugeru/Desktop/unnamed.jpeg'))

            if user_data[user_id]["room"] == "main":
                if text == "карта":
                    send_message(user_id, "Привет", keyboard=keyboard2, file_vk_url = upl('map.png'))
                elif (text == "users") and (user_id == admin_id):
                    
                    data_json = json.dumps(user_data, ensure_ascii=False)
                    send_message(user_id,data_json)



                    
                elif text == "карусель":
                    send_message(user_id, "ku", car=caroysel)
                elif text == "как дела":
                    send_message(user_id, "ой мне пора пока", keyboard=keyboard2)
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
                    user_data[user_id]["game_data"]=["а",[]]
                    send_message(user_id, "Начинай, тебе на А", keyboard=keyboard2)


                else:
                    if "карта" in text:
                        map_type = "map"
                    elif "спутник" in text:
                        map_type = "sat"
                    else:
                        map_type = "sat"
                    if "близко" in text:
                        scale = "0.02,0.02"
                    elif "из космоса" in text:
                        scale = "20,20"
                    else:
                        scale = "1,1"


                        
                    map_info = do_map_stuff(text, map_type, scale)
                    map_file = map_info[2]
                    send_message(user_id, "ку", keyboard=keyboard2, file_vk_url = upl("map.png"))





            elif user_data[user_id]["room"] == "game_goroda":
                last_letter, goroda = user_data[user_id]["game_data"]
                if text == "такого города нет":
                    map_info = do_map_stuff(goroda[-1], map_type = 'map', scale = '1,1')
                    if map_info is None:
                        send_message(user_id, "и правда")
                        continue
                    send_message(user_id, "зря не веригь",  file_vk_url = upl("map.png"))

                    send_message(user_id, "тебе на "+last_letter, keyboard=keyboard2)
                elif text == 'ок':
                    send_message(user_id, "хорошо, тебе на "+bukva.upper(), keyboard=keyboard2)

                elif text == 'выход':
                    send_message(user_id, "хорошо, тебе на "+bukva.upper(), keyboard=keyboard2)
                
                elif (text[0].lower()==last_letter.lower()) and (text not in goroda):
                    
                    if proverka(text):

                        goroda.append(text)
                        my_gorod = get_city(text[-1], goroda) 
                        if my_gorod is None:
                            send_message(user_id, "ты победил")
                            user_data[user_id]["room"] = 'main'
                            continue
                        goroda.append(my_gorod)
                        b = my_gorod[-1].upper()
                        if b.lower() in 'ьъы':
                            b = my_gorod[-2].upper()
                        
                        user_data[user_id]["game_data"][0] = b
                        text = ("Мой город - "+my_gorod+", теперь тебе на\n" +
                                b)
                        generate_keyboard(["ок", "такого города нет"])
                        send_message(user_id, text, keyboard=keyboard2)
                        
                    
                elif (text in goroda):
                    send_message(user_id, "Такой город уже был", keyboard=keyboard2)
                else:
                    send_message(user_id, "чииивоооо тебе на "+last_letter.upper(), keyboard=keyboard2)                    
                    






