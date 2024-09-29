
# Telegram Result Bot

This is a Python-based Telegram bot that allows users to retrieve their exam results by entering their roll number and selecting their course, year, and semester. The bot is built using the `telebot` library and includes a Flask server to keep it running.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Welcome Message**: Sends a welcome message when the user starts the bot.
- **Interactive Course Selection**: Users can choose between BA and BSC courses.
- **Year and Semester Selection**: Users can specify the year (2020-2024) and semester (1st to 6th).
- **PDF Result Retrieval**: Fetches and sends the result PDF if available, or notifies the user if not.
- **Error Handling**: Manages HTTP errors and unexpected issues gracefully.

## Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/telegram-result-bot.git
   cd telegram-result-bot
   ```

2. **Install Dependencies**
   Ensure you have Python 3.x and pip installed, then run:
   ```bash
   pip install pyTelegramBotAPI requests Flask
   ```

3. **Configure Your Bot Token**
   Replace the placeholder token in your script with your actual Telegram bot token:
   ```python
   TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
   ```

4. **Run the Bot**
   Execute the script to start the bot:
   ```bash
   python your_bot_script.py
   ```

## Usage

- Start a conversation with your bot on Telegram and type `/start`.
- Follow the interactive prompts to select your course, year, and semester.
- Receive your result PDF if available, or a notification if it's not.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
