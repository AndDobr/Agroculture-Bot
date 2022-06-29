from telebot import types, TeleBot
from telebot.types import *
import threading
import time
import ssl
import paho.mqtt.client as mqtt
import ast
import json

bot = TeleBot(token=token)

f = open('var.txt', 'r') #f.read()
#info = ast.literal_eval(f.read())
device1 = {'thingId': 'device1', 'type': 'telemetry', 'timeStamp': 1656401248621, 'hwVer': '1.0', 'swVer': '1.0', 'contractVer': '1.0', 'current': {'geo0': {'lat': 55.912967, 'lon': 49.285896}, 'geo1': {'lat': 55.91368522639197, 'lon': 49.284930287168024}}, 'isWatering': True, 'isWorking': True}
device2 = {"thingId": "device2", "type": "telemetry", "timeStamp": 1656401252482, "hwVer": "1.0", "swVer": "1.0", "contractVer": "1.0", "current": {"geo0": {"lat": 56.020424, "lon": 49.665864}, "geo1": {"lat": 56.01926615841914, "lon": 49.65864081931579}}, "isWatering": True, "isWorking": True}
device3 = {"thingId": "device3", "type": "telemetry", "timeStamp": 1656401249614, "hwVer": "1.0", "swVer": "1.0", "contractVer": "1.0", "current": {"geo0": {"lat": 56.01387, "lon": 49.631268}, "geo1": {"lat": 56.011921502553484, "lon": 49.626642715056256}}, "isWatering": True, "isWorking": True}
typess = ['thingId', 'type', 'timeStamp', 'hwVer', 'swVer', 'contractVer', 'current', 'isWatering', 'isWorking']
devices = ['device1', 'device2', 'device3']

keyb1 = types.ReplyKeyboardMarkup()
keyb1.add(KeyboardButton('thingId'), KeyboardButton('type'), KeyboardButton('timeStamp'))
keyb1.add(KeyboardButton('hwVer'), KeyboardButton('swVer'), KeyboardButton('contractVer'))
keyb1.add(KeyboardButton('current'), KeyboardButton('isWatering'), KeyboardButton('isWorking'))
keyb1.add(KeyboardButton('Полностью'))

