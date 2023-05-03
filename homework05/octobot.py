import json
import re
from datetime import datetime, timedelta

import gspread  # type: ignore
import pandas as pd  # type: ignore
import telebot  # type: ignore

bot = telebot.TeleBot("6293226582:AAEpjl4Tz4fpwC87O9C_vGf4vXxOEiLy6bE")
user_data = {}


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:  # работает
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""

    try:
        if len(date.split(divider)[-1]) == 4:
            tmp = date.split(divider)[-1]
            date = date.replace(tmp, str(int(tmp) - 2000))

        current_date = datetime.now().date()
        if divider not in date:
            return False
        date_conv = convert_date(date)
        if date_conv < current_date:
            return False
        if date_conv > current_date + timedelta(days=365):
            return False
        return True
    except ValueError:
        return False


def is_valid_url(url: str = "") -> bool:  # работает
    """Проверяем, что ссылка рабочая"""
    if re.match(r"^(https?|www)\S*\.ru$", url):
        return True
    elif re.match(r"^(?!https?|www)\S*\.ru$", url):
        return True
    elif re.match(r"^en\S*\.[a-z]+\.[a-z]{2,3}$", url):
        return False
    return False


def convert_date(date: str = "01/01/00"):  # работает
    """Конвертируем дату из строки в datetime"""
    divider = r"[\W_]"
    if re.search(divider, date):
        divider = re.search(divider, date).group()  # type: ignore
        return datetime.strptime(date, "%d{divider}%m{divider}%y".format(divider=divider)).date()
    return


def connect_table(message):  # работает
    """Подключаемся к Google-таблице"""
    url = message.text
    if not is_valid_url(url):
        bot.send_message(message.chat.id, "Неверная ссылка")
        return
    sheet_id = "1l9LsHVScJNN2ajugSq6hreSq4Zm7IHJ3-ktTtUq2IWw"
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")


