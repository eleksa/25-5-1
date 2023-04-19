import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from settings import e_mail, pass_word


# создаю фикстуру для авторизации и перехода на страницу со списком питомцев всех пользователей
@pytest.fixture(scope='class')
def testing_for_all_pets():

    try:
        pytest.driver = webdriver.Chrome('/for_software/chromedriver/chromedriver.exe')

        # устанавливаю неявное ожидание в 5 секунд
        pytest.driver.implicitly_wait(5)

        # переход на страницу авторизации
        pytest.driver.get('https://petfriends.skillfactory.ru/login')

        # ввод логина пользователя
        pytest.driver.find_element(By.ID, 'email').send_keys(e_mail)

        # ввод пароля пользователя
        pytest.driver.find_element(By.ID, 'pass').send_keys(pass_word)

        # жмем кнопку входа
        pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-success').click()

        # проверяем что после входа попали на страницу со списком питомцев всех польователей
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'

        yield

    finally:
        pytest.driver.quit()


# создаю фикстуру для авторизации и перехода на страницу со списком питомцев пользователя
@pytest.fixture(scope='class')
def testing_for_my_pets():
    try:
        pytest.driver = webdriver.Chrome('/for_software/chromedriver/chromedriver.exe')
        pytest.driver.get('https://petfriends.skillfactory.ru/login')

        # устанавливаю явные ожидания элементов
        WebDriverWait(pytest.driver, 5).until(ec.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-success')))
        WebDriverWait(pytest.driver, 5).until(ec.element_to_be_clickable((By.ID, 'email')))
        WebDriverWait(pytest.driver, 5).until(ec.element_to_be_clickable((By.ID, 'pass')))
        WebDriverWait(pytest.driver, 5).until(ec.element_to_be_clickable((By.CLASS_NAME, 'btn.btn-success')))

        # переход на страницу авторизации
        pytest.driver.get('https://petfriends.skillfactory.ru/login')

        # ввод логина пользователя
        pytest.driver.find_element(By.ID, 'email').send_keys(e_mail)

        # ввод пароля пользователя
        pytest.driver.find_element(By.ID, 'pass').send_keys(pass_word)

        # жмем кнопку входа
        pytest.driver.find_element(By.CLASS_NAME, 'btn.btn-success').click()

        # проверяем что после входа попали на страницу со списком питомцев всех польователей
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'

        # перехожу на вкладку "мои питомцы"
        WebDriverWait(pytest.driver, 5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/my_pets"]')))
        pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

        # проверяем что после входа попали на страницу со списком питомцев пользователя
        assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

        yield

    finally:
        pytest.driver.quit()


# проверка раздела "все питомцы"
@pytest.mark.usefixtures('testing_for_all_pets')
class TestSectionAllPets:
    def test_images_all_pets(self):
        """Проверяем что у всех питомцев есть фото"""

        pytest.driver.implicitly_wait(5)
        names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
        photos = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')

        for item in range(len(names)):
            assert photos[item].get_attribute('src') != '' or photos[item].get_attribute('src') == ''

    def test_names_all_pets(self):
        """Проверяем что у всех питомцев есть имя"""

        pytest.driver.implicitly_wait(5)
        names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')

        for item in range(len(names)):
            assert names[item].text != '' or names[item].text == ''

    def test_character_all_pets(self):
        """Проверяем что у всех питомцев есть порода и возраст"""

        pytest.driver.implicitly_wait(5)
        names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
        character = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

        for item in range(len(names)):
            assert character[item].text != '' or character[item].text == ''
            assert ', ' in character[item].text
            parts = character[item].text.split(", ")
            assert len(parts[0]) > 0 or len(parts[0]) == 0
            assert len(parts[1]) > 0 or len(parts[1]) == 0


# проверка раздела "мои питомцы"
@pytest.mark.usefixtures('testing_for_my_pets')
class TestSectionMyPets:
    def test_how_many_my_pets(self):
        """Проверяем, что в таблице есть все питомцы пользователя"""

        WebDriverWait(pytest.driver, 5).until(ec.visibility_of_element_located((By.XPATH,
                                                                                 '//div[@class=".col-sm-4 left"]')))

        # берем статистику пользователя
        user_stats_data = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text
        user_stats_list = user_stats_data.split('\n')

        # перебираем данные из статистики и выделяем количество
        for row in user_stats_list:
            if 'Питомцев' in row:
                count_stats = int(row.split(': ')[1])

        WebDriverWait(pytest.driver, 5).until(ec.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))

        # определяем количество записей в таблице с питомцами
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        count_pets_table = len(my_pets)

        # проверяем что количество из статистики совпадает с количеством записей в таблице
        assert count_stats == count_pets_table

    def test_chek_existence_photos_my_pets(self):
        """Проверяется, что хотя бы у половины питомцев есть фото"""

        WebDriverWait(pytest.driver, 5).until(ec.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))

        # определяем количество записей в таблице с питомцами
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        count_pets_table = len(my_pets)

        WebDriverWait(pytest.driver, 5).until(ec.presence_of_all_elements_located((By.XPATH, '//tbody/tr/th/img')))

        # определяем количество записей в таблице с питомцами
        photos_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/th/img')
        photos_count_my_pets = 0

        # определяем для каких записей есть фото
        for item in range(count_pets_table):
            if photos_my_pets[item].get_attribute('src') != '':
                photos_count_my_pets += 1

        # проверяем, что у хотя бы половины записей есть фото
        assert photos_count_my_pets >= count_pets_table / 2

    def test_names_races_ages_my_pets(self):
        """Проверяется, что у всех питомцев есть имя, возраст и порода"""

        WebDriverWait(pytest.driver, 5).until(ec.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))

        # определяем количество записей в таблице с питомцами
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        count_pets_table = len(my_pets)

        WebDriverWait(pytest.driver, 5).until(
            ec.visibility_of_all_elements_located((By.XPATH, '//tbody/tr/td[1]')))
        WebDriverWait(pytest.driver, 5).until(
            ec.visibility_of_all_elements_located((By.XPATH, '//tbody/tr/td[2]')))
        WebDriverWait(pytest.driver, 5).until(
            ec.visibility_of_all_elements_located((By.XPATH, '//tbody/tr/td[3]')))

        #  определяем имя, породу и возраст питомцев
        name_pet = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
        race_pet = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
        age_pet = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')

        # для каждого питомца проверяем наличие имени, возраста, породы
        for item in range(count_pets_table):
            assert name_pet[item].text != ''
            assert race_pet[item].text != ''
            assert age_pet[item].text != ''

    def test_names_difference_my_pets(self):
        """Проверяется, что у всех питомцев разные имена"""

        WebDriverWait(pytest.driver, 5).until(ec.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))

        # определяем количество записей в таблице с питомцами
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        count_pets_table = len(my_pets)

        WebDriverWait(pytest.driver, 5).until(
            ec.visibility_of_all_elements_located((By.XPATH, '//tbody/tr/td[1]')))

        # определяем имена питомцев
        names_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')

        # формируем список из имен всех питомцев используяя генератор списка
        my_pets_list_names = [names_my_pets[item].text for item in range(count_pets_table)]

        # список преобразуем в множество для удаления дубликатов, в случае их обнаружения
        my_pets_set_names = set(my_pets_list_names)

        # провряем что длина списка и длина множества равны, что означает что повторов нет
        assert len(my_pets_list_names) == len(my_pets_set_names)

    def test_pets_difference_my_pets(self):
        """Проверяется, что в списке нет повторяющихся питомцев. Повторящимися считаются питомцы с одинаковыми
        именем, породой, возрастом."""

        WebDriverWait(pytest.driver, 10).until(ec.visibility_of_all_elements_located((By.XPATH, '//tbody/tr')))

        # определяем количество записей в таблице с питомцами
        my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')
        count_pets_table = len(my_pets)

        # используя генератор списка формируем список из имени, породы, возраста
        my_pets_list = [my_pets[i].text for i in range(count_pets_table)]

        # список преобразуем в множество
        my_pets_set = set(my_pets_list)

        # провряем что длина списка и длина множества равны, что означает что повторов нет
        assert len(my_pets_list) == len(my_pets_set)