keyb2 = types.ReplyKeyboardMarkup()
keyb2.add(KeyboardButton('Выбрать устройство'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, f"Здравствуйте, {message.from_user.first_name} рады Вас видеть")
    markup = types.InlineKeyboardMarkup()
    button1 = InlineKeyboardButton('device1', callback_data='device1')
    button2 = InlineKeyboardButton('device2', callback_data='device2')
    button3 = InlineKeyboardButton('device3', callback_data='device3')
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    bot.send_message(message.chat.id, 'Выберите устройство', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    for device in devices:
        if call.data == device:
            bot.send_message(call.message.chat.id, 'Выберите что хотите узнать', reply_markup=keyb1)
            bot.register_next_step_handler(call.message, save, device)

@bot.message_handler(content_types=['text'])
def process_message(message):
    if message.text == 'Выбрать устройство':
        markup = types.InlineKeyboardMarkup()
        button1 = InlineKeyboardButton('device1', callback_data='device1')
        button2 = InlineKeyboardButton('device2', callback_data='device2')
        button3 = InlineKeyboardButton('device3', callback_data='device3')
        markup.row(button1)
        markup.row(button2)
        markup.row(button3)
        bot.send_message(message.chat.id, 'Выберите устройство', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Неизвестное сообщение', reply_markup=keyb2)

def save(message, device):
    if device == 'device1':
        if message.text != 'Полностью':
            for type in typess:
                if type == 'current': #info = ast.literal_eval(f.read())
                    a = str(device1.get(type)).find("'lat': ")
                    b = str(device1.get(type)).find("},")
                    bot.send_message(message.chat.id, f"▫️{type.capitalize()} = {str(device1.get(type))[a:b]}")
                    break
                elif message.text == type:
                    bot.send_message(message.chat.id, f"▫️{type.capitalize()} = {device1.get(type)}", reply_markup=keyb2)
                    break
        if message.text == 'Полностью':
            list = []
            for type in typess:
                if type == 'current':
                    a = str(device1.get(type)).find("'lat': ")
                    b = str(device1.get(type)).find("},")
                    list.append(f'▫️{type.capitalize()} = {str(device1.get(type))[a:b]}')
                else:
                    list.append(f'▫️{type.capitalize()} = {device1.get(type)}')
            bot.send_message(message.chat.id, '\n'.join(list))
    elif device == 'device2':
        if message.text != 'Полностью':
            for type in typess:
                if type == 'current':
                    a = str(device1.get(type)).find("'lat': ")
                    b = str(device1.get(type)).find("},")
                    bot.send_message(message.chat.id, f'▫️{type.capitalize()} = {str(device2.get(type))[a:b]}')
                    break
                elif message.text == type:
                    bot.send_message(message.chat.id, f'▫️{type.capitalize()} = {device2.get(type)}', reply_markup=keyb2)
                    break
        if message.text == 'Полностью':
            list = []
            for type in typess:
                if type == 'current':
                    a = str(device2.get(type)).find("'lat': ")
                    b = str(device2.get(type)).find("},")
                    list.append(f'▫️{type.capitalize()} = {str(device2.get(type))[a:b]}')
                else:
                    list.append(f'▫️{type.capitalize()} = {device2.get(type)}')
            bot.send_message(message.chat.id, '\n'.join(list))
    elif device == 'device3':
        if message.text != 'Полностью':
            for type in typess:
                if type == 'current':
                    a = str(device3.get(type)).find("'lat': ")
                    b = str(device3.get(type)).find("},")
                    bot.send_message(message.chat.id, f'▫️{type.capitalize()} = {str(device3.get(type))[a:b]}')
                    break
                elif message.text == type:
                    bot.send_message(message.chat.id, f'▫️{type.capitalize()} = {device3.get(type)}', reply_markup=keyb2)
                    break
        if message.text == 'Полностью':
            list = []
            for type in typess:
                if type == 'current':
                    a = str(device3.get(type)).find("'lat': ")
                    b = str(device3.get(type)).find("},")
                    list.append(f'▫️{type.capitalize()} = {str(device3.get(type))[a:b]}')
                else:
                    list.append(f'▫️{type.capitalize()} = {device3.get(type)}')
            bot.send_message(message.chat.id, '\n'.join(list))
def updater():
    while True:
        try:
            file2 = open("var.txt", "w+")
            file2.write('')
            def on_subscribe(client, userdata, mid, granted_qos):
                print("Subscribed", client, userdata, mid, granted_qos)
            def on_connect(client, userdata, flags, rc):
                if rc == 0:
                    print("Connected to broker")
                    global Connected
                    Connected = True
                else:
                    print("Connection failed")

            def on_message(client, userdata, message):
                file2 = open("var.txt", "w+")
                file2.write('')
                print(f"Message received: {message.payload}")
                jsonString = message.payload
                dict_str = jsonString.decode("UTF-8")
                # global jsonData
                jsonData = ast.literal_eval(dict_str)
                file1 = open("var.txt", "a")
                file1.write(dict_str)

                if jsonData.get("thingId") == "device1":
                    device1 = dict(jsonData)
                if jsonData.get("thingId") == "device2":
                    device2 = dict(jsonData)
                if jsonData.get("thingId") == "device3":
                    device3 = dict(jsonData)

            broker_address = "mqtt.cloud.yandex.net"
            port = 8883
            user = "aresmv64htqk8lkmqr61"
            password = "ICLinnocamp2022"
            client = mqtt.Client("kazanka")
            client.username_pw_set(user, password=password)
            client.on_connect = on_connect
            client.on_message = on_message
            client.on_subscribe = on_subscribe
            client.tls_set(r"rootCA.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
            client.tls_insecure_set(True)
            client.connect(broker_address, port=port)
            traps = ["$devices/are9gnqohp4npug37mbs/events/raw", "$devices/are1suqff6jhlala2bsh/events/raw",
                     "$devices/areg5dfne7179n4o24q2/events/raw"]

            for trap in traps:
                client.subscribe(trap)

            client.loop_forever()


        except Exception as e:
            print("error", e)
        time.sleep(5)


t = threading.Thread(target=updater)
t.start()

bot.infinity_polling()
