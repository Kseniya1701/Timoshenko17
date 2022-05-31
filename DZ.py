import time

def dz1(bot, chat_id):
    dz1_ResponseHandler = lambda message: bot.send_message(chat_id, f'Привет, {message.text}!')
    my_input(bot, chat_id, 'Введите ваше имя:', dz1_ResponseHandler)

#-------------------------------------------------------------------------------------------------

def dz2(bot, chat_id):
    def dz2_ResponseHandler(bot, chat_id, age_int):
        bot.send_message(chat_id, text=f"Вам {age_int} лет!")

    my_inputInt(bot, chat_id, "Сколько вам лет?", dz2_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz3(bot, chat_id):
    dz3_ResponseHandler = lambda message: bot.send_message(chat_id, f"{message.text*5}")
    my_input(bot, chat_id, 'Введите ваше имя:', dz3_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz45(bot, chat_id):
    def dz45_ResponseHandler(bot, chat_id, age):
        if 0 < age < 7:
            bot.send_message(chat_id, "Фу, малявка...")
        if 8 < age < 18:
            bot.send_message(chat_id, "Вали отсюда, школота ))")
        if age > 19:
            bot.send_message(chat_id, "Ну ты и старый " + str(age) + "?")

    my_inputInt(bot, chat_id, "Введите возраст:", dz45_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz6(bot, chat_id):
    dz6_ResponseHandler = lambda message: bot.send_message(chat_id, f"Привет, {message.text}! Смотри \n"
                                                                    f"{str(message.text[1:len(message.text) - 1:])}\n"
                                                                    f"{str(message.text[::-1])}\n"
                                                                    f"{str(message.text[-3::])}\n"
                                                                    f"{str(message.text[:5:])}\n")
    my_input(bot, chat_id, 'Введите ваше имя:', dz6_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz7n(bot, chat_id):
    dz7n_ResponseHandler = lambda message : bot.send_message(chat_id, f"Привет, {message.text}! Смотри \n"
                                                                      f"Длина вашего имени: " + f"{str(len(message.text))}\n")

    my_input(bot, chat_id, "Введите ваше имя: ", dz7n_ResponseHandler)


def dz7a(bot, chat_id):
    def dz7a_ResponseHandler(bot, chat_id, age):
        bot.send_message(chat_id, "Сумма символов в вашем имени: " + str((age // 10) + (age % 10)))
        bot.send_message(chat_id, "Произведение символов в вашем имени: " + str((age // 10) * (age % 10)))

    my_inputInt(bot, chat_id, "Введите возраст:", dz7a_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz8(bot, chat_id):
    dz8_ResponseHandler = lambda message : bot.send_message(chat_id, f"Привет, {message.text}! Смотри \n"
                                                                         f"{str.upper(message.text)}\n"
                                                                         f"{str.lower(message.text)}\n"
                                                                         f"{str.upper(message.text)[0:1:] + str.lower(message.text)[1::]}\n"
                                                                         f"{str.lower(message.text)[0:1:] + str.upper(message.text)[1::]}\n")
    my_input(bot, chat_id, 'Введите ваше имя:', dz8_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz92(bot, chat_id):
    def dz92_ResponseHandler(bot, chat_id, age):
        if age > 150 or age < 0 :
            bot.send_message(chat_id, 'Ой, такого возраста не существует!')
        else:
            bot.send_message(chat_id, 'Нет ошибки')

    my_inputInt(bot, chat_id, 'Введите возраст: ', dz92_ResponseHandler)

def dz91(bot, chat_id):
    def dz91_ResponseHandler(bot, chat_id, name):
        spaces = 0
        for i in range(0, len(name)) :
            if name[i] == ' ' :
                spaces += 1
                break
            else :
                spaces = 0
        if spaces == 0 :
            bot.send_message(chat_id, 'Нет ошибки')
        else :
            bot.send_message(chat_id, 'Есть ошибка!')

    my_inputStr(bot, chat_id, 'Введите имя: ', dz91_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz10(bot, chat_id):
    bot.send_message(chat_id, "Реши: ")
    time.sleep(1)
    bot.send_message(chat_id, "1/2*x*y+(47-x-y)*(x/3+y/4)")


    def dz10_ResponseHandler(bot, chat_id, ans):
        if ans == 282 :
            time.sleep(1)
            bot.send_message(chat_id, "молодец")
        else :

            time.sleep(1)
            bot.send_message(chat_id, "Ну, ты старался)")

    my_inputInt(bot, chat_id, "ЖДУ...", dz10_ResponseHandler)


#дописать
def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)

def my_inputInt(bot, chat_id, txt, ResponseHandler):

    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)

def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        var_int = int(message.text)
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                         text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)

def my_inputStr(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputStr_SecondPart, botQuestion=bot, txtQuestion=txt,
                                   ResponseHandler=ResponseHandler)

def my_inputStr_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id

    var_str = str(message.text)
    ResponseHandler(botQuestion, chat_id, var_str)