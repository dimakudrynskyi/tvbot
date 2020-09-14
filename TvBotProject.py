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
import config
from wish_list_SQL import sqlighter
from remind_SQL import Sqlighter
from button import markup_button_name, inline_link_button_name,inline_button_name

API_KEY = os.environ["API_KEY"]

API_TOKEN = os.environ["API_TOKEN"]
bot = telebot.TeleBot(API_TOKEN)


def send_top(typee,day,message):
    url = f"https://api.themoviedb.org/3/trending/{typee}/{day}?api_key={API_KEY}"
    response = requests.get(url, headers={'Accept' : 'application/json'})
    data = response.json()

    i = 0 
    try:
        while i < 5:
            if typee == "tv":
                title = data["results"][i]["name"]
            else:
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
                db = sqlighter("Wish_list.db")
                if db.select_wish_list(user_id) == text:                    
                    text1 = "❌Remove from wish list❌" 
                    text2 = "remove_wish_list" 
                else:
                    text1 = "✅Add to wish list✅" 
                    text2 = "add_to_wish_list"
    
                name = {"Watch online🔗":"watch_online",
                        text1:text2,
                        "📅Remind to watch📅":"remind"
                        }  

            except UnboundLocalError:
                name = {"Watch online🔗":"watch_online",
                        "✅Add to wish list✅":"add_to_wish_list",
                        "📅Remind to watch📅":"remind"
                        }  

            f = open('out.jpg','wb')
            f.write(urllib.request.urlopen(full_image).read())
            f.close()

            img = open('out.jpg', 'rb')
            bot.send_photo(message.chat.id, img, text, reply_markup=inline_button_name(name))
            img.close()
            
            i += 1
            
    except KeyError:
        pass  

def send_random_film(film_type, message):
    random_numder = random.randint(125,99999)
    movie_id = str(random_numder)
    url =  f"https://api.themoviedb.org/3/{film_type}/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url, headers={'Accept' : 'application/json'})
    data = response.json()

    try:
        if film_type == "tv":
            title = data["name"]
        else:
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
            db = sqlighter("Wish_list.db")
            if db.select_wish_list(user_id) == text:                    
                text1 = "❌Remove from wish list❌" 
                text2 = "remove_wish_list" 
            else:
                text1 = "✅Add to wish list✅" 
                text2 = "add_to_wish_list"

            name = {"Watch online🔗":"watch_online",
                    text1:text2,
                    "📅Remind to watch📅":"remind"
                    }  

        except UnboundLocalError:
            name = {"Watch online🔗":"watch_online",
                    "✅Add to wish list✅":"add_to_wish_list",
                    "📅Remind to watch📅":"remind"
                    } 

        f = open('random_film.jpg','wb')
        f.write(urllib.request.urlopen(full_image).read())
        f.close()

        img = open('random_film.jpg', 'rb')
        bot.send_photo(message.chat.id, img, text, reply_markup=inline_button_name(name))
        img.close() 

    except KeyError:
        send_random_film(film_type, message) 

    except urllib.error.HTTPError:
        send_random_film(film_type, message) 


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
def help_mess(message):
    mess = f"<b>Hi i am a tvBot!😀</b>\nBelow is a list of all my commands👇\n●1 - /help - List of comands\n●2 - /film_and_series - Top and random\n●3 - /subscribe - Subscribed to our tvBot\n●4 - /unsubscribe - Unsubscribed from our tvBot\n●5 - /upcoming - Watch upcomung flm\n●6 - /wish_list - Movies your liked"

    bot.send_message(message.chat.id, mess, parse_mode="html")


