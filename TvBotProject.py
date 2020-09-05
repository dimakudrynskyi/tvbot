import telebot 
import schedule
import requests
from telebot import types
import urllib
import random
from sqlighter import SQLighter
import sqlite3
from datetime import date
from datetime import datetime
import time
import threading
import os
import re



API_TOKEN = os.environ["API_TOKEN"]
bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler(commands = ["start"])
def start(message):
    sti = open('welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    mess = f"<b>Hi {message.from_user.first_name} {message.from_user.last_name}</b>!\nWelcome to tvBot !\nIf you want to know all my functions write a command /help"
    bot.send_message(message.chat.id, mess, parse_mode="html")
    db = SQLighter("SQLite.db")
    if(not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
    else:
        db.update_subscription(message.from_user.id, False)

    user_name = message.from_user.first_name + message.from_user.last_name
    text = f"New user in bot -  {user_name}" + "\n" + f"User ID - {message.from_user.id}"
    bot.send_message(874341820, text)



@bot.message_handler(commands = ["help"])
def sthelpart(message):
    mess = f"<b>Hi i am a tvBot!😀</b>\nBelow is a list of all my commands👇\n●1 - /help - List of comands\n●2 - /film_and_series - Top and random\n●3 - /subscribe - Subscribed to our tvBot\n●4 - /unsubscribe - Unsubscribed from our tvBot\n●5 - /upcoming - Watch upcomung flm\n●6 - /wish_list - Movies your liked"

    bot.send_message(message.chat.id, mess, parse_mode="html")


@bot.message_handler(commands = ["wish_list"])
def wish_list(message):
    user_id = message.from_user.id
    conn = sqlite3.connect("Wish_list.db")
    c = conn.cursor()  
    c.execute("SELECT wish_list FROM Wish_list WHERE user_id=?", (user_id,))  
    rows = c.fetchall()
    for row in rows:
        new_row =  ''.join(row)
        markup_inline = types.InlineKeyboardMarkup()
        button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online" )
        button_wish_list = types.InlineKeyboardButton(text="❌Remove from wish list❌", callback_data="remove_wish_list")
        button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")
        markup_inline.add(button_link, button_wish_list, button_remind)
        bot.send_message(message.chat.id, new_row, parse_mode="html", reply_markup=markup_inline)



@bot.message_handler(commands = ["subscribe"])
def subscribe(message):
    db = SQLighter("SQLite.db")
    if(not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, True)

    mess = f"<b>{message.from_user.first_name} {message.from_user.last_name}</b>!\n👍You have successfully subscribed to our tvBot\n<b>Welcome🖐🏼</b>"
    bot.send_message(message.chat.id, mess, parse_mode="html")


@bot.message_handler(commands = ["unsubscribe"])
def unsubscribe(message):
    db = SQLighter("SQLite.db")
    if(not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
    else:
        db.update_subscription(message.from_user.id, False)

    mess = f"{message.from_user.first_name} {message.from_user.last_name}!\n😥You have successfully unsubscribed from our tvBot😥"
    bot.send_message(message.chat.id, mess, parse_mode="html")



@bot.message_handler(commands = ["upcoming_film"])
def upcoming(message):
    today = datetime.today() 
    api_key = "124a9a01380f47d7fb0dc07e6d25ec26"
    url =  f"https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=en-US&page=1"
    response = requests.get(url, headers={'Accept' : 'application/json'})
    data = response.json()
    
    try:
        i = 0
        while i < len(data["results"]):
            release_date = data["results"][i]["release_date"]
            title = data["results"][i]["title"]
            image = data["results"][i]["poster_path"]
            full_image = f"https://image.tmdb.org/t/p/original{image}"
            overview = data["results"][i]["overview"]
            datetime_object = datetime.strptime(release_date, "%Y-%m-%d")

            if datetime_object >= today:
                user_id = message.from_user.id

                text_dict = {"title": "● Title" + " - " + title,
                            "release_date": "❕ Release date" + " - " + str(release_date),
                            "overview": "📖 Overview" + " - " + overview 
                            }

                text = text_dict["title"] + "\n" + "\n" + text_dict["release_date"] + "\n" + "\n" +text_dict["overview"]


                conn = sqlite3.connect("Wish_list.db")
                c = conn.cursor()  
                c.execute("SELECT wish_list FROM Wish_list WHERE user_id=?", (user_id,))  
                rows = c.fetchall()
                markup_inline = types.InlineKeyboardMarkup() 
                try:   
                    for row in rows:
                        new_row =  ''.join(row)
                        if new_row == text:
                            text1 = "❌Remove from wish list❌" 
                            text2 = "remove_wish_list"
                            
                        else:
                            text1 = "✅Add to wish list✅" 
                            text2 = "add_to_wish_list"

                                    
                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online" )
                    button_wish_list = types.InlineKeyboardButton(text=text1, callback_data=text2)
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")
                except UnboundLocalError:
                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
                    button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")

                markup_inline.add(button_link, button_wish_list, button_remind) 
                
                f = open('upcoming.jpg','wb')
                f.write(urllib.request.urlopen(full_image).read())
                f.close()

                img = open('upcoming.jpg', 'rb')
                bot.send_photo(message.chat.id, img, text, reply_markup=markup_inline)
                img.close()
            i += 1
    except KeyError:
        pass  




@bot.message_handler(commands = ["film_and_series"])
def film_and_series(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🔝Top")
    btn2 = types.KeyboardButton("🎲Random")
    btn3 = types.KeyboardButton("/wish_list")
    markup.add(btn1, btn2, btn3)
    mess = "Choose from the list below what you want to know 👇"
    bot.send_message(message.chat.id, mess, parse_mode="html", reply_markup=markup)



@bot.message_handler(content_types=["text"]) 
def check_mess(message):
    get_mess_bot = message.text
    type_mess = type(get_mess_bot)
    if get_mess_bot == "🔝Top":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("Movie")
        btn2 = types.KeyboardButton("Series")
        btn3 = types.KeyboardButton("Сome back to the beginning🔙")
        markup.add(btn1, btn2, btn3)
        final_mess = "Do you want to know the top SERIES or MOVIES ?"
        bot.send_message(message.chat.id, final_mess, parse_mode="html", reply_markup=markup)

    elif get_mess_bot == "🎲Random":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("🎲Random film")
        btn2 = types.KeyboardButton("🎲Random series")
        btn3 = types.KeyboardButton("Сome back to the beginning🔙")
        markup.add(btn1, btn2, btn3)
        final_mess = "Do you want to watch a random movie or TV series?"
        bot.send_message(message.chat.id, final_mess, parse_mode="html", reply_markup=markup)


    
    elif get_mess_bot == "Movie":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("Day top for movie")
        btn2 = types.KeyboardButton("Week top for movie")
        btn3 = types.KeyboardButton("Сome back to the beginning🔙")
        markup.add(btn1, btn2, btn3)
        final_mess = "Do you want to see the top movies of the last DAY or the WEEK??"
        bot.send_message(message.chat.id, final_mess, parse_mode="html", reply_markup=markup)

    elif get_mess_bot == "Series":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("Day top for series")
        btn2 = types.KeyboardButton("Week top for series")
        btn3 = types.KeyboardButton("Сome back to the beginning🔙")
        markup.add(btn1, btn2, btn3)
        final_mess = "Do you want to see the top movies of the last DAY or the WEEK??"
        bot.send_message(message.chat.id, final_mess, parse_mode="html", reply_markup=markup)

    elif get_mess_bot == "🎲Random film":
    
    
        def send_random_film():
            random_numder = random.randint(125,99999)
            movie_id = str(random_numder)
            api_key = "124a9a01380f47d7fb0dc07e6d25ec26"
            url =  f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
            response = requests.get(url, headers={'Accept' : 'application/json'})
            data = response.json()

            try:
                title = data["original_title"]
                image = data["poster_path"]
                full_image = f"https://image.tmdb.org/t/p/original{image}"
                overview = data["overview"]
                vote_average = data["vote_average"]
                user_id = message.from_user.id

                text_dict = {"title": "● Title" + " - " + title,
                            "vote_average": "⭐️ Vote average" + " - " + str(vote_average),
                            "overview": "📖 Overview" + " - " + overview 
                            }
                text = text_dict["title"] + "\n" + "\n" + text_dict["vote_average"] + "\n" + "\n" +text_dict["overview"]

                try:
                    conn = sqlite3.connect("Wish_list.db")
                    c = conn.cursor()  
                    c.execute("SELECT wish_list FROM Wish_list WHERE user_id=?", (user_id,))  
                    rows = c.fetchall()
                    markup_inline = types.InlineKeyboardMarkup() 
                    user_id = message.from_user.id

                    for row in rows:
                        new_row =  ''.join(row)
                        if new_row == text:
                            text1 = "❌Remove from wish list❌" 
                            text2 = "remove_wish_list"
                            
                        else:
                            text1 = "✅Add to wish list✅" 
                            text2 = "add_to_wish_list"
                                    
                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
                    button_wish_list = types.InlineKeyboardButton(text=text1, callback_data=text2)
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")
   
                except UnboundLocalError:
                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
                    button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")

                markup_inline.add(button_link, button_wish_list, button_remind) 

                f = open('random_film.jpg','wb')
                f.write(urllib.request.urlopen(full_image).read())
                f.close()

                img = open('random_film.jpg', 'rb')
                bot.send_photo(message.chat.id, img, text, reply_markup=markup_inline)
                img.close() 

            except KeyError:
                send_random_film() 

            except urllib.error.HTTPError:
                send_random_film() 

        send_random_film()    
        

    elif get_mess_bot == "🎲Random series":

        def send_random_series():
            random_numder = random.randint(125,99999)
            series_id = str(random_numder)
            api_key = "124a9a01380f47d7fb0dc07e6d25ec26"
            url =  f"https://api.themoviedb.org/3/movie/{series_id}?api_key={api_key}&language=en-US"
            response = requests.get(url, headers={'Accept' : 'application/json'})
            data = response.json()

            try:
                title = data["original_title"]
                image = data["poster_path"]
                full_image = f"https://image.tmdb.org/t/p/original{image}"
                overview = data["overview"]
                vote_average = data["vote_average"]
                user_id = message.from_user.id
                
                text_dict = {"title": "● Title" + " - " + title,
                            "vote_average": "⭐️ Vote average" + " - " + str(vote_average),
                            "overview": "📖 Overview" + " - " + overview 
                            }

                text = text_dict["title"] + "\n" + "\n" + text_dict["vote_average"] + "\n" + "\n" +text_dict["overview"]
                try:
                    conn = sqlite3.connect("Wish_list.db")
                    c = conn.cursor()  
                    c.execute("SELECT wish_list FROM Wish_list WHERE user_id=?", (user_id,))  
                    rows = c.fetchall()
                    markup_inline = types.InlineKeyboardMarkup() 
                    
                    for row in rows:
                        new_row =  ''.join(row)
                        if new_row == text:
                            text1 = "❌Remove from wish list❌" 
                            text2 = "remove_wish_list"
                            
                        else:
                            text1 = "✅Add to wish list✅" 
                            text2 = "add_to_wish_list"

                                    
                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online" )
                    button_wish_list = types.InlineKeyboardButton(text=text1, callback_data=text2)
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")

                except UnboundLocalError:
                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
                    button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")    

                markup_inline.add(button_link, button_wish_list, button_remind) 

                f = open('random_series.jpg','wb')
                f.write(urllib.request.urlopen(full_image).read())
                f.close()

                img = open('random_series.jpg', 'rb')
                bot.send_photo(message.chat.id, img, text, reply_markup=markup_inline)
                img.close()
            except KeyError:
                send_random_series()

            except urllib.error.HTTPError:
                send_random_series()
            
        send_random_series()
            
    elif get_mess_bot == "Сome back to the beginning🔙":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("🔝Top")
        btn2 = types.KeyboardButton("🎲Random")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "You can choose something another👇", parse_mode="html", reply_markup=markup)


    day = ""
    typee = ""

    get_mess_bot = message.text
    if get_mess_bot == "Day top for movie":
        day = "day"
        typee = "movie"
    elif get_mess_bot == "Week top for movie":
        day = "week"
        typee = "movie"
    elif get_mess_bot == "Day top for series":
        day = "day"
        typee = "series"
    elif get_mess_bot == "Week top for series":
        day = "week"
        typee = "series" 
    else:
        pass
    
    if typee == "movie":

        api_key = "124a9a01380f47d7fb0dc07e6d25ec26"
        url = f"https://api.themoviedb.org/3/trending/{typee}/{day}?api_key={api_key}"

        response = requests.get(url, headers={'Accept' : 'application/json'})

        data = response.json()

        i = 0 
        try:
            while i < 5:
            
                title = data["results"][i]["title"]
                image = data["results"][i]["poster_path"]
                full_image = f"https://image.tmdb.org/t/p/original{image}"
                overview = data["results"][i]["overview"]
                vote_average = data["results"][i]["vote_average"]            
                text_dict = {"title": "● Title" + " - " + title,
                            "vote_average": "⭐️ Vote average" + " - " + str(vote_average),
                            "overview": "📖 Overview" + " - " + overview 
                            }

                text = text_dict["title"] + "\n" + "\n" + text_dict["vote_average"] + "\n" + "\n" +text_dict["overview"]

                user_id = message.from_user.id
                try:   
                    conn = sqlite3.connect("Wish_list.db")
                    c = conn.cursor()  
                    c.execute("SELECT wish_list FROM Wish_list WHERE user_id=?", (user_id,))  
                    rows = c.fetchall()
                    markup_inline = types.InlineKeyboardMarkup() 
                    text1 = "✅Add to wish list✅" 
                    text2 = "add_to_wish_list"               
                    for row in rows:
                        new_row =  ''.join(row)
                        if new_row == text:
                            text1 = "❌Remove from wish list❌" 
                            text2 = "remove_wish_list"   
                        

                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online" )
                    button_wish_list = types.InlineKeyboardButton(text=text1, callback_data=text2)
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")
                except UnboundLocalError:
                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
                    button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")

                markup_inline.add(button_link, button_wish_list, button_remind)

                f = open('out.jpg','wb')
                f.write(urllib.request.urlopen(full_image).read())
                f.close()

                img = open('out.jpg', 'rb')
                bot.send_photo(message.chat.id, img, text, reply_markup=markup_inline)
                img.close()
                
                i += 1
                
        except KeyError:
            pass  


    elif typee == "series":
        
        api_key = "124a9a01380f47d7fb0dc07e6d25ec26"
        url = f"https://api.themoviedb.org/3/trending/tv/{day}?api_key={api_key}"
        response = requests.get(url, headers={'Accept' : 'application/json'})
        data = response.json()
        
        try:
            i = 0 
            while i < 5:

                title = data["results"][i]["name"]
                image = data["results"][i]["poster_path"]
                full_image = f"https://image.tmdb.org/t/p/original{image}"
                overview = data["results"][i]["overview"]
                vote_average = data["results"][i]["vote_average"]
                user_id = message.from_user.id

                text_dict = {"title": "● Title" + " - " + title,
                            "vote_average": "⭐️ Vote average" + " - " + str(vote_average),
                            "overview": "📖 Overview" + " - " + overview 
                            }
                text = text_dict["title"] + "\n" + "\n" + text_dict["vote_average"] + "\n" + "\n" +text_dict["overview"]
                try:
                    conn = sqlite3.connect("Wish_list.db")
                    c = conn.cursor()  
                    c.execute("SELECT wish_list FROM Wish_list WHERE user_id=?", (user_id,))  
                    rows = c.fetchall()
                    markup_inline = types.InlineKeyboardMarkup() 

                    for row in rows:
                        new_row =  ''.join(row)
                        if new_row == text:
                            text1 = "❌Remove from wish list❌" 
                            text2 = "remove_wish_list"
                            
                        else:
                            text1 = "✅Add to wish list✅" 
                            text2 = "add_to_wish_list"                    
                    
                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online" )
                    button_wish_list = types.InlineKeyboardButton(text=text1, callback_data=text2)  
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")

                except UnboundLocalError:
                    button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
                    button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")
                    button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")   
                     
                markup_inline.add(button_link, button_wish_list, button_remind)
                f = open('outt.jpg','wb')
                f.write(urllib.request.urlopen(full_image).read())
                f.close()
            
                img = open('outt.jpg', 'rb')
                bot.send_photo(message.chat.id, img, text, reply_markup=markup_inline)
                img.close()
                
                i += 1

        except KeyError:
              pass
           
   
    else:
        def notification_mess():
            conn = sqlite3.connect("Remind.db")
            c = conn.cursor()  
            text = c.execute("SELECT remind FROM remind WHERE user_id=?", (message.from_user.id,))  
            rows = text.fetchall()
            markup_inline = types.InlineKeyboardMarkup()                    
            
            button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online" )
            button_link1 = types.InlineKeyboardButton(text="❌Turn off notification❌", callback_data="turn_off")

            markup_inline.add(button_link1, button_link)
            bot.send_message(message.chat.id, rows, parse_mode="html", reply_markup=markup_inline)
        try:
            def fff():
                schedule.every().day.at(f"{get_mess_bot}").do(notification_mess).tag('daily-tasks', 'friend') 
                text = f"Ok👌\nI'll remind you to watch a movie at this time {get_mess_bot}\nYou can continue to work with the bot😝" 
                bot.send_message(message.chat.id, text) 

                while True:  
                    schedule.run_pending()   
                    time.sleep(1)
                    continue
            my_thread = threading.Thread(target=fff)
            my_thread.start()      
        except schedule.ScheduleValueError:
            pass

        
@bot.callback_query_handler(func=lambda call:True)
def check_inline_button(query):
    if query.data == "add_to_wish_list":
        markup_inline = types.InlineKeyboardMarkup()
        button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
        button_wish_list = types.InlineKeyboardButton(text="❌Remove from wish list❌", callback_data="remove_wish_list")
        button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")

        markup_inline.add(button_link, button_wish_list, button_remind)
        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=markup_inline)
        all_inf = query.message
        caption = all_inf.caption
        user_id = all_inf.chat.id

        
        conn = sqlite3.connect("Wish_list.db")
        c = conn.cursor()
        
        c.execute("INSERT INTO `user` (`user_id`) VALUES(?)", (user_id,))
        c.execute("INSERT INTO 'wish_list' (`user_id`, `wish_list`) VALUES(?,?)", (user_id,caption))
        conn.commit()
        conn.close()
            
    

    elif query.data == "remove_wish_list":
        markup_inline = types.InlineKeyboardMarkup()
        button_link = types.InlineKeyboardButton(text="Watch online🔗",callback_data="watch_online")
        button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")
        button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")
        markup_inline.add(button_link, button_wish_list, button_remind)
        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=markup_inline)
     
        all_inf = query.message
        caption = all_inf.caption
        user_id = all_inf.chat.id
        
        if caption == None:
            caption = query.message.text
        else:
            caption = all_inf.caption
    
        conn = sqlite3.connect("Wish_list.db")
        c = conn.cursor()
        c.execute("SELECT wish_list FROM Wish_list WHERE user_id=?", (user_id,)) 
        rows = c.fetchall()
       
        for row in rows:
            new_row =  ''.join(row)
            if new_row == caption:
                c.execute(f"DELETE FROM wish_list WHERE wish_list=? AND user_id={user_id}", (row))
        
        conn.commit()
        conn.close()
            

    elif query.data == "watch_online":
        markup_inline = types.InlineKeyboardMarkup()
        button_link1 = types.InlineKeyboardButton(text="OKKO", url="https://www.google.com.ua/?hl=ru")
        button_link2 = types.InlineKeyboardButton(text="IVI", url="https://www.google.com.ua/?hl=ru")
        button_link3 = types.InlineKeyboardButton(text="MEGOGO", url="https://www.google.com.ua/?hl=ru")
        button_link4 = types.InlineKeyboardButton(text="GOGLE", url="https://www.google.com.ua/?hl=ru")
        button_link5 = types.InlineKeyboardButton(text="SITE", url="https://www.google.com.ua/?hl=ru")
        button_link6 = types.InlineKeyboardButton(text="SITE", url="https://www.google.com.ua/?hl=ru")
        button_link7 = types.InlineKeyboardButton(text="SITE", url="https://www.google.com.ua/?hl=ru")
        button_link8 = types.InlineKeyboardButton(text="SITE", url="https://www.google.com.ua/?hl=ru")
        button_link9 = types.InlineKeyboardButton(text="SITE", url="https://www.google.com.ua/?hl=ru")
        button_link10 = types.InlineKeyboardButton(text="BACK 🔙", callback_data="BACK")

        markup_inline.add(button_link1, button_link2, button_link3, button_link4, button_link5, button_link6, button_link7, button_link8, button_link9, button_link10)
        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=markup_inline)


    elif query.data == "remind":
        try:
            markup_inline = types.InlineKeyboardMarkup()
            button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
            button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")
            button_notif = types.InlineKeyboardButton(text="❌Turn off notification❌", callback_data="turn_off")
            markup_inline.add(button_link, button_wish_list, button_notif)
            bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=markup_inline)
            caption1 = query.message.caption
            user_id = query.message.chat.id
            conn = sqlite3.connect("Remind.db")
            c = conn.cursor()
            
            
            c.execute("INSERT INTO 'remind' (`user_id`, `remind`) VALUES(?,?)", (user_id,caption1))
            conn.commit()
            conn.close()
            text = "‼ Please enter the time you want to receive notifications today👇\n‼ In this format👇\n<b>hour:minete</b> Example(22:00)"
            bot.send_message(query.message.chat.id, text, parse_mode="html")
        except sqlite3.IntegrityError:
            markup_inline = types.InlineKeyboardMarkup()
            button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
            button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")
            button_notif = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")
            markup_inline.add(button_link, button_wish_list, button_notif)
            bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=markup_inline)
            text = "🧐 You have already added one movie to your reminders and now to add this one you have to delete the last one ‼️"
            markup_inline = types.InlineKeyboardMarkup()
            button_notif = types.InlineKeyboardButton(text="❌Turn off❌", callback_data="turn_off1")
            markup_inline.add(button_notif)
            bot.send_message(query.message.chat.id, text, reply_markup=markup_inline)
            

            
    
    elif query.data == "turn_off":
        print("hi")
        schedule.clear('daily-tasks')
        all_inf = query.message
        caption = all_inf.text
        user_id = all_inf.chat.id

        conn = sqlite3.connect("Remind.db")
        c = conn.cursor()
        c.execute("SELECT remind FROM remind WHERE user_id=?", (user_id,)) 
        rows = c.fetchall()
        
        for row in rows:
            new_row =  ''.join(row)
            if new_row == caption:
                c.execute("DELETE FROM 'remind' WHERE user_id=? AND remind=?", (user_id, new_row,))
        conn.commit()
        conn.close()
        markup_inline = types.InlineKeyboardMarkup()
        button_link = types.InlineKeyboardButton(text="Watch online🔗",callback_data="watch_online")
        button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")
        button_remind = types.InlineKeyboardButton(text="📅Remind to watch📅", callback_data="remind")
        markup_inline.add(button_link, button_wish_list, button_remind)
        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=markup_inline)

        text = "You have successfully turned off notifications for this movie🙂"
        bot.send_message(query.message.chat.id, text)
    elif query.data == "turn_off1":
        schedule.clear('daily-tasks')
        all_inf = query.message
        caption = all_inf.text
        user_id = all_inf.chat.id

        conn = sqlite3.connect("Remind.db")
        c = conn.cursor()
        c.execute("DELETE FROM 'remind' WHERE user_id=?", (user_id,))
        conn.commit()
        conn.close()

        text = "👌Нou have successfully deleted notifications and now you can add a new movie🙂"
        bot.send_message(query.message.chat.id, text)
    elif query.data == "BACK":
        markup_inline = types.InlineKeyboardMarkup()
        button_link = types.InlineKeyboardButton(text="Watch online🔗", callback_data="watch_online")
        button_wish_list = types.InlineKeyboardButton(text="✅Add to wish list✅", callback_data="add_to_wish_list")

        markup_inline.add(button_link, button_wish_list)
        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=markup_inline)
     


if __name__ == '__main__':       
    bot.polling(none_stop=True, interval=0)
