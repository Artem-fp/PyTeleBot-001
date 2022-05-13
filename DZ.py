import telebot

# -----------------------------------------------------------------------
# def dz1(bot, chat_id):
#     M_name = "Артём"
#print(M_name) bot.send_message(chat_id, text="ДОДЕЛАТЬ")

# -----------------------------------------------------------------------
# def dz2(bot, chat_id):
    #M_age = '19'print("Здравствуй, взрослая жизнь мне", M_age) bot.send_message(chat_id, text="ДОДЕЛАТЬ")


# -----------------------------------------------------------------------
# def dz3(bot, chat_id):
    # Spam = M_name * 5
    # print(Spam)
    # bot.send_message(chat_id, text="ДОДЕЛАТЬ")

# -----------------------------------------------------------------------
# def dz4(bot, chat_id):
#     name = input('Введите ваше имя\n')
#     age = int(input("Сколько вам лет\n"))
#     print("Здравствуйте,", name)
#     if age < 18:
#         print('Ты еще мал, чтобы понимать мои шутки\n')
#     elif age >= 18:
#         print("Здравствуй, товарищ по несчастью\n")
#     elif age >= 20:
#         print("Здравствуй, старичок. Песочек не мешает, коленки не болят?\n")
#     bot.send_message(chat_id, text="ДОДЕЛАТЬ")
#
# # -----------------------------------------------------------------------
# def dz5(bot, chat_id):
#     my_inputInt(bot, chat_id, "Сколько вам лет?", dz5_ResponseHandler)
#
#
# def dz5_ResponseHandler(bot, chat_id, age_int):
#     bot.send_message(chat_id, text=f"О! тебе уже {age_int}! \nА через год будет уже {age_int + 1}!")
#
# # -----------------------------------------------------------------------
# def dz6(bot, chat_id):
#     # 6
#     print(name[2:-1])
#     print(name[::-1])
#     print(name[:3])
#     print(name[5:])
#     dz6_ResponseHandler = lambda message: bot.send_message(chat_id,
#                                                            f"Добро пожаловать {message.text}! У тебя красивое имя, в нём {len(message.text)} букв!")
#     my_input(bot, chat_id, "Как тебя зовут?", dz6_ResponseHandler)
#
# # -----------------------------------------------------------------------
# def dz7(bot, chat_id): #7.Список
# A = 1 #Срез
# result =[]
# for i in range(0, len(str(age)), A):
#     result.append(int(str(age)[i: i + A]))
# print("\nЛист : " + str(result))
#
# #Перебираем значения листа -> плюсуем, множим
# div = 1
# sm = 0
#
# for i in result:
#     div = div * i
#     sm = sm + i
# print('\nСумма='+str(sm), '\nПроизведение ='+str(div), "\n")
# # -----------------------------------------------------------------------
# def dz8(bot, chat_id, U):
#     U = name.capitalize()
# bot.send_message (chat_id, name.upper(), (name.lower(), (name.title()), U.swapcase()))
#
# # -----------------------------------------------------------------------
# def dz9(bot, chat_id):
# prob = 0
# while 1:
#     try:
#         if (age < 1) or (age > 150):
#             print("ГОДА")
#             raise prob
#         elif str.isspace(name):
#             print("Ошибка ввода\n")
#             raise prob
#         else:
#             print("ИМЯ")
#         continue
#     except prob as err:
#         break
# # -----------------------------------------------------------------------
# def dz10(bot, chat_id):
# pr = int(input("\nСколько будет 2*2+2\n"))
# if pr == 6:
#     print("Ты прав, а теперь решаем выш мат!")
# else:
#     print("Эх, брат, гугли порядок действий...")
# # -----------------------------------------------------------------------
# def my_input(bot, chat_id, txt, ResponseHandler):
#     message = bot.send_message(chat_id, text=txt)
#     bot.register_next_step_handler(message, ResponseHandler)
#
#
# # -----------------------------------------------------------------------
# def my_inputInt(bot, chat_id, txt, ResponseHandler):
#     message = bot.send_message(chat_id, text=txt)
#     bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt,
#                                    ResponseHandler=ResponseHandler)
#     # bot.register_next_step_handler(message, my_inputInt_return, bot, txt, ResponseHandler)  # то-же самое, но короче
#
#
# def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
#     chat_id = message.chat.id
#     try:
#         if message.content_type != "text":
#             raise ValueError
#         var_int = int(message.text)
#         # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
#         ResponseHandler(botQuestion, chat_id, var_int)
#     except ValueError:
#         botQuestion.send_message(chat_id,
#                                  text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
#         my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже
#         # у нас пара процедур, которые вызывают друг-друга, пока пользователь не введёт корректные данные,
#         # и тогда этот цикл прервётся, и управление перейдёт "наружу", в ResponseHandler
#
# # -----------------------------------------------------------------------
