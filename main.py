import telebot
import os


token = '1753739843:AAFeUbQw2lvQs1c-B47ubUsjcxxINZLkoOg'

bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Функция ответа на стартовое сообщение пользователя
    :param message: сообщение от пользователя
    :return:
    """
    new_message = "Привет, я бот для печати документов.\n" \
                  "Отправь мне файл для печати\n\n" \
                  "Доступные форматы: DOC, DOCX, XLS, XLSX, PPT, PPTX, PNG, JPG, JPEG, BMP, EPS, GIF, TXT, RTF, HTML"
    bot.send_message(message.chat.id, new_message)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    """
    Фунция ответа на текстовое сообщение пользователя
    :param message: сообщение от пользователя
    :return:
    """
    chat_id = message.chat.id
    new_message = "Отправь мне файл для печати\n\n" \
                  "Доступные форматы: DOC, DOCX, XLS, XLSX, PPT, PPTX, PNG, JPG, JPEG, BMP, EPS, GIF, TXT, RTF, HTML"
    bot.send_message(chat_id, new_message)


@bot.message_handler(content_types=['document'])
def doc_handler(message):
    """
    Функция валидации и печати файла
    :param message: сообщение от пользователя
    :return:
    """
    chat_id = message.chat.id
    formats = "Доступные форматы: DOC, DOCX, XLS, XLSX, PPT, PPTX, PNG, JPG, JPEG, BMP, EPS, GIF, TXT, RTF, HTML"
    try:
        # получаем файл
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # валидация типа полученного файла
        if str(message.document.file_name).split('.')[-1] not in ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'png',
                                                                  'jpg', 'jpeg', 'bmp', 'eps', 'gif', 'txt', 'rtf',
                                                                  'html']:
            bot.send_message(chat_id, 'Неподдерживаемый формат!\n' + formats)
            return
        src = 'C:/Users/kaimak/PycharmProjects/printBot/files/' + message.document.file_name

        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Распечатал файл!")
        os.startfile("output.pdf")
        os.startfile(src, "print")
    except Exception as e:
        bot.reply_to(message, "Не понял тебя, попробуй снова!")
        print(e)


bot.polling()
