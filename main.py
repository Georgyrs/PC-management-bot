import os
import telebot
import tempfile
from PIL import ImageGrab
import platform
import psutil
import subprocess
import GPUtil
import requests
from bs4 import BeautifulSoup
import wikipedia
from tabulate import tabulate
import random
import time
import sys
import pyAesCrypt
import pyautogui as pg
import threading
import pyaudio
reklama = True
path = 'C:/Users/xxxx'
computer_names = ['Тебя гриферят, троллят? Купи полный доступ к регионам и накажи всех ненавистников!', 'Поздравляем, вы выиграли опку! Чтобы забрать, купи донат на сайте skybars.net',  'хочешь чтобы твоя мама жила вечно? Купи донат!']
downloadpath = r"C:\Users\xxxx\Downloads"
API_TOKEN = ''
WHITELIST_USERS = ['']
bot = telebot.TeleBot(API_TOKEN)
wikipedia.set_lang('ru')
CITY_NAME = ''
url = "https://rp5.ru/Погода_в_Белграде"
url1 = "https://www.accuweather.com/ru/rs/belgrade/298198/hourly-weather-forecast/298198"
urlvalue = "https://www.banki.ru/products/currency/cb/"
response = requests.get(url)
response1 = requests.get(url1)
responseval = requests.get(urlvalue)
soup = BeautifulSoup(response.text, "html.parser")
soupvak = BeautifulSoup(responseval.text, "html.parser")
soupel = soupvak.find("table", {"class": "standard-table standard-table--row-highlight"})
temperature_element = soup.find("span", {"class": "t_0"})
temperature = temperature_element.text.strip() if temperature_element else "N/A"
valuetable = []
is_media_paused = False


table_headers = [ "Валюта", "Курс"]
formatted_valuetable = tabulate(valuetable, headers=table_headers, tablefmt="plain", floatfmt=".0f")

print(formatted_valuetable)
print(valuetable)
a = "https://rusmeteo.net/weather/loznica-84182/14days/"
so = requests.get(a).text
s = BeautifulSoup(so, 'html.parser')

current_weather = None
for r in s.find_all('div', class_="forecast-14-day"):
    current_weather = r.find('td', class_="precip-line").text.strip()

def get_computer_name():
    return os.environ['COMPUTERNAME'] if os.name == 'nt' else os.uname().nodename

main_menu_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
main_menu_markup.add(
    telebot.types.InlineKeyboardButton(text="Мой компьютер", callback_data="my_computer"),
    telebot.types.InlineKeyboardButton(text="Другое", callback_data="other"),
    telebot.types.InlineKeyboardButton(text="Диспетчер задач", callback_data="taskmanager"),
    telebot.types.InlineKeyboardButton(text="Медиа", callback_data="media")
)

my_computer_markup = telebot.types.InlineKeyboardMarkup(row_width=1)
my_computer_markup.add(
    telebot.types.InlineKeyboardButton(text="Выключить📴", callback_data="shutdown"),
    telebot.types.InlineKeyboardButton(text="Перезагрузить🔄️", callback_data="reboot"),
    telebot.types.InlineKeyboardButton(text="Получить скриншот📨", callback_data="screenshot"),
    telebot.types.InlineKeyboardButton(text="Список файлов📃", callback_data="list_files"),
    telebot.types.InlineKeyboardButton(text="Информация о системеℹ️", callback_data="system_info")
)

