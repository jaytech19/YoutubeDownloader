import telebot
from pytubefix import YouTube
import os

# Masukkan TOKEN Telegram disini
API_TOKEN = "7251759171:AAEnWyJ7HKXF51gJ8DwWRPKEYwrvhyk1gOs"

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Halo!
Saya Yotube Video Downloader, Saya bisa mengunduh video dari youtube. 
Untuk memulai kirimkan link youtube ke bot secara langsung atau tambahkan bot ke dalam grup dan kirimkan link ke grup tersebut. 

/help - Untuk info lebih lanjut\
""")

# Handle '/help'
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, """\
Youtube Downloader dapat mengunduh video dari Youtuve

Cara mengunduh video Youtube:
    1. Masuk ke aplikasi Youtube
    2. Pilih video Youtuve yang ingin kamu unduh
    3. Klik tombol bagikan atau titik tiga di kanan atas.
    4. Klik tombol "salin" atau "copy".
    5. Kirimkan link ke bot dan dapatkan video Anda tanpa watermark\
""")


# Handle semua pesan text
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    url = message.text

    # validasi URL Youtube
    if "youtube.com" not in url and "youtu.be" not in url :
        bukanURLYoutube = "Tolong kirimkan link Youtube yang benar"
        bot.reply_to(message,bukanURLYoutube)
        return
    
    # Mencoba memproses video
    try :
        # Tampilkan pesan sedang memproses video
        bot.reply_to(message,"Sedang memproses video, mohon tunggu...")
        # Ambil informasi video Youtube
        yt = YouTube(url)
        # Memilih video resolusi 480p
        video_stream =  yt.streams.filter(file_extension="mp4", res="480p").first()
        # Memberikan nama default video
        video_title = video_stream.default_filename
        # Mengunduh video
        video_stream.download()
        # Mengirimkan video ke bot telegram
        with open (video_title,'rb') as video:
            bot.send_video(message.chat.id,video)
        # Menghapus video di komputer ini setelah dikirimkan ke bot telegram
        os.remove(video_title)

        
    # Jika terjadi kesalahan
    except Exception as e:
        # Tampilkan kesalahan saat memproses
        bot.reply_to(message,f"Terjadi kesalahan saat mengunduh video : {str(e)}")
print("The bot is running...")
bot.infinity_polling()