
import random
from telebot import types
from MenuBot import goto_menu
import json
import os

activeGames = {}

def newgame(chatID, newGame):
    activeGames.update({chatID: newGame})
    return newGame

def getgame(chatID):
    return activeGames.get(chatID)

def stopgame(chatID):
    activeGames.pop(chatID)

if_heroku = ""

if os.environ.get('HEROKU'):
    if_heroku = "Games/"

class Translation:
    """
    Класс переводчика.
    """
    __players = {}
    __menu_translation_path = f'{if_heroku}Translations/menu.json'
    __slots_translation_path = f'{if_heroku}Translations/slots.json'
    __xo_translation_path = f'{if_heroku}Translations/xo.json'
    __bj_translation_path = f'{if_heroku}Translations/bj.json'
    __hm_translation_path = f'{if_heroku}Translations/hangman.json'
    __dating_translation_path = f'{if_heroku}Translations/dating.json'
    __tora_translation_path = f'{if_heroku}Translations/TorA.json'

    @classmethod
    def get_menu_expression(cls, key: str, user_id: int) -> str:
        """
        Метод получения выражения из menu.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        if user_id not in cls.__players:
            cls.set_lang(user_id)

        with open(cls.__menu_translation_path, "r", encoding="utf8") as read:
            return json.load(read)[key][cls.__players[user_id]]

    @classmethod
    def get_dating_menu_expression(cls, key, user_id):
        """
        Метод получения menu выражения из dating.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__dating_translation_path, "r", encoding="utf8") as read:
            return json.load(read)["menu"][key][cls.get_player_language(user_id)]

    @classmethod
    def get_dating_log_expression(cls, key):
        """
        Метод получения log выражения из dating.json по ключу.

        :param key: Ключ.
        :return: Выражение.
        """
        with open(cls.__dating_translation_path, "r", encoding="utf8") as read:
            return json.load(read)["log"][key]

    @classmethod
    def get_tora_true_dict(cls):
        """
        Метод получения true выражения из TorA.json.

        :return: Выражение.
        """
        with open(cls.__tora_translation_path, "r", encoding="utf8") as read:
            return json.load(read)['true']

    @classmethod
    def get_tora_action_dict(cls):
        """
        Метод получения action выражения из TorA.json.

        :return: Выражение.
        """
        with open(cls.__tora_translation_path, "r", encoding="utf8") as read:
            return json.load(read)['action']

    @classmethod
    def get_tora_menu_expression(cls, key, user_id):
        """
        Метод получения menu выражения из TorA.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__tora_translation_path, "r", encoding="utf8") as read:
            return json.load(read)['menu'][key][cls.get_player_language(user_id)]

    @classmethod
    def get_bj_expression(cls, key, user_id):
        """
        Метод получения выражения из bj.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__bj_translation_path, "r", encoding="utf8") as read:
            return json.load(read)[key][cls.get_player_language(user_id)]

    @classmethod
    def get_slots_menu_expression(cls, key, user_id):
        """
        Метод получения выражения из slots.json по ключу.

        :param key: Ключ.
        :param user_id: ID пользователя.
        :return: Выражение.
        """
        with open(cls.__slots_translation_path, "r", encoding="utf8") as read:
            return json.load(read)[key][cls.get_player_language(user_id)]

    @classmethod
    def get_player_language(cls, user_id):
        """
        Метод получения языка игрока.

        :param user_id: ID игрока.
        :return: Язык.
        """
        if user_id not in cls.__players:
            cls.__players[user_id] = 0
        return cls.__players[user_id]

    @staticmethod
    def switch_language(user_id):
        """
        Метод смены языка.

        :param user_id: ID игрока.
        """
        if user_id in Translation.__players:
            if Translation.__players[user_id] == 0:
                Translation.__players[user_id] = 1
            else:
                Translation.__players[user_id] = 0

    @classmethod
    def set_lang(cls, user_id):
        """
        Метод установки языка.

        :param user_id: ID пользователя.
        """
        if user_id not in cls.__players:
            cls.__players[user_id] = 0
        else:
            cls.__players[user_id] = 1

    @classmethod
    def set_language(cls, user_id, lang):
        """
        Метод установки языка (улучшенный).

        :param user_id: ID пользователя.
        :param lang: Язык.
        """
        cls.__players[user_id] = lang

    @classmethod
    def get_language(cls, user_id):
        """
        Метод получения языка пользователя (улучшенный).

        :param user_id: ID пользователя
        :return: Язык
        """
        return cls.__players[user_id]


class Slots:
    """
    Класс игры Слоты.
    """
    @property
    def flag(self):
        """
        Геттер флага.

        :return: Флаг.
        """
        return self.__flag

    # Поток обработки сообщений
    @staticmethod
    def main_slots(call, bot):
        """
        Метод редактирования сообщения и кнопки при вызове "Slots".

        :param call: Вызов.
        :param bot: Бот.
        """
        markup = types.InlineKeyboardMarkup(row_width=3)
        b = types.InlineKeyboardButton(Translation.get_slots_menu_expression("spin", call.from_user.id),
                                       callback_data='spin')
        markup.add(b)
        bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=markup,
                              text=Translation.get_slots_menu_expression("slots", call.from_user.id),
                              message_id=call.message.message_id)

    @classmethod
    def callback_inline(cls, call, bot):
        """
        Метод обработки Вызовов.

        :param call: Вызов.
        :param bot: Бот.
        """
        cls.__flag = True

        if call.data == "Slots":
            cls.main_slots(call, bot)
            return

        # Код при нажатии на "Play Slots" в меню (сама игра "Слот-Машина")
        if call.data == 'spin':
            i = 0
            array = []

            # Генерация случайного списка, от которого зависит выигрыш
            while i < 9:
                array.append(random.randint(0, 4))
                i = i + 1
            new_array = []
            i = 0

            # Замена случайных чисел на картинки для наглядности
            while i < 9:
                if array[i] == 0:
                    new_array.append("7️⃣")
                elif array[i] == 1:
                    new_array.append("🍒")
                elif array[i] == 2:
                    new_array.append("🍋")
                elif array[i] == 3:
                    new_array.append("🍎")
                elif array[i] == 4:
                    new_array.append("🍉")
                i += 1

            # Удаление inline-кнопки у предыдущего сообщения (остаётся только сообщение "Slots: ")
            bot.edit_message_text(chat_id=call.message.chat.id, reply_markup=None, text=call.message.text,
                                  message_id=call.message.message_id)

            # Подготовка inline-кнопок "Spin!" и "Exit" к следующему сообщению
            markup = types.InlineKeyboardMarkup(row_width=3)
            b1 = types.InlineKeyboardButton(Translation.get_slots_menu_expression("spin", call.from_user.id),
                                            callback_data='spin')
            b2 = types.InlineKeyboardButton(Translation.get_slots_menu_expression("exit", call.from_user.id),
                                            callback_data='Menu')
            markup.add(b1, b2)

            # Крепление inline-меню (кнопки "Spin!" и "Exit") и вывод слотов пользователю


def get_text_messages(bot, cur_user, message):
    chatID = message.chat.id
    ms_text = message.text

    if ms_text == "Играть":

    elif ms_text == "Стоп!":
        stopgame(chatID)
        goto_menu(bot, chatID, "Выход")
        return