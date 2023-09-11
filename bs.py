import re
import time
import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot
from googletrans import Translator

def get_div_content():

    driver_path = './chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')

    service = ChromeService(executable_path=driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = 'https://www.counter-strike.net/news/updates'

        driver.get(url)

        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.blogoverviewpage_SubUpdates_31uv5')))

        dynamic_html = element.get_attribute('innerHTML')

    except Exception as e:
        print(f'Ошибка: {e}')
        driver.quit()
        return None

    finally:
        driver.quit()

    soup = BeautifulSoup(dynamic_html, 'html.parser')

    div_element = soup.find('div', class_='updatecapsule_UpdateCapsule_-Eouv')

    if div_element:

        div_content = div_element

        div_content = re.sub(r'</div>', '</div>\n', str(div_content))

        div_content = re.sub(r'<br/>', '\n', div_content)

        div_content = re.sub(r'<ul[^>]*>', '\n', div_content)
        div_content = re.sub(r'</ul>', '\n', div_content)
        div_content = re.sub(r'<li[^>]*>', '• ', div_content)

        div_content = re.sub(r'<[^>]*>', '', div_content)

        translator = Translator()
        translated_text = translator.translate(div_content, src='en', dest='ru')

        return translated_text.text
    else:
        print('Элемент div не найден.')
        return None

previous_content = None


bot_token = '6307636565:AAEnPGLQJvKnD7BxUif8AEws7UV3WABHsQA'
bot = Bot(token=bot_token)

async def send_message(chat_id, text):
                await bot.send_message(chat_id=chat_id, text=text)

chat_id = '409878162'



while True:
    current_content = get_div_content()

    if current_content:
        if current_content != previous_content:
            print("Содержимое элемента div:")
            print(current_content)
            previous_content = current_content

            async def note():
                try:
                    
                    message_text = "--ВЫШЛА ОБНОВА--\n" + current_content
                    await send_message(chat_id, message_text)
                except Exception as e:
                    print(f"Ошибка при отправке сообщения: {e}")

            if __name__ == '__main__':
                asyncio.run(note())

    time.sleep(120)