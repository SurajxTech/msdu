import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from flask import Flask  
import time  

app = Flask(__name__)  

@app.route('/')  
def home():  
    return "Hello, I'm alive!"  

# Your provided Telegram bot token
TOKEN = '7403608188:AAGqQWqmWowWamTnqu4ElLRepxt-V3vJrGY'

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# Function to start the bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Please send me your roll number to get the PDF result.")

# Function to ask for BA/BSC selection
@bot.message_handler(func=lambda message: True)
def ask_for_course(message):
    roll_number = message.text.strip()

    # Create a markup for course selection (BA or BSC)
    markup_course = InlineKeyboardMarkup()
    markup_course.add(InlineKeyboardButton("BA", callback_data=f"course_BA_{roll_number}"))
    markup_course.add(InlineKeyboardButton("BSC", callback_data=f"course_BSC_{roll_number}"))

    bot.send_message(message.chat.id, "Please choose your course:", reply_markup=markup_course)

# Handle course selection and then ask for year
@bot.callback_query_handler(func=lambda call: call.data.startswith('course'))
def handle_course_selection(call):
    data = call.data.split('_')
    course = data[1]  # BA or BSC
    roll_number = data[2]  # Extract roll number

    # Create a markup for year selection (2020-2024)
    markup_year = InlineKeyboardMarkup()
    markup_year.add(InlineKeyboardButton("2020", callback_data=f"year_2020_{course}_{roll_number}"))
    markup_year.add(InlineKeyboardButton("2021", callback_data=f"year_2021_{course}_{roll_number}"))
    markup_year.add(InlineKeyboardButton("2022", callback_data=f"year_2022_{course}_{roll_number}"))
    markup_year.add(InlineKeyboardButton("2023", callback_data=f"year_2023_{course}_{roll_number}"))
    markup_year.add(InlineKeyboardButton("2024", callback_data=f"year_2024_{course}_{roll_number}"))

    bot.send_message(call.message.chat.id, "Please choose the year:", reply_markup=markup_year)

# Handle year selection and then ask for semester
@bot.callback_query_handler(func=lambda call: call.data.startswith('year'))
def handle_year_selection(call):
    data = call.data.split('_')
    year = data[1]  # Extract year (2020, 2021, 2022, 2023, 2024)
    course = data[2]  # BA or BSC
    roll_number = data[3]  # Extract roll number

    # Create a markup for semester selection (1st to 6th Semester)
    markup_semester = InlineKeyboardMarkup()
    markup_semester.add(InlineKeyboardButton("1st Semester", callback_data=f"sem1_{year}_{course}_{roll_number}"))
    markup_semester.add(InlineKeyboardButton("2nd Semester", callback_data=f"sem2_{year}_{course}_{roll_number}"))
    markup_semester.add(InlineKeyboardButton("3rd Semester", callback_data=f"sem3_{year}_{course}_{roll_number}"))
    markup_semester.add(InlineKeyboardButton("4th Semester", callback_data=f"sem4_{year}_{course}_{roll_number}"))
    markup_semester.add(InlineKeyboardButton("5th Semester", callback_data=f"sem5_{year}_{course}_{roll_number}"))
    markup_semester.add(InlineKeyboardButton("6th Semester", callback_data=f"sem6_{year}_{course}_{roll_number}"))

    bot.send_message(call.message.chat.id, "Please choose the semester:", reply_markup=markup_semester)

# Handle semester selection and send the result PDF
@bot.callback_query_handler(func=lambda call: call.data.startswith('sem'))
def handle_semester_selection(call):
    data = call.data.split('_')
    semester = data[0]  # sem1, sem2, sem3, sem4, sem5, sem6
    year = data[1]  # Extract the year (2020, 2021, 2022, 2023, 2024)
    course = data[2]  # Extract the course (BA or BSC)
    roll_number = data[3]  # Extract roll number

    # Construct the URL for the result PDF based on the course, year, and semester
    base_url = f"https://msduexam.co.in/RESULT/YEAR-{year}/UG/{course}/{semester.upper()}/{roll_number}.pdf"

    # Check if the PDF exists
    response = requests.get(base_url)

    # If the PDF is found (status 200)
    if response.status_code == 200:
        pdf_file_path = f"{roll_number}_{semester}.pdf"

        with open(pdf_file_path, 'wb') as file:
            file.write(response.content)

        with open(pdf_file_path, 'rb') as file:
            bot.send_document(call.message.chat.id, file, caption=f"Here is the result for roll number: {roll_number} - {semester} - {course} - Year {year}")

        # Clean up by removing the file
        os.remove(pdf_file_path)

    elif response.status_code == 404:
        # Handle 404 Not Found
        bot.send_message(call.message.chat.id, f"Sorry, the result for roll number {roll_number} - {semester} - {course} - Year {year} is not available. Please check if the roll number and selection are correct or try again later.")

    else:
        # Handle any other unexpected response codes
        bot.send_message(call.message.chat.id, f"An unexpected error occurred (status code: {response.status_code}). Please try again later.")

# Start polling
# Start the bot  
if __name__ == '__main__':  
    from threading import Thread  
    Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000}).start()  

    while True:  
        try:  
            bot.polling()  
        except Exception:  
            time.sleep(15)