@bot.message_handler(commands = ["wish_list"])
def wish_list(message):
    user_id = message.from_user.id
    name = {"Watch online🔗":"watch_online",
        "❌Remove from wish list❌":"remove_wish_list",
        "📅Remind to watch📅":"remind"
        }
    inline_button_name(name)
    db = sqlighter("Wish_list.db")

    bot.send_message(message.chat.id, db.select_wish_list(user_id), parse_mode="html", reply_markup=inline_button_name(name))



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

                try:   
                    db = sqlighter("Wish_list.db")
                    if db.select_wish_list(user_id) == text:                    
                        text1 = "❌Remove from wish list❌" 
                        text2 = "remove_wish_list" 
                    else:
                        text1 = "✅Add to wish list✅" 
                        text2 = "add_to_wish_list"
        
                    name = {"Watch online🔗":"watch_online",
                            text1:text2,
                            "📅Remind to watch📅":"remind"
                            }  

                except UnboundLocalError:
                    name = {"Watch online🔗":"watch_online",
                            "✅Add to wish list✅":"add_to_wish_list",
                            "📅Remind to watch📅":"remind"
                            } 
                
                f = open('upcoming.jpg','wb')
                f.write(urllib.request.urlopen(full_image).read())
                f.close()

                img = open('upcoming.jpg', 'rb')
                bot.send_photo(message.chat.id, img, text, reply_markup=inline_button_name(name))
                img.close()
            i += 1
    except KeyError:
        pass  


@bot.message_handler(commands = ["film_and_series"])
def film_and_series(message):
    names = ["🔝Top", "🎲Random","/wish_list"]
    markup_button_name(names)
    mess = "Choose from the list below what you want to know 👇"
    bot.send_message(message.chat.id, mess, parse_mode="html", reply_markup=markup_button_name(names))



@bot.message_handler(content_types=["text"]) 

def check_mess(message):
    get_mess_bot = message.text

    if get_mess_bot == "🔝Top":
        names = ["Movie", "Series", "Сome back to the beginning🔙"]
        markup_button_name(names)
        mess = "Do you want to know the top SERIES or MOVIES ?"
        bot.send_message(message.chat.id, mess, parse_mode="html", reply_markup=markup_button_name(names))

    elif get_mess_bot == "🎲Random":
        names = ["🎲Random film", "🎲Random series", "Сome back to the beginning🔙"]
        markup_button_name(names)
        mess = "Do you want to watch a random movie or TV series?"
        bot.send_message(message.chat.id, mess, parse_mode="html", reply_markup=markup_button_name(names))

    elif get_mess_bot == "Movie":
        names =["Day top for movie", "Week top for movie", "Сome back to the beginning🔙"]
        markup_button_name(names)
        final_mess = "Do you want to see the top movies of the last DAY or the WEEK??"
        bot.send_message(message.chat.id, final_mess, parse_mode="html", reply_markup=markup_button_name(names))

    elif get_mess_bot == "Series":
        names = ["Day top for series", "Week top for series", "Сome back to the beginning🔙"]
        markup_button_name(names)
        final_mess = "Do you want to see the top movies of the last DAY or the WEEK??"
        bot.send_message(message.chat.id, final_mess, parse_mode="html", reply_markup=markup_button_name(names))

    elif get_mess_bot == "🎲Random film":
        film_type = "movie"
        send_random_film(film_type, message)
    
   
    elif get_mess_bot == "🎲Random series":
        film_type = "tv"
        send_random_film(film_type, message)

            
    elif get_mess_bot == "Сome back to the beginning🔙":
        names = ["🔝Top", "🎲Random","/wish_list"]
        markup_button_name(names)
        mess = "You can choose something another👇"
        bot.send_message(message.chat.id, mess, parse_mode="html", reply_markup=markup_button_name(names))


    get_mess_bot = message.text
    if get_mess_bot == "Day top for movie":
        day = "day"
        typee = "movie"
        send_top(typee, day, message)

    elif get_mess_bot == "Week top for movie":
        day = "week"
        typee = "movie"
        send_top(typee, day, message)

    elif get_mess_bot == "Day top for series":
        day = "day"
        typee = "tv"
        send_top(typee, day, message)

    elif get_mess_bot == "Week top for series":
        day = "week"
        typee = "tv" 
        send_top(typee, day, message)
   
    else:
        def notification_mess():
            db = Sqlighter("Remind.db")
            name = {"Watch online🔗":"watch_online",
                    "❌Turn off notification❌":"turn_off"
                    }                 

            bot.send_message(message.chat.id, db.send_remind(message.from_user.id), parse_mode="html", reply_markup=inline_button_name(name))
            def send_notification_mess():
                try:
                    schedule.every().day.at(f"{get_mess_bot}").do(notification_mess).tag('daily-tasks', 'friend') 
                    text = f"Ok👌\nI'll remind you to watch a movie at this time {get_mess_bot}\nYou can continue to work with the bot😝" 
                    bot.send_message(message.chat.id, text) 

                    while True:  
                        schedule.run_pending()   
                        time.sleep(1)
                        continue
                except schedule.ScheduleValueError:
                    print("hi")
                    pass
            my_thread = threading.Thread(target=send_notification_mess)
            my_thread.start()      


        
