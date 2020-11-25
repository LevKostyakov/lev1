import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
key = "1e73597d9953a32cb53dfaa97075427b9ebb0db5972dcc92485395e3b508c782efdb44e1091bd8edf06fd"
# Авторизуемся как сообщество
vk = vk_api.VkApi(token=key)

def send_message(user_id, message, file_vk_url = None, keyboard = None):
                from random import randint
                vk.method('messages.send',
                          {'user_id': user_id,
                           "random_id":randint(1,1000) ,
                           'message': message,
                           'attachment':file_vk_url,
                           'keyboard':keyboard}
                          )
keyboard = VkKeyboard(one_time=True)

keyboard.add_button('привет')
keyboard.add_line()  # Переход на вторую строку

keyboard.add_button('давай угодаю число')

    # Работа с сообщениями
longpoll = VkLongPoll(vk)
# Основной цикл
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            text = event.text.lower()
            user_id = event.user_id
            print(repr(text))
            if text == "привет":
                send_message(user_id, "Привет",  keyboard = keyboard.get_keyboard())
            elif text == "как дела":
                send_message(user_id, "ой мне пора пока")
            else:
                send_message(user_id, "ку", keyboard = keyboard.get_keyboard())
            

