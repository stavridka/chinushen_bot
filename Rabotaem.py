#!/bin/python3
# - *- coding: utf- 8 - *-
import config
import telebot
import sqlite3
import random
from telebot import types


bot = telebot.TeleBot(config.token)

with sqlite3.connect('memories.db') as db:
    cursor = db.cursor()
    query = ("""CREATE TABLE IF NOT EXISTS data(id INTEGER, username TEXT) """)
    cursor.execute(query)

with sqlite3.connect('memories.db') as db:
    cursor = db.cursor()
    query = """CREATE TABLE IF NOT EXISTS swimes(id INTEGER, num INTEGER, popit INTEGER, wins INTEGER, status INTEGER) """
    cursor.execute(query)




@bot.message_handler(commands = ['start'])
def reg_user(message):
    with sqlite3.connect('memories.db') as db:
        cursor = db.cursor()
        u_id = message.chat.id
        u_name = message.chat.username
        info = cursor.execute('SELECT * FROM data WHERE id = ?', [message.chat.id])
        if info.fetchone() is None: 
            
            cursor.execute('''INSERT INTO data VALUES (?,?);''', (u_id, u_name))
            db.commit()                
            
    with sqlite3.connect('memories.db') as db:
        cursor = db.cursor()
        u_id = message.chat.id
        u_num = 0
        u_popit = 0
        u_wins = 0
        statu = 0
        info = cursor.execute('SELECT * FROM swimes WHERE id=?', [message.chat.id ])
        if info.fetchone() is None:         
                
            cursor.execute('''INSERT INTO swimes VALUES (?,?,?,?,?);''', (u_id, u_num, u_popit,u_wins,statu ))
            db.commit()        
    return menu(message)  
@bot.message_handler(commands =['lobby⛩'])
def menu(message):
    
    with sqlite3.connect('memories.db') as db:
        cursor = db.cursor()        
        cursor.execute(f'UPDATE swimes SET popit = { 0 } WHERE id = "{message.chat.id}" ')    
        db.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)

    b_play = types.KeyboardButton(text = '/play📱')
    b_stats = types.KeyboardButton(text = '/stats📊')
    b_h_play = types.KeyboardButton(text = '/info📝')

    
    markup.add(b_play,b_stats,b_h_play)
    info = cursor.execute('SELECT coins FROM swimes WHERE id=?', [message.chat.id ]). fetchone()[0]
    bot.send_message(message.chat.id, '👋🏻Рад видеть, {0.first_name}!\n'.format(message.from_user) +f'В твоем мешочке {info}🪬 монет', reply_markup = markup)


