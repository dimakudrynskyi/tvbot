import telebot 
from telebot import types

def markup_button_name(name):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for names in name:
        btn1 = types.KeyboardButton(f"{names}")
        markup.add(btn1)
    return markup

def inline_link_button_name(name):
    markup_inline = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton(text="BACK🔙", callback_data="BACK")
    i = 0
    while i < len(name.keys()):
        btn1 = types.InlineKeyboardButton(text=list(name.keys())[i], url=list(name.values())[i])
        markup_inline.add(btn1)
        i += 1
    markup_inline.add(back_btn)
    return markup_inline

def inline_button_name(name):
    markup_inline = types.InlineKeyboardMarkup()
    i = 0
    while i < len(name.keys()):
        btn1 = types.InlineKeyboardButton(text=list(name.keys())[i], callback_data=list(name.values())[i])
        markup_inline.add(btn1)
        i += 1
    return markup_inline