import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from random import randint
key = "f182c62921c4131b033c1c304ae886874ec2957b895b15e5a4260c4d0d9a28d17889ddadf12595e2bd254"
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
                
def get_keyboard_x_y(x,y):
    keyboard = VkKeyboard(one_time=True)
    first = True
    for i in range(y):
        if not first:
            keyboard.add_line()  # Переход на вторую строку
        first = False
        for j in range(x):
            keyboard.add_button('y '+str(i)+','+'x '+str(j))
    return keyboard.get_keyboard()
def generate_keyboard(variants, w=3):
    n = len(variants)
    x = w
    y = n//w
    if n%w:
        y+=1
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

main_keyboard = generate_keyboard(['об авторе','игра','тест','пинг'], w=3)
game_keyboard = generate_keyboard(['камень','ножницы','бумага','назад'], w=1)
back_keyboard = generate_keyboard(['назад'], w=1)
ping_keyboard = generate_keyboard(['назад','пинг'], w=1)
users = {} 

    # Работа с сообщениями
longpoll = VkLongPoll(vk)
# Основной цикл
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:
            user_id = event.user_id
            text = event.text.lower()
            if user_id not in users:
                users[user_id] = {'status':'main'}
            if users[user_id]['status'] == 'main':
                if text == 'об авторе':
                    send_message(user_id, 'Damir',  keyboard = back_keyboard )
                elif text == 'игра':
                    send_message(user_id, 'GAME',  keyboard = game_keyboard )
                    users[user_id]['status'] = 'gaming'
                    users[user_id]['round'] = 0
                    users[user_id]['wins'] = 0
                elif text == 'тест':
                    send_message(user_id, 'тест',  keyboard = back_keyboard )
                elif text == 'пинг':
                    send_message(user_id, 'понг',  keyboard = ping_keyboard )
                else:
                    name = vk.method('users.get', {'user_ids': user_id})
                    name_user = name[0].get('first_name')
                    send_message(user_id, 'Привет ' + name_user,  keyboard = main_keyboard )
                    name = vk.method('users.get', {'user_ids': user_id})
                    name_user = name[0].get('first_name')
            
            if users[user_id]['status'] == 'gaming':
                if text not in ['камень','ножницы','бумага','назад']:
                    send_message(user_id, 'its a game,bro. press buttons',  keyboard = game_keyboard )
                    continue
                if text == 'моя инфа':
                    about_user = vk.method('users.get', {'user_ids': user_id, 'fields': 'sex , bdate , city , contry'})
                    print(about_user)
                    name = about_name[0].get('first_name')
                    bdate = about_bdate[0].get('bdate')
                    sex = about_firstname[0].get('sex')
                    city = about_city[0].get('city')
                    contry = about_contry[0].get('contry').get('city')
                    massage = 'Имя: () \n Город: \n Страна: \n Пол: \n Дата: \n'.format(name, city, contry, sex, bdate)
                    send_massage(user_id, message)

                if text == 'назад':
                    send_message(user_id, 'GG',  keyboard = main_keyboard )
                    users[user_id] = {'status':'main'}
                    continue
                uspeh = randint(1,3)
                if uspeh == 1:
                    send_message(user_id, 'проиграл')
                elif uspeh == 2:
                    send_message(user_id, 'ничья')
                elif uspeh == 3:
                    send_message(user_id, 'выиграл')
                    users[user_id]['wins']  += 1
                else:
                    print(uspeh)
                users[user_id]['round']  +=1
                send_message(user_id, "побед"+str(users[user_id]['wins'])+'/'+str(users[user_id]['round']),  keyboard = game_keyboard )