def access_current_sheet():  # работает
    """Обращаемся к Google-таблице"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    df = pd.DataFrame(worksheet.get_all_records())
    return worksheet, tables[max(tables)]["url"], df


def choose_action(message):  # работает
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        bot.send_message(message.chat.id, "Введите ссылку на таблицу")
        bot.register_next_step_handler(message, connect_table)
    elif message.text == "Редактировать предметы":
        subject_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        subject_markup.row("Добавить предмет")
        subject_markup.row("Удалить предмет")
        subject_markup.row("Обновить предмет")
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=subject_markup)
        bot.register_next_step_handler(message, choose_subject_action)
    elif message.text == "Редактировать дедлайн":
        deadline_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        deadline_markup.row("Добавить или обновить дедлайн")
        deadline_markup.row("Удалить дедлайн")
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=deadline_markup)
        bot.register_next_step_handler(message, choose_deadline_action)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        bot.send_message(message.chat.id, "Дедлайны на этой неделе:")
        bot.send_message(message.chat.id, get_deadlines())
    elif message.text == "Очистить таблицу":
        removal_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        removal_markup.row("Да")
        removal_markup.row("Нет")
        bot.send_message(message.chat.id, "Вы уверены, что хотите очистить таблицу?", reply_markup=removal_markup)
        bot.register_next_step_handler(message, choose_removal_option)


def get_deadlines():  # работает
    """Получаем список дедлайнов на этой неделе"""
    _, _, df = access_current_sheet()
    deadlines = df[["Subject", "Deadline"]].values.tolist()
    deadlines = [deadline for deadline in deadlines if is_valid_date(deadline[1])]
    deadlines = "\n".join([" ".join(deadline) for deadline in deadlines])

    if deadlines == "":
        return "Дедлайнов на этой неделе нет"
    return deadlines


def choose_subject_action(message):  # работает
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Добавить предмет":
        bot.send_message(message.chat.id, "Введите название предмета, который хотите добавить")
        bot.register_next_step_handler(message, add_new_subject)
    elif message.text == "Удалить предмет":
        bot.send_message(message.chat.id, "Введите название предмета, который хотите удалить")
        bot.register_next_step_handler(message, delete_subject)
    elif message.text == "Обновить предмет":
        bot.send_message(message.chat.id, "Введите название предмета, который хотите обновить")
        bot.register_next_step_handler(message, subject_updating_option)
    else:
        bot.send_message(message.chat.id, "Команда не распознана")


def choose_deadline_action(message):  # работает
    """Выбираем действие в разделе Редактировать дедлайн"""
    if message.text == "Добавить или обновить дедлайн":
        bot.send_message(message.chat.id, "Введите предмет, у которого хотите добавить или обновить дедлайн")
        bot.register_next_step_handler(message, choose_subject)
    elif message.text == "Удалить дедлайн":
        bot.send_message(message.chat.id, "Введите предмет, у которого хотите удалить дедлайн")
        bot.register_next_step_handler(message, choose_subject_to_delete_deadline)
    else:
        bot.send_message(message.chat.id, "Команда не распознана")


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    if message.text == "Да":
        bot.register_next_step_handler(message, clear_subject_list(message))
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Очистка отменена")
    else:
        bot.send_message(message.chat.id, "Команда не распознана")


def choose_subject(message):  # работает
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    _, _, df = access_current_sheet()
    user_data["subject_to_change_deadline"] = message.text
    if message.text in df["Subject"].values:
        bot.send_message(message.chat.id, "Введите дату дедлайна")
        bot.register_next_step_handler(message, update_subject_deadline)
    else:
        bot.send_message(message.chat.id, "Такого предмета не существует")


def choose_subject_to_delete_deadline(message):
    """Выбираем предмет, у которого надо удалить дедлайн"""
    worksheet, _, df = access_current_sheet()
    user_data["subject_to_delete_deadline"] = message.text
    if message.text in df["Subject"].values:
        worksheet.update_cell(df[df["Subject"] == message.text].index[0] + 2, 3, "")
        bot.send_message(message.chat.id, "Дедлайн удален")
    else:
        bot.send_message(message.chat.id, "Такого предмета не существует")


def update_subject_deadline(message):  # работает
    """Обновляем дедлайн"""
    subject = user_data["subject_to_change_deadline"]
    divider = message.text[re.search(r"[\W_]", message.text).start()]
    if is_valid_date(message.text, divider):
        worksheet, _, df = access_current_sheet()
        if message.text not in df["Deadline"].values[df["Subject"] == subject]:
            worksheet.update_cell(df[df["Subject"] == subject].index[0] + 2, 3, message.text)
            bot.send_message(message.chat.id, "Дедлайн добавлен")
        else:
            bot.send_message(message.chat.id, "Такой дедлайн уже существует")
    else:
        bot.send_message(message.chat.id, "Неверная дата")


def add_new_subject(message):  # работает
    """Вносим новое название предмета в Google-таблицу"""
    worksheet, _, df = access_current_sheet()
    user_data["subject_to_update"] = message.text
    if message.text not in df["Subject"].values:
        worksheet.append_row([message.text, "", ""])
        bot.send_message(message.chat.id, "Предмет добавлен. Теперь введите ссылку на таблицу предмета")
        bot.register_next_step_handler(message, add_new_subject_url)

    else:
        bot.send_message(message.chat.id, "Такой предмет уже существует")


def subject_updating_option(message):  # работает
    """Уточняем, что именно надо обновить - название или ссылку на таблицу"""
    user_data["subject_to_update"] = message.text
    subject_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    subject_markup.row("Название")
    subject_markup.row("Ссылку")
    bot.send_message(message.chat.id, "Что именно хотите обновить?", reply_markup=subject_markup)
    bot.register_next_step_handler(message, choose_subject_updating)


def choose_subject_updating(message):  # работает
    """Выбираем, что именно надо обновить - название или ссылку на таблицу"""
    if message.text == "Название":
        bot.send_message(message.chat.id, "Введите новое название предмета")
        bot.register_next_step_handler(message, update_subject)
    elif message.text == "Ссылку":
        bot.send_message(message.chat.id, "Введите новую ссылку на таблицу предмета")
        bot.register_next_step_handler(message, add_new_subject_url)
    else:
        bot.send_message(message.chat.id, "Команда не распознана")


def add_new_subject_url(message):  # работает
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    worksheet, _, df = access_current_sheet()
    subject = user_data["subject_to_update"]
    if subject in df["Subject"].values:
        worksheet.update_cell(df[df["Subject"] == subject].index[0] + 2, 2, message.text)
        bot.send_message(message.chat.id, "Ссылка на таблицу предмета обновлена")
    else:
        bot.send_message(message.chat.id, "Такого предмета не существует")


def update_subject(message):  # работает
    """Обновляем информацию о предмете в Google-таблице"""
    worksheet, _, df = access_current_sheet()
    subject = user_data["subject_to_update"]
    if subject in df["Subject"].values:
        worksheet.update_cell(df[df["Subject"] == subject].index[0] + 2, 1, message.text)
        bot.send_message(message.chat.id, "Название предмета обновлено")
    else:
        bot.send_message(message.chat.id, "Такого предмета не существует")


def delete_subject(message):  # работает
    """Удаляем предмет в Google-таблице"""
    worksheet, _, df = access_current_sheet()
    if message.text in df["Subject"].values:
        worksheet.delete_rows(int(df[df["Subject"] == message.text].index[0] + 2))
        bot.send_message(message.chat.id, "Предмет удален")
    else:
        bot.send_message(message.chat.id, "Такого предмета не существует")


def clear_subject_list(message):  # работает
    """Удаляем все из Google-таблицы"""
    worksheet, _, df = access_current_sheet()
    # удаляем все строки, кроме первой
    worksheet.delete_rows(2, df.shape[0] + 1)
    bot.send_message(message.chat.id, "Список предметов очищен")


@bot.message_handler(commands=["start"])
def start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    try:
        with open("tables.json") as json_file:
            _, _, df = access_current_sheet()
            # выводим список предметов
            subjects = "\n".join(df["Subject"].values.tolist())
            bot.send_message(message.chat.id, "Сохранённые предметы:\n" + subjects)
            start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            start_markup.row("Посмотреть дедлайны на этой неделе")
            start_markup.row("Редактировать дедлайн")
            start_markup.row("Редактировать предметы")
            start_markup.row("Очистить таблицу")
            info = bot.send_message(
                message.chat.id, "Что хотите сделать?", reply_markup=start_markup, parse_mode="Markdown"
            )
            bot.register_next_step_handler(info, choose_action)
    except FileNotFoundError:
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Подключить Google-таблицу")
        info = bot.send_message(
            message.chat.id, "Что хотите сделать?", reply_markup=start_markup, parse_mode="Markdown"
        )
        bot.register_next_step_handler(info, choose_action)


if __name__ == "__main__":
    bot.infinity_polling()