@bot.callback_query_handler(func=lambda call:True)
def check_inline_button(query):
    all_inf = query.message
    if query.data == "add_to_wish_list":
        name = {"Watch online🔗":"watch_online",
                "❌Remove from wish list❌":"remove_wish_list",
                "📅Remind to watch📅":"remind"
                }

        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_button_name(name))
        
        caption = all_inf.caption
        user_id = all_inf.chat.id

        db = sqlighter("Wish_list.db")
        db.add_to_wish_list(user_id, caption)
    
    elif query.data == "remove_wish_list":
        name = {"Watch online🔗":"watch_online",
                "✅Add to wish list✅":"add_to_wish_list",
                "📅Remind to watch📅":"remind"
                }

        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_button_name(name))
     
        caption = all_inf.caption
        user_id = all_inf.chat.id
        
        if caption == None:
            caption = query.message.text
        else:
            caption = all_inf.caption

        db = sqlighter("Wish_list.db")
        db.remove_wish_list(user_id, caption)

    elif query.data == "watch_online":
        name = {"OKKO":"https://www.google.com.ua/?hl=ru", 
                "IVI":"https://www.google.com.ua/?hl=ru",
                "GOOGLE":"https://www.google.com.ua/?hl=ru"
                }
       
        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_link_button_name(name))

    elif query.data == "remind":
        try:
            name = {"Watch online🔗":"watch_online",
                    "✅Add to wish list✅":"add_to_wish_list",
                    "❌Turn off notification❌":"turn_off"
                    }

            bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_button_name(name))
            caption = query.message.caption
            user_id = query.message.chat.id

            db = Sqlighter("Remind.db")
            db.add_remind(user_id, caption) 

            text = "‼ Please enter the time you want to receive notifications today👇\n‼ In this format👇\n<b>hour:minete</b> Example(22:00)"
            bot.send_message(query.message.chat.id, text, parse_mode="html")
        except sqlite3.IntegrityError:
            name = {"Watch online🔗":"watch_online",
                    "✅Add to wish list✅":"add_to_wish_list",
                    "📅Remind to watch📅":"remind"
                    }
            
            bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_button_name(name))

            text = "🧐 You have already added one movie to your reminders and now to add this one you have to delete the last one ‼️"
            markup_inline = types.InlineKeyboardMarkup()
            button_notif = types.InlineKeyboardButton(text="❌Turn off❌", callback_data="turn_off1")
            markup_inline.add(button_notif)
            bot.send_message(query.message.chat.id, text, reply_markup=markup_inline)
    
    elif query.data == "turn_off":
        schedule.clear('daily-tasks')

        caption = all_inf.text
        user_id = all_inf.chat.id

        db = Sqlighter("Remind.db")
        db.delete_remind(user_id, caption) 

        name = {"Watch online🔗":"watch_online",
                "✅Add to wish list✅":"add_to_wish_list",
                "📅Remind to watch📅":"remind"
                }
        
        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_button_name(name))

        text = "You have successfully turned off notifications for this movie🙂"
        bot.send_message(query.message.chat.id, text)
    elif query.data == "turn_off1":
        schedule.clear('daily-tasks')
        user_id = query.message.chat.id

        db = Sqlighter("Remind.db")
        db.delete_all_remind(user_id) 

        text = "👌Нou have successfully deleted notifications and now you can add a new movie🙂"
        bot.send_message(query.message.chat.id, text)
    elif query.data == "BACK":
        name = {"Watch online🔗":"watch_online",
                "✅Add to wish list✅":"add_to_wish_list",
                "📅Remind to watch📅":"remind"
                }
        
        bot.edit_message_reply_markup(query.message.chat.id, message_id=query.message.message_id, reply_markup=inline_button_name(name))
     


if __name__ == '__main__':       
    bot.polling(none_stop=True, interval=0)
