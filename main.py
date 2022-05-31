# Телеграм-бот v.004
import json
from gettext import find
from io import BytesIO
import telebot
from telebot import types
import requests
import bs4
import botGames
import menuBot
from menuBot import Menu, Users
import DZ
import wikipedia, re

wikipedia.set_lang("ru")

bot = telebot.TeleBot('5242721464:AAEGTV21OggWh_bRXCiqL_wVIqE4Jjlcz5c')


# -----------------------------------------------------------------------

@bot.message_handler(commands="start")
def command(message, res=False):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE4PdilRWWk0HOmMJ3IzeY_UELVLOw4QACbgUAAj-VzAqGOtldiLy3NSQE")
    txt_message = f"Привет, {message.from_user.first_name}! Добро пожаловать в чат-бот"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)


@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)


@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)

@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    voice = message.voice
    bot.send_message(message.chat.id, voice)

@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)

@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)

@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")

@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)

@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)

# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = Users.getUser(chat_id)
    if cur_user == None:
        cur_user = Users(chat_id, message.json["from"])

    # проверка = мы нажали кнопку подменю, или кнопку действия
    subMenu = menuBot.goto_menu(bot, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu is not None:
        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if subMenu.name == "Игра в 21":
            game21 = botGames.newGame(chat_id, botGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif subMenu.name == "Игра КНБ":
            gameRPS = botGames.newGame(chat_id, botGames.GameRPS())  # создаём новый экземпляр игры и регистрируем его
            text_game = "<b>Победитель определяется по следующим правилам:</b>\n" \
                        "1. Камень побеждает ножницы\n" \
                        "2. Бумага побеждает камень\n" \
                        "3. Ножницы побеждают бумагу\n" \
                        "подробная информация об игре: <a href='https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D0%BC%D0%B5%D0%BD%D1%8C,_%D0%BD%D0%BE%D0%B6%D0%BD%D0%B8%D1%86%D1%8B,_%D0%B1%D1%83%D0%BC%D0%B0%D0%B3%D0%B0'>Wikipedia</a>"
            bot.send_photo(chat_id, photo="https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg", caption=text_game,
                           parse_mode='HTML')

        elif subMenu.name == "Кубик":
            gameCUBE = botGames.newGame(chat_id, botGames.GameCUBE(bot))
            text_game = "Играть могут сколько угодно человек, вначале игрок загадывает число от 1 до 6, " \
                        "если оно совпадает с подброшенными костями, то игрок выбывает, иначе ему зачисляется " \
                        "разница очков"
            bot.send_message(chat_id, text=text_game)

        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    # проверим, является ли текст текущий команды кнопкой действия
    cur_menu = Menu.getCurMenu(chat_id)

    if cur_menu != None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню

        if ms_text == "Помощь":
            send_help(chat_id)

        elif ms_text == "Книга":
            bot.send_message(chat_id, get_book())

        elif ms_text == "Поиск по названию":
            bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE4QNilRZ5cSmPpIU4WCzvwCqMCu1MgQACMwEAAvcCyA87yuGU7tlOzSQE")
            bot.send_message(chat_id, 'Отправь мне название книги. Я попробую ее найти.')
            bot.register_next_step_handler(message, search_book)

        elif ms_text == "Поиск по автору":
            bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE4QtilRb08UJo_DKX4CNO4jKQCGb72QACSgMAArVx2gbCfgb6m0gexCQE")
            bot.send_message(chat_id, 'Отправь мне имя автора. Я попробую его найти.')
            bot.register_next_step_handler(message, search_author)

        elif ms_text == "Собака":
            bot.send_photo(chat_id, photo=get_dogURL(), caption="Твоя собачка!")

        elif ms_text == "Котик":
            bot.send_photo(chat_id, photo=get_kotik(), caption="Твоя кошечка!")

        elif ms_text == "Анекдот":
            bot.send_message(chat_id, text=get_anekdot())

        elif ms_text == "Цитата":
            bot.send_message(chat_id, text=get_citaty())

        elif ms_text == "Фильм":
            send_film(chat_id)

        elif ms_text == "Википедия":
            bot.send_sticker(chat_id, "CAACAgIAAxkBAAEE4RFilReMLujy8Saa_ZVrVnC8NW6A3QACFwADlp-MDlZMBDUhRlElJAQ")
            msg = bot.send_message(chat_id, 'Отправьте слово, и я найду его значение в Wikipedia.org')
            bot.register_next_step_handler(msg, wikipedia_step)

        elif ms_text == "Число":
            bot.send_message(chat_id, text=get_number())

        elif ms_text == "Угадай кто?":
            get_ManOrNot(chat_id)

        # ======================================= реализация игры в 21

        elif ms_text == "Карту!":
            game21 = botGames.getGame(chat_id)
            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                menuBot.goto_menu(bot, chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                botGames.stopGame(chat_id)
                menuBot.goto_menu(bot, chat_id, "Выход")
                return

        elif ms_text == "Стоп!":
            botGames.stopGame(chat_id)
            menuBot.goto_menu(bot, chat_id, "Выход")
            return

        # ==================================================================

        elif ms_text in botGames.GameRPS.values:
            gameRPS = botGames.getGame(chat_id)
            if gameRPS == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                menuBot.goto_menu(bot, chat_id, "Выход")
                return
            text_game = gameRPS.playerChoice(ms_text)
            bot.send_message(chat_id, text=text_game)

        # ======================================================================

        elif ms_text == "Начать":
            #print("cube nachat'")
            gameCUBE = botGames.getGame(chat_id)
            if gameCUBE == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                menuBot.goto_menu(bot, chat_id, "Выход")
                return
            gameCUBE.start(cur_user.id, cur_user.userName)
            #print("cube nachat'_end")

        # ======================================= реализация игры Камень-ножницы-бумага Multiplayer
        elif ms_text == "Игра КНБ-MP":
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text="Создать новую игру", callback_data="GameRPSm|newGame")
            keyboard.add(btn)
            numGame = 0
            for game in botGames.activeGames.values():
                if type(game) == botGames.GameRPS_Multiplayer:
                    numGame += 1
                    btn = types.InlineKeyboardButton(
                        text="Игра КНБ-" + str(numGame) + " игроков: " + str(len(game.players)),
                        callback_data="GameRPSm|Join|" + menuBot.Menu.setExtPar(game))
                    keyboard.add(btn)
            btn = types.InlineKeyboardButton(text="Вернуться", callback_data="GameRPSm|Exit")
            keyboard.add(btn)

            bot.send_message(chat_id, text=botGames.GameRPS_Multiplayer.name, reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(chat_id, "Вы хотите начать новую игру, или присоединиться к существующей?",
                             reply_markup=keyboard)

        # ===========================================================
        elif ms_text == "Задание-1":
            DZ.dz1(bot, chat_id)

        elif ms_text == "Задание-2":
            DZ.dz2(bot, chat_id)

        elif ms_text == "Задание-3":
            DZ.dz3(bot, chat_id)

        elif ms_text == "Задание-45":
            DZ.dz45(bot, chat_id)

        elif ms_text == "Задание-6":
            DZ.dz6(bot, chat_id)

        elif ms_text == "Задание-7a":
            DZ.dz7a(bot, chat_id)

        elif ms_text == "Задание-7n":
            DZ.dz7n(bot, chat_id)

        elif ms_text == "Задание-8":
            DZ.dz8(bot, chat_id)

        elif ms_text == "Задание-91":
            DZ.dz91(bot, chat_id)

        elif ms_text == "Задание-92":
            DZ.dz92(bot, chat_id)

        elif ms_text == "Задание-10":
            DZ.dz10(bot, chat_id)

        # =================================================================
    else:
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        menuBot.goto_menu(bot, chat_id, "Главное меню")


# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать параметр или несколько параметров в обработчик кнопки,
    # используйте методы Menu.getExtPar() и Menu.setExtPar()
    # call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    # После обработки каждого запроса вызовете метод answer_callback_query(), чтобы Telegram понял, что запрос обработан
    chat_id = call.message.chat.id
    message_id = call.message.id
    cur_user = Users.getUser(chat_id)
    if cur_user == None:
        cur_user = Users(chat_id, call.message.json["from"])

    tmp = call.data.split("|")
    menu = tmp[0] if len(tmp) > 0 else ""
    cmd = tmp[1] if len(tmp) > 1 else ""
    par = tmp[2] if len(tmp) > 2 else ""

    if menu == "GameRPSm":

        if cmd == "newGame":
            # bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)  # удалим кнопки начала игры из чата
            bot.delete_message(chat_id, message_id)
            botGames.newGame(chat_id, botGames.GameRPS_Multiplayer(bot, cur_user))
            bot.answer_callback_query(call.id)

        elif cmd == "Join":
            # bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)  # удалим кнопки начала игры из чата
            bot.delete_message(chat_id, message_id)
            gameRSPMult = Menu.getExtPar(par)
            if gameRSPMult is None:  # если наткнулись на кнопку, которой быть не должно
                return
            else:
                gameRSPMult.addPlayer(cur_user.id, cur_user.userName)
            bot.answer_callback_query(call.id)

        elif cmd == "Exit":
            bot.delete_message(chat_id, message_id)
            gameRSPMult = Menu.getExtPar(par)
            if gameRSPMult is not None:
                gameRSPMult.delPlayer(cur_user.id)
            menuBot.goto_menu(bot, chat_id, "Игры")
            bot.answer_callback_query(call.id)

        elif "Choice-" in cmd:
            gameRSPMult = Menu.getExtPar(par)
            if gameRSPMult is None:  # если наткнулись на кнопку, которой быть не должно - удалим её из чата
                bot.delete_message(chat_id, message_id)
            else:
                choice = cmd[7:]
                gameRSPMult.playerChoice(cur_user.id, choice)
            bot.answer_callback_query(call.id)

    # ==================================================

    elif menu == "GameCUBE":

        if "Choice-" in cmd:
            gameCUBE = Menu.getExtPar(par)
            if gameCUBE is None:  # если наткнулись на кнопку, которой быть не должно - удалим её из чата
                bot.delete_message(chat_id, message_id)
            else:
                choice = cmd[7:]
                if choice == "Game":
                    gameCUBE.input_1(cur_user.id)
                elif choice == "Score":
                    gameCUBE.CheckGlobalScore(cur_user.id)
            bot.answer_callback_query(call.id)

        elif cmd == "Exit":
            bot.delete_message(chat_id, message_id)
            gameCUBE = Menu.getExtPar(par)
            if gameCUBE is not None:
                gameCUBE.delPlayer(cur_user.id)
            menuBot.goto_menu(bot, chat_id, "Игры")
            bot.answer_callback_query(call.id)

# -----------------------------------------------------------------------

def goto_menu(chat_id, name_menu):
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        if target_menu.name == "Игра в 21":
            game21 = botGames.newGame(chat_id, botGames.Game21(jokers_enabled=True))
            text_game = game21.get_cards(2)
            bot.send_media_group(chat_id, media=getMediaCards(game21))
            bot.send_message(chat_id, text=text_game)
        return True
    else:
        return False


# -----------------------------------------------------------------------

def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias


# -----------------------------------------------------------------------

def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Тимошенко Ксения")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/Xenia1701")
    markup.add(btn1)
    img = open('99999.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=markup)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in menuBot.Users.activeUsers:
        bot.send_message(chat_id, menuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')


# -----------------------------------------------------------------------

def get_number():
    array_num = []
    req_numbers = requests.get('https://calculator888.ru/random-generator')
    if req_numbers.status_code == 200:
        soup = bs4.BeautifulSoup(req_numbers.text, "html.parser")
        result_find = soup.select('.blok_otvet')
        for result in result_find:
            array_num.append(result.getText().strip())
    if len(array_num) > 0:
        return array_num[0]
    else:
        return ""


# -----------------------------------------------------------------------

def get_book():
    array_books = []
    req_book = requests.get('https://readly.ru/books/i_am_lucky/?show=1')
    soup = bs4.BeautifulSoup(req_book.text, "html.parser")
    result_find = soup.select("a > img")
    result_find2 = soup.select('.blvi__title, .blvi__book_info')
    for img in result_find:
        img_url = img.attrs.get("src")
    book_image = f"https://readly.ru/{img_url}"
    for result in result_find2:
        array_books.append(result.getText())
    return book_image + array_books[0] + array_books[1]


# -----------------------------------------------------------------------

def get_citaty():
    citaty = []
    avtor = []
    req_ci = requests.get("https://citaty.info/random")
    soup = bs4.BeautifulSoup(req_ci.text, "html.parser")
    res = soup.find_all(class_='field-item even last')
    avt = soup.find_all(class_="field-item even")
    for res4 in res:
        citaty.append(res4.getText().strip())
    for avt4 in avt:
        avtor.append(avt4.getText())
    citaty = citaty[0]
    wh = ""
    try:
        for i in range(0, len(avtor)):
            if wh == "":
                wh += avtor[i]
            elif avtor[i] == avtor[i].lower():
                break
            else:
                wh += ", " + avtor[i]
        authors = "\n\n" + wh
    except IndexError:
        authors = ''
    citaty = '" ' + citaty.replace("\xa0", " ") + ' "' + authors
    return citaty


# -----------------------------------------------------------------------

def search_author(message):
    chat_id = message.chat.id
    ms_text1 = message.text
    try:
        array_authors = []
        url = f"https://readly.ru/search/?q={ms_text1}"
        book_href = requests.get(url)
        soup = bs4.BeautifulSoup(book_href.content, "html.parser")
        for a in soup.select("figure > a"):
            array_authors.append(a.get('href'))
        searchQuery = array_authors[0]
        author_href = f"https://readly.ru/{searchQuery}"
        bot.send_message(chat_id, text="Похоже вы искали этого автора" + '\n' + author_href)
    except Exception:
        bot.send_message(chat_id, text="Такой автор не найден")


# -----------------------------------------------------------------------

def search_book(message):
    chat_id = message.chat.id
    ms_text = message.text
    try:
        array_books = []
        url = f"https://readly.ru/search/?q={ms_text}"
        books_href = requests.get(url)
        soup = bs4.BeautifulSoup(books_href.content, "html.parser")
        for a in soup.select("figure > div > a", rel="nofollow"):
            array_books.append(a.get('href'))
        searchQuery = array_books[0]
        book_href = f"https://readly.ru/{searchQuery}"
        bot.send_message(chat_id, text="Похоже вы искали эту книгу" + '\n' + book_href)
    except Exception:
        bot.send_message(chat_id, text="Такая книга не найдена")


# -----------------------------------------------------------------------

def send_film(chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


# -----------------------------------------------------------------------

def get_anekdot():
    array_anekdots = []
    req_anek = requests.get('http://anekdotme.ru/random')
    if req_anek.status_code == 200:
        soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
        result_find = soup.select('.anekdot_text')
        for result in result_find:
            array_anekdots.append(result.getText().strip())
    if len(array_anekdots) > 0:
        return array_anekdots[0]
    else:
        return ""


# -----------------------------------------------------------------------

def get_dogURL():
    url = ""
    req = requests.get('https://random.dog/woof.json')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['url']
    return url

# -----------------------------------------------------------------------

def get_kotik():
    url = ""
    req = requests.get("https://api.thecatapi.com/v1/images/search")
    if req.status_code == 200:
        r_json = req.json()
        url = r_json[0]["url"]
    return url

# -----------------------------------------------------------------------

def get_ManOrNot(chat_id):
    global bot

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить",
                                      url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")


# ---------------------------------------------------------------------

def wikipedia_step(message):
    m = message.text

    try:
        ny = wikipedia.page(m)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not ('==' in x):
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('{[^\{\}]*\)', '', wikitext2)
        ans = wikitext2

    except Exception as e:
        ans = 'Ничего не могу найти, попробуй еще раз'

    bot.send_message(message.chat.id, ans)


# ---------------------------------------------------------------------

def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm


# ---------------------------------------------------------------------

bot.polling(none_stop=True, interval=0)

print()