other_markup = telebot.types.InlineKeyboardMarkup()
other_markup.add(
    telebot.types.InlineKeyboardButton(text="Курсы валют💱", callback_data="currency_rates"),
    telebot.types.InlineKeyboardButton(text="Wikipedia", callback_data="wiki"),
    telebot.types.InlineKeyboardButton(text="Загрузить файл на ПК🖥️", callback_data="getfile")
)
taskmanager_markup = telebot.types.InlineKeyboardMarkup()
taskmanager_markup.add(
    telebot.types.InlineKeyboardButton(text="Завершить процесс❌", callback_data="kill_process"),
    telebot.types.InlineKeyboardButton(text="Список процессов🪟", callback_data="list_processes"),
    telebot.types.InlineKeyboardButton(text="Запустить процесс✅", callback_data="run_process")
)
media_markup = telebot.types.InlineKeyboardMarkup()
media_markup.add(
    telebot.types.InlineKeyboardButton(text="Пауза", callback_data="pause1"),
    telebot.types.InlineKeyboardButton(text="Прибавить звук", callback_data="volumeup1"),
    telebot.types.InlineKeyboardButton(text="Убавить звук", callback_data="volumedown1"),
    telebot.types.InlineKeyboardButton(text="Выключить звук", callback_data="volumeoff1"),
    telebot.types.InlineKeyboardButton(text="Звук с микрофона", callback_data="microlisten")
)
@bot.callback_query_handler(func=lambda call: call.data == "my_computer")
def show_my_computer_menu(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Мой компьютер", reply_markup=my_computer_markup)

@bot.callback_query_handler(func=lambda call: call.data == "other")
def show_other_menu(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Другое", reply_markup=other_markup)
@bot.callback_query_handler(func=lambda call: call.data == "taskmanager")
def show_taskmanager_menu(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Диспетчер задач", reply_markup=taskmanager_markup)
@bot.callback_query_handler(func=lambda call: call.data == "media")
def show_taskmanager_menu(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Управление медиа", reply_markup=media_markup)
@bot.callback_query_handler(func=lambda call: call.data == "currency_rates")
def fetch_currency_rates(call):
    message = "<b>Курсы валют:</b>\n"
    for row in valuetable:
        currency = row[0]
        rate = float(row[1])
        message += f"<b>[💴]:</b> {currency}, <b>₽:</b> {rate:.2f}\n"
    bot.send_message(call.message.chat.id, message, parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "getfile")
def getfile(call):
    global waiting_for_pid, waiting_for_wiki, waiting_for_run, waiting_for_download
    waiting_for_pid = False
    waiting_for_wiki = False
    waiting_for_run = False
    waiting_for_download = True
    print("Waiting for file upload...")
    bot.send_message(call.message.chat.id, "Загрузите сюда ваш файл:")
@bot.callback_query_handler(func=lambda call: call.data == "pause1")
def pause(call):
    bot.send_message(call.message.chat.id, "Медиа на паузе!")
    pg.press('playpause')
@bot.callback_query_handler(func=lambda call: call.data == "volumeup1")
def volumeup(call):
    bot.send_message(call.message.chat.id, "Звук прибавлен!")
    pg.press('volumeup')

@bot.callback_query_handler(func=lambda call: call.data == "volumedown1")
def volumedown(call):
    bot.send_message(call.message.chat.id, "Звук убавлен!")
    pg.press('volumedown')
@bot.callback_query_handler(func=lambda call: call.data == "volumeoff1")
def volumeoff(call):
    bot.send_message(call.message.chat.id, "Звук выключен!")
    pg.press('volumemute')

confirm_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
confirm_markup.add(
    telebot.types.InlineKeyboardButton(text="Да", callback_data="confirm_screenshot"),
    telebot.types.InlineKeyboardButton(text="Нет", callback_data="cancel_screenshot")
)
@bot.callback_query_handler(func=lambda call: call.data == "run_process")
def run_process(call):
    global waiting_for_pid, waiting_for_wiki, waiting_for_run
    waiting_for_pid = False
    waiting_for_wiki = False  # Reset the flag for Wikipedia search
    waiting_for_run = True
    bot.send_message(call.message.chat.id, "Введите полный путь к исполняемому файлу:")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    loading_message = bot.send_message(message.chat.id, "⏳")
    if str(message.from_user.id) in WHITELIST_USERS:
        bot.delete_message(message.chat.id, loading_message.message_id)
        welcome_message = f'Приветствую!\n\nВы подключены к компьютеру: {get_computer_name()}.\n\n'
        weather_info = f'Текущая погода в {CITY_NAME}:\n\nТемпература: *{temperature}*\nСостояние: *{current_weather}*\n\n'
        challenge = random.choice(computer_names)
        bot.send_message(message.chat.id, welcome_message + weather_info + str(challenge), parse_mode="Markdown", reply_markup=main_menu_markup)
    else:
        bot.send_message(message.chat.id, "Вы не авторизованы для использования этого бота.")

@bot.callback_query_handler(func=lambda call: call.data == "screenshot")
def send_screenshot_confirmation(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    msg = bot.send_message(call.message.chat.id, "Вы уверены, что хотите получить скриншот?", reply_markup=confirm_markup)

wiki_search_in_progress = False

waiting_for_pid = False
waiting_for_wiki = False
waiting_for_run = False
waiting_for_download = False
@bot.callback_query_handler(func=lambda call: call.data == "kill_process")
def kill_process(call):
    global waiting_for_pid, waiting_for_wiki, waiting_for_download
    waiting_for_pid = True
    waiting_for_wiki = False
    waiting_for_download = False
    bot.send_message(call.message.chat.id, "Введите PID процесса, который хотите завершить:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global waiting_for_pid, waiting_for_wiki, waiting_for_run, path, waiting_for_download
    if waiting_for_pid:
        if message.text.isdigit():
            pid = int(message.text)
            try:
                subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
                bot.send_message(message.chat.id, f'Процесс с PID {pid} успешно завершен.')
            except subprocess.CalledProcessError:
                bot.send_message(message.chat.id, f'Процесс с PID {pid} не найден или не может быть завершен.')
            except Exception as e:
                bot.send_message(message.chat.id, f'Ошибка при завершении процесса: {e}')
        else:
            bot.send_message(message.chat.id, 'Введите корректный PID процесса (целое число).')
        waiting_for_pid = False
    elif waiting_for_wiki:
        wiki_search(message)
    elif waiting_for_run:
        try:
            process_path = message.text.strip()
            if os.path.isfile(process_path):
                os.startfile(process_path)
                bot.send_message(message.chat.id, f'Процесс {os.path.basename(process_path)} запущен успешно!')
            else:
                bot.send_message(message.chat.id, 'Указанный файл не существует!')
        except Exception as e:
            bot.send_message(message.chat.id, f'Ошибка при запуске процесса: {e}')
        waiting_for_run = False
    elif waiting_for_download:
         fileget = bot.get_file(message.document.file_id)
         zagruZka = bot.download_file(fileget.file_path)
         pathget = os.path.join(f'{path}', message.document.file_name)
         with open(pathget, 'wb') as filepc:
              filepc.write(zagruZka)
         bot.send_message(message.chat.id, 'Файл успешно загружен!')
         print('hi')
         waiting_for_download = False
    else:
        print("Ожидание PID terminate")

def wiki_search(message):
    global waiting_for_wiki
    word = message.text.strip().lower()
    try:
        finalmess = wikipedia.summary(word)
        bot.send_message(message.chat.id, finalmess, parse_mode='html')
    except wikipedia.exceptions.PageError:
        bot.send_message(message.chat.id, "Такой страницы не существует!")
    finally:
        waiting_for_wiki = False

@bot.callback_query_handler(func=lambda call: call.data == "wiki")
def ask_for_wikipedia_query(call):
    global waiting_for_wiki
    waiting_for_wiki = True
    waiting_for_pid = False
    waiting_for_run = False# Reset the flag for process termination
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, "Введите ваш запрос для поиска на Wikipedia:")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_screenshot")
def send_screenshot(call):
    loadingmsg = bot.send_message(call.message.chat.id, "⏳")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    path = tempfile.gettempdir() + 'screenshot.png'
    screenshot = ImageGrab.grab()
    screenshot.save(path, 'PNG')
    bot.send_photo(call.message.chat.id, open(path, 'rb'))
    bot.send_message(call.message.chat.id, "Скриншот отправлен.", reply_markup=my_computer_markup)
    bot.delete_message(call.message.chat.id, loadingmsg.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "shutdown")
def shutdown_system(call):
    loadingmsg = bot.send_message(call.message.chat.id, "⏳")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Выключаю...')
    os.system("shutdown -s -t 0")
    bot.delete_message(call.message.chat.id, loadingmsg.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "reboot")
def reboot_system(call):
    loadingmsg = bot.send_message(call.message.chat.id, "⏳")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Перезагрузка...')
    if platform.system() == 'Windows':
        os.system('shutdown /r /t 1')
    elif platform.system() == 'Linux':
        os.system('reboot now')
    bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=my_computer_markup)

@bot.callback_query_handler(func=lambda call: call.data == "list_files")
def request_directory(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, 'Введите путь к директории:')
    bot.register_next_step_handler(call.message, list_files)

def list_files(message):
    directory_path = message.text.strip()
    files = os.listdir(directory_path)
    files_list = "\n".join(files)
    bot.send_message(message.chat.id, f'Файлы в директории {directory_path}:\n{files_list}')
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=my_computer_markup)

@bot.callback_query_handler(func=lambda call: call.data == "system_info")
def system_info(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    system_info_str = f'ОС: {platform.system()} {platform.release()}\n'
    system_info_str += f'Процессор: {platform.processor()}\n'
    system_info_str += f'Количество ядер процессора: {psutil.cpu_count(logical=False)}\n'

    svmem = psutil.virtual_memory()
    system_info_str += f'Общий объем памяти: {svmem.total / (1024 ** 3):.2f} GB\n'
    system_info_str += f'Использовано памяти: {svmem.used / (1024 ** 3):.2f} GB\n'
    system_info_str += f'Свободно памяти: {svmem.available / (1024 ** 3):.2f} GB\n'

    gpus = GPUtil.getGPUs()
    for i, gpu in enumerate(gpus):
        system_info_str += f'GPU {i+1}:\n'
        system_info_str += f'    Название: {gpu.name}\n'
        system_info_str += f'    Загрузка: {gpu.load * 100:.2f}%\n'
        system_info_str += f'    Память: {gpu.memoryTotal:.0f}MB / {gpu.memoryUsed:.0f}MB\n'

    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        system_info_str += f'Диск {partition.device}:\n'
        system_info_str += f'    Использовано: {partition_usage.used / (1024 ** 3):.2f} GB\n'
        system_info_str += f'    Свободно: {partition_usage.free / (1024 ** 3):.2f} GB\n'

    bot.send_message(call.message.chat.id, system_info_str)
    bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=my_computer_markup)

@bot.callback_query_handler(func=lambda call: call.data == "list_processes")
def list_processes(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append((proc.info['pid'], proc.info['name']))

    processes_list = "\n".join([f"🔄 PID: {pid}\n    🔧 Name: {name}" for pid, name in processes])

    chunk_size = 4096
    for chunk in [processes_list[i:i + chunk_size] for i in range(0, len(processes_list), chunk_size)]:
        bot.send_message(call.message.chat.id, chunk)
    bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=taskmanager_markup)



bot.polling()
