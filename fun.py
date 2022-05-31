# ======================================= Развлечения
import requests
import bs4  # BeautifulSoup4
from telebot import types
from io import BytesIO
import SECRET  # секретные ключи, пароли

# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

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