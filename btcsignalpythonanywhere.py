import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Your bot's token (replace with your actual bot token)
bot_token = '7857232045:AAF9zUGzR8lQaieW773HfcrL-QNnJGU8BEY'  # Replace with your Telegram bot token

# Initialize the bot
bot = telebot.TeleBot(bot_token)

# Function to send the copied content to the user
def send_copied_content(chat_id):
    # Set up the ChromeDriver in headless mode
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Launch Chrome with the chromedriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Open the website
        url = "https://ha4bglol.github.io/bitcoin/"  # Replace with the URL of the website you want to open
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        # Extract the entire page text
        page_text = driver.find_element(By.TAG_NAME, "body").text

        # Extract content between "Oscillators" and "Summary"
        start_keyword = "Oscillators"
        end_keyword = "Summary"
        if start_keyword in page_text and end_keyword in page_text:
            # Extract the part of the text between the two keywords
            start_index = page_text.find(start_keyword)
            end_index = page_text.find(end_keyword) + len(end_keyword)
            filtered_content = page_text[start_index:end_index]

            # Remove the first 6 lines after the "Oscillators" keyword
            lines = filtered_content.splitlines()  # Split text into lines
            if len(lines) > 6:
                filtered_content = "\n".join(lines[:1] + lines[7:])  # Keep the first line (Oscillators) and skip next 6 lines

            # Replace "Sell" with "Buy" and "Buy" with "Sell"
            filtered_content = filtered_content.replace("Sell", "TEMP_SELL")  # Temporary placeholder
            filtered_content = filtered_content.replace("Buy", "Sell")  # Replace "Buy" with "Sell"
            filtered_content = filtered_content.replace("TEMP_SELL", "Buy")  # Replace placeholder with "Buy"
        else:
            # If the keywords are not found, send a fallback message
            filtered_content = "The keywords 'Oscillators' and 'Summary' were not found in the content."

        # Send the filtered content to the user via Telegram
        bot.send_message(chat_id, filtered_content)

    except Exception as e:
        # Handle any errors
        bot.send_message(chat_id, f"An error occurred: {str(e)}")
    finally:
        # Close the browser after the operations
        driver.quit()

# Handle the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Welcome! I will now get the data for you. Please wait...")

    # Trigger the process to scrape the content and send it
    send_copied_content(chat_id)

# Start the bot
bot.polling()
