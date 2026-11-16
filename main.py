import os
import telebot
import yt_dlp

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send TikTok link")

@bot.message_handler(func=lambda m: 'tiktok.com' in m.text)
def download(message):
    url = message.text.strip()
    bot.reply_to(message, "Downloading... Please wait")
    try:
        ydl_opts = {'format': 'mp4', 'outtmpl': 'video.mp4', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        with open('video.mp4', 'rb') as f:
            bot.send_video(message.chat.id, f)
        os.remove('video.mp4')
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

@bot.message_handler(func=lambda m: True)
def other(message):
    bot.reply_to(message, "Send a valid TikTok link")

bot.polling()
