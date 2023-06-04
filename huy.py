from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import signal

# Чтение списка прокси из файла
with open('proxies.txt', 'r') as file:
    proxies = file.read().splitlines()

# Функция для проверки прокси
def check_proxy(proxy):
    try:
        # Настройка Chrome Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Включение скрытого режима
        chrome_options.add_argument(f'--proxy-server=socks4://{proxy}')
        
        with webdriver.Chrome(options=chrome_options) as driver:
            # Загрузка страницы
            driver.get('https://minecraft.org.ua/minecraft-servers/Helix-Vanilla/536')

            # Ожидание появления кнопки
            button_locator = (By.CSS_SELECTOR, 'button.mc-button:nth-child(2)')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(button_locator))

            # Нажатие на кнопку
            button = driver.find_element(*button_locator)
            button.click()
            print(f"Нажал на прокси {proxy}")

    except Exception as e:
        print(f'Произошла ошибка с прокси {proxy}')

# Функция для обработки сигнала прерывания (Ctrl+C)
def handle_interrupt(signal, frame):
    print('Прерывание скрипта...')
    # Остановка выполнения потоков и завершение работы браузера
    executor.shutdown(wait=False)
    for thread in threads:
        thread.join()
    # Выход из программы
    sys.exit(0)

# Регистрация обработчика сигнала прерывания
signal.signal(signal.SIGINT, handle_interrupt)

# Использование пула потоков
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    # Сохранение ссылки на пул потоков для последующего завершения
    threads = executor.map(check_proxy, proxies)
    # Ожидание завершения всех потоков
    executor.shutdown(wait=True)