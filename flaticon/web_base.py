from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Web_base:
    def __init__(self, caminho_download=False, anonimo=False, invisivel=False):
        """Construtor."""
        self.caminho_download = caminho_download
        self.anonimo = anonimo
        self.invisivel = invisivel
        self.status_driver = False

    def start_driver(self):
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if self.caminho_download:
            prefs = {'download.default_directory': self.caminho_download}
            options.add_experimental_option('prefs', prefs)
        options.headless = self.invisivel
        options.add_argument('ignore-certificate-errors')
        if self.anonimo:
            options.add_argument('--incognito')
        servico = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=servico, options=options)
        self.status_driver = True

    def find_element(self, elem, By=By.NAME):
        try:
            delay = 3  # seconds
            WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By, elem))
            )
            return True
        except TimeoutException:
            return False

    def destroy_driver(self):
        try:
            self.driver.quit()
            return True, 'sucesso'
        except Exception as error:
            return False, error

    def restart_driver(self):
        self.destroy_driver()
        self.start_driver()

    def navigate(self, url):
        try:
            self.driver.get(url)
            sleep(0.5)
            return True
        except TimeoutException as ex:
            print('Ocorreu ma falha na conexão. ' + str(ex))
            return False