@bot.message_handler(commands = ['play📱'])
def game (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    b_play = types.KeyboardButton(text = '/lobby⛩')
    
    markup.add(b_play)    
    numb = int(str(random.randint(1,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)))
        
    if numb % 10 == numb // 1000 or numb % 10 == numb % 1000 // 100 or numb % 10 == numb % 100 // 10 or numb % 100 // 10 == numb // 1000 or numb % 100 // 10 == numb % 1000 // 100 or numb // 1000 == numb % 1000 // 100:
                
        return game(message)    
    else:
        with sqlite3.connect('memories.db') as db:
            cursor = db.cursor()        
            cursor.execute(f'UPDATE swimes SET num = { numb } WHERE id = "{message.chat.id}" ')
        bot.send_message(message.chat.id, '🪐Я загадал число! Попробуй отгадать его!'.format(message.from_user), reply_markup = markup)    
            
           
        bot.register_next_step_handler(message,vivod)        

@bot.message_handler(commands = ['lobby⛩']) 
def ret(message):
    return menu(message)

@bot.message_handler(commands = ['stats📊']) 
def stats (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    b_play = types.KeyboardButton(text = '/lobby⛩')
    
    markup.add(b_play)    
    
    with sqlite3.connect('memories.db') as db:
        cursor = db.cursor()       
        win = cursor.execute("SELECT wins FROM swimes WHERE id = ?", [message.chat.id]) . fetchone()[0]
   
    bot.send_message(message.chat.id, '🎖Ты отгадал ' + str(win) + ' чисел!'.format(message.from_user), reply_markup = markup)

    with sqlite3.connect('memories.db') as db:
        cursor = db.cursor()
        tops = cursor.execute("SELECT d.id, d.username, s.wins FROM swimes as s left join data as d on s.id = d.id where d.username is not null order by s.wins desc, s.id asc Limit 10") . fetchall()
        messageTops = "Лучшие игроки: Топ-10\r\n";
        for element in tops:
            messageTops = messageTops + "Никнеим: "+element[1]+" - "+str(element[2])+" побед!\r\n";

        bot.send_message(message.chat.id, messageTops,
                             reply_markup=markup)


@bot.message_handler(commands = ['lobby⛩']) 
def ret(message):
    return menu(message)


@bot.message_handler(commands = ['info📝']) 
def info (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    b_play = types.KeyboardButton(text = '/lobby⛩')
    
    markup.add(b_play)    
    bot.send_message(message.chat.id, 'Бот загадывает 4х значное число(цифры без повтора и не начинается с 0. Необходимо угадать его, используя подсказки - "бык", "корова" ' .format(message.from_user), reply_markup = markup)
    bot.send_message(message.chat.id, 'Бык означает, что в загаданном числе есть цифра из введённого Вами числа и она стоит на своём месте')
    bot.send_message(message.chat.id, 'Корова - в загаданном числе есть цифра из введённого Вами числа, но она не на своём месте')
    bot.send_message(message.chat.id,'Пример: 1234 - загадано, Вы ввели 1902. Это 1 бык и 1 корова, т.к 1 стоит на своём месте, а 2 не на своём, но она есть в загаданном числе')    

    

def vivod(message):
    if message.text == '/lobby⛩':
        return menu(message)
    try:
        vvod = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, '🔮Гадаю, что тут что-то не так! Попробуй ввести число!')
        bot.register_next_step_handler(message,vivod)
    except TypeError:
        bot.send_message(message.chat.id, '🔮Гадаю, что тут что-то не так! Попробуй ввести число!')
        bot.register_next_step_handler(message,vivod)        
    
    else:
        if len(str(vvod)) != 4:
            bot.send_message(message.chat.id,'🍕Вводи 4х разрядное число!') 
            bot.register_next_step_handler(message, vivod)          
            
        else:
            with sqlite3.connect('memories.db') as db:
                cursor = db.cursor()    
                num = int(cursor.execute("SELECT num FROM swimes WHERE id = ?", [message.chat.id]) . fetchone()[0]) 
    
   
        
            cow = 0
            bull = 0
   
            
    
            if (vvod % 10 == num % 10):    
                bull += 1
            if (vvod // 1000 == num // 1000):    
                bull += 1
            if (vvod % 1000 // 100) == (num % 1000 // 100 ):
                bull += 1
            if (vvod % 100 // 10) == (num % 100 // 10):
                bull += 1
            
            
            if vvod % 10 == num // 1000:
                cow += 1
            if vvod % 10 == num % 1000 // 100:
                cow += 1
            if vvod % 10 == num % 100 // 10:
                cow += 1
            
            if vvod //1000  == num % 10:
                cow += 1
            if vvod //1000 == num % 1000 // 100:
                cow += 1
            if vvod //1000 == num % 100 // 10:  
                cow += 1
            
            if vvod % 1000 // 100  == num % 10:
                cow += 1
            if vvod % 1000 // 100  == num  // 1000 :
                cow += 1
            if vvod % 1000 // 100  == num % 100 // 10:   
                cow += 1
                
            if vvod % 100 // 10  == num % 10:
                cow += 1
            if vvod % 100 // 10  == num  // 1000 :
                cow += 1
            if vvod % 100 // 10  == num % 1000 // 100:   
                cow += 1    
            if num == vvod:
                with sqlite3.connect('memories.db') as db:
                    cursor = db.cursor()
                    cursor.execute(f'UPDATE swimes SET wins = wins + 1 WHERE id = "{message.chat.id}" ')
                    db.commit()                        
                    pop = cursor.execute("SELECT popit FROM swimes WHERE id = ?", [message.chat.id]) . fetchone()[0] 
                
                 
                       
                    coin = 12 - int(pop)
                    cursor.execute(f'UPDATE swimes SET coins = coins + {coin} WHERE id = "{message.chat.id}" ')
                    db.commit()                
                    bot.send_message(message.chat.id , '🎆Мои поздравления! Ты угадал число за ' + str(pop + 1) + ' попыток !')
                    
                    bot.send_message(message.chat.id, f'Ты сгреб в мешочек {12 - int(pop) }🪬 монет...')
                return menu(message)        
            if num != vvod:
            
                with sqlite3.connect('memories.db') as db:
                    cursor = db.cursor()
                    cursor.execute(f'UPDATE swimes SET popit = popit + 1 WHERE id = "{message.chat.id}" ')
                    db.commit()
                    pop = cursor.execute("SELECT popit FROM swimes WHERE id = ?", [message.chat.id]) . fetchone()[0] 
                    if pop == 12:
                        bot.send_message(message.chat.id, 'Оп,попытки закончились,ты продул -_-')
                        return menu(message)
            
                bot.send_message(message.chat.id, f'{str(bull)} бык(а) и {str(cow)} коров(а)' )       
                bot.register_next_step_handler(message, vivod)          



bot.polling(none_stop=True)
