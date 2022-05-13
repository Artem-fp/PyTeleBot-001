# Телеграм-бот v. 002 - Меню
import telebot  # pyTelegramBotAPI	4.3.1
from telebot import types  # Импорт модуля Requests
import MenuBot
from MenuBot import Menu
import Games
import DZ
import re
import requests
import Fun
import bs4

bot = telebot.TeleBot(
    '5241329098:AAFwTwBMDbk8fD-GVHlXBlz52jI9X4SWoVk')
# t.me/Artem_Boyarchenko_1MD4_bot # Создаем экземпляр бота @Artem_Boyarchenko_1MD4_bot


# -----------------------------------------------------------------------
# Функция, обрабатывающая команду
@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Главное меню")
    btn2 = types.KeyboardButton("Помощь")
    markup.add(btn1, btn2)
    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я тестовый бот для курса программирования на языке Пайтон".format(
                         message.from_user), reply_markup=markup)


# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Прислать собаку":
        bot.send_message(chat_id, get_dog())


    elif ms_text == "Прислать анекдот":
        bot.send_message(chat_id, text=get_anekdot())

    cur_user = MenuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = MenuBot.Users(chat_id, message.json["from"])

    # проверка = мы нажали кнопку подменю, или кнопку действия
    subMenu = MenuBot.goto_menu(bot, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu is not None:
        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды

        if subMenu.name == "Игра в 21":
            game21 = Games.newGame(chat_id, Games.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=game21.mediaCards)  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif subMenu.name == "Игра КНБ":
            gameRPS = Games.newGame(chat_id, Games.RPS())  # создаём новый экземпляр игры и регистрируем его
            bot.send_photo(chat_id, photo=gameRPS.url_picRules, caption=gameRPS.text_rules, parse_mode='HTML')

        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    # проверим, является ли текст текущий команды кнопкой действия
    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu is not None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню
        module = cur_menu.module

        if module != "":  # проверим, есть ли обработчик для этого пункта меню в другом модуле, если да - вызовем его (принцип инкапсуляции)
            exec(module + ".get_text_messages(bot, cur_user, message)")

        if ms_text == "Помощь":
            help(bot, chat_id)

    else:  # ======================================= случайный текст
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        MenuBot.goto_menu(bot, chat_id, "Главное меню")


# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать один или несколько параметров в обработчик кнопки,
    # используйте методы Menu.getExtPar() и Menu.setExtPar()
    # call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    # После обработки каждого запроса вызовете метод answer_callback_query(), чтобы Telegram понял, что запрос обработан
    chat_id = call.message.chat.id
    message_id = call.message.id
    cur_user = MenuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = MenuBot.Users(chat_id, call.message.json["from"])

    tmp = call.data.split("|")
    menu = tmp[0] if len(tmp) > 0 else ""
    cmd = tmp[1] if len(tmp) > 1 else ""
    par = tmp[2] if len(tmp) > 2 else ""

    if menu == "GameRPSm":
        Games.callback_worker(bot, cur_user, cmd, par, call)  # обработчик кнопок игры находится в модули игры

# -----------------------------------------------------------------------
# Модули запросов
def help(bot, chat_id):
    bot.send_message(chat_id, "Автор: Боярченко Артём")
    key1 = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/ArtemBoyarch")  # Ссылка на себя
    key1.add(btn1)
    img = open('i6lASX19BOY.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=key1)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in MenuBot.Users.activeUsers:
        bot.send_message(chat_id, MenuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')

def MediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias

def get_dog():  # Cсылки на картиночки собак
    global url
    contents = requests.get('https://random.dog/woof.json').json()
    image_url = contents['url']
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = image_url
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url

def get_anekdot():  # Анекдоты (Проблема с модулем)
    array_anekdots = []
    req_anek = requests.get("http://anekdotme.ru/random")
    soup = bs4.BeautifulSoup(req_anek.text, "parser")
    result_find = soup.select('.anekdot_text')
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]

# -----------------------------------------------------------------------

bot.polling(none_stop=True, interval=0)  # Запускаем бота
