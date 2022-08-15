import os
import urllib
from tempfile import TemporaryDirectory

from PIL import Image
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from web_base import Web_base


class Flaticon(Web_base):
    def __init__(self, url, weight='', corner='', name=''):
        """Construtor."""
        super().__init__()
        self.page = url
        self.weight = weight
        self.corner = corner
        self.name = name

    def calc_new_height(self, width, height, new_width):
        """Calcula o novo tamanho da imagem."""
        return round(new_width * height / width)

    def resize(self, file_path, new_width, new_img_name):
        """Redimenciona a imagem."""
        pillow_img = Image.open(file_path)
        width, height = pillow_img.size

        new_height = self.calc_new_height(width, height, new_width)

        new_img = pillow_img.resize(
            (new_width, new_height), Image.Resampling.LANCZOS
        )

        folder = f'{self.name}_{self.weight}_{self.corner}_{str(new_width)}'
        save_file_path = f'{os.getcwd()}\\flaticon\\icons\\{folder}'

        if not os.path.exists(save_file_path):
            os.makedirs(save_file_path)

        save_full_path = f'{save_file_path}\\{new_img_name}'

        try:
            new_img.save(
                save_full_path,
                optimize=True,
                quality=50,
            )
        except Exception as exc:
            raise RuntimeError(
                f'Não foi possivel converter a imagem "{file_path}".'
            ) from exc

    def download_interface_icons(self):
        """Realiza a navegação e o processo de download."""
        self.start_driver()
        self.navigate(url=self.page.format('', self.weight, self.corner))

        page_last = self.driver.find_element(
            By.ID, 'pagination-total'
        ).get_attribute('innerHTML')

        for page in range(2, int(page_last) + 2):
            unordered_list = self.driver.find_element(
                By.CLASS_NAME, 'uicons--results'
            )

            scroll = 50

            for index, li in enumerate(
                unordered_list.find_elements(By.TAG_NAME, 'li')
            ):
                try:
                    name = (
                        li.find_element(By.TAG_NAME, 'a').get_attribute(
                            'data-name'
                        )
                        + '.png'
                    )
                except NoSuchElementException:
                    break

                src = li.find_element(By.TAG_NAME, 'img').get_attribute('src')

                with TemporaryDirectory() as temp_dir:
                    file_path = f'{temp_dir}\\{name}'
                    urllib.request.urlretrieve(src, file_path)
                    proportions = (32, 24, 16)
                    for proportion in proportions:
                        self.resize(file_path, proportion, name)

                if index % 8 == 0:
                    self.driver.execute_script(f'window.scrollBy(0, {scroll})')
                    scroll += 50

            self.navigate(
                url=self.page.format('/' + str(page), self.weight, self.corner)
            )
        self.destroy_driver()

    def download_package_icons(self):
        """Realiza a navegação e o processo de download."""
        self.start_driver()
        self.navigate(url=self.page.format('', self.weight, self.corner))

        page_last = self.driver.find_element(
            By.ID, 'pagination-total'
        ).get_attribute('innerHTML')

        for page in range(2, int(page_last) + 2):
            itens_icon = (
                self.driver.find_element(By.ID, 'pack-view__inner')
                .find_element(By.CLASS_NAME, 'search-result')
                .find_element(By.CLASS_NAME, 'icons ')
                .find_elements(By.CLASS_NAME, 'icon--item')
            )

            scroll = 50

            for index, icon in enumerate(itens_icon):
                try:
                    name = icon.get_attribute('data-keyword_name') + '.png'
                    name = str(name).replace('\\', '-')
                except TypeError:
                    break

                src = icon.get_attribute('data-png')

                with TemporaryDirectory() as temp_dir:
                    file_path = f'{temp_dir}\\{name}'
                    urllib.request.urlretrieve(src, file_path)
                    proportions = (32, 24, 16)
                    for proportion in proportions:
                        self.resize(file_path, proportion, name)

                if index % 8 == 0:
                    self.driver.execute_script(f'window.scrollBy(0, {scroll})')
                    scroll += 50

            self.navigate(
                url=self.page.format('/' + str(page), self.weight, self.corner)
            )
        self.destroy_driver()


if __name__ == '__main__':
    packages = (
        'home-screen-apps-21',
        'stationery-34',
        'ui-28',
        'hacker-173',
        'folders-139',
        'domotics-81',
        'printing-137',
        'cyber-monday-205',
        'abstract-shapes-3',
        'scrapbooking-19',
        'origami-41',
        'mother-earth-day-111',
        'delivery-251',
        'work-from-home-93',
        'cyber-security-54',
        'google-suite-16',
        'design-thinking-88',
        'cryptocurrency-67',
        'location-98',
        'social-media-logos-3',
        'marketing-97',
        'protection-security-7',
        'marketing-growth-11',
        'e-commerce-85',
        'ui-interface-8',
    )
    for pack in packages:
        url = 'https://www.flaticon.com/br/packs/' + pack + '{}{}{}'
        name = ''.join([i for i in pack if not i.isdigit()])[:-1]
        flat = Flaticon(url, name=name)
        flat.download_package_icons()

    url = 'https://www.flaticon.com/br/uicons{}?brands=1{}{}'
    flat = Flaticon(url)
    flat.download_interface_icons()

    weights = ('regular', 'bold', 'solid')
    corners = ('straight', 'rounded')

    for corner in corners:
        for weight in weights:
            url = 'https://www.flaticon.com/br/uicons{}?weight={}&corner={}'
            flat = Flaticon(url, weight, corner)
            flat.download_interface_icons()
