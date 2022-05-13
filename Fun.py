# ======================================= Развлечения
import requests
import re
import bs4
from io import BytesIO  # секретные ключи, пароли

# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Прислать собаку":
        bot.send_message(chat_id, get_dog())

    elif ms_text == "Прислать анекдот":
        bot.send_message(chat_id, text=get_anekdot())


# -----------------------------------------------------------------------
def get_anekdot():  # Анекдоты (Проблема с модулем)
    array_anekdots = []
    req_anek = requests.get("http://anekdotme.ru/random")
    soup = bs4.BeautifulSoup(req_anek.text, "parser")
    result_find = soup.select('.anekdot_text')
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]

# -----------------------------------------------------------------------
def get_dog():  # Cсылки на собак
    global url
    contents = requests.get('https://random.dog/woof.json').json()
    image_url = contents['url']
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = image_url
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url

# -----------------------------------------------------------------------
def get_cur_pairs():
    lst_cur_pairs = []
    req_currency_list = requests.get(f'https://currate.ru/api/?get=currency_list&key={5241329098:AAFwTwBMDbk8fD-GVHlXBlz52jI9X4SWoVk}')
    if req_currency_list.status_code == 200:
        currency_list_json = req_currency_list.json()
        for pairs in currency_list_json["data"]:
            if pairs[3:] == "RUB":
                lst_cur_pairs.append(pairs)
    return lst_cur_pairs


# -----------------------------------------------------------------------
def get_cur():
    txt_curses = ""
    txt_pairs = ",".join(get_cur_pairs())
    req_currency_rates = requests.get(f'https://currate.ru/api/?get=rates&pairs={txt_pairs}&key={5241329098:AAFwTwBMDbk8fD-GVHlXBlz52jI9X4SWoVk}')
    if req_currency_rates.status_code == 200:
        currency_rates = req_currency_rates.json()
        for pairs, rates in currency_rates["data"].items():
            txt_curses += f"{pairs} : {rates}\n"
    else:
        txt_curses = req_currency_rates.text
    return txt_curses

# ---------------------------------------------------------------------
