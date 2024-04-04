from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import openpyxl



def select_flights():
    flights_button = driver.find_element(By.XPATH, '//span[text()="Flights"]')
    flights_button.click()


def click_one_way():
    one_way_button = driver.find_element(By.XPATH, '//span[text()="One-way"]')
    one_way_button.click()


def select_airports():
    departure_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Leaving from"]')
    departure_button.click()

    departure_input = driver.find_element(By.CSS_SELECTOR, 'input[data-stid="origin_select-menu-input"]')
    departure_input.send_keys(departure_ad)

    dep_airport_button = driver.find_element(By.CSS_SELECTOR, 'li[data-index="0"]')
    dep_airport_button.click()

    sleep(2)

    arrival_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Going to"]')
    arrival_button.click()

    arrival_input = driver.find_element(By.CSS_SELECTOR, 'input[data-stid="destination_select-menu-input"]')
    arrival_input.send_keys(arrival_ad)

    arr_airport_button = driver.find_element(By.CSS_SELECTOR, 'li[data-index="0"]')
    arr_airport_button.click()


def select_date():
    date_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Date, "]')
    date_button.click()

    date_element = driver.find_element(By.CSS_SELECTOR, f'div[aria-label*="{date}"]')

    clickable_parent = date_element.find_element(By.XPATH, './..')
    actions.move_to_element(clickable_parent).perform()
    clickable_parent.click()

    done_button = driver.find_element(By.CSS_SELECTOR, 'button[data-stid="apply-date-selector"]')
    done_button.click()


def select_travelers():
    if no_of_travelers == '1':
        pass
    else:
        travelers_button = driver.find_element(By.CSS_SELECTOR, 'button[data-stid="open-room-picker"]')
        travelers_button.click()
        int_of_travelers = int(no_of_travelers)
        plus_button = driver.find_element(By.CSS_SELECTOR, 'svg[aria-label = "Increase the number of adults"]')
        for i in range(1, int_of_travelers):
            actions.move_to_element(plus_button).perform()
            plus_button.click()

        done_button = driver.find_element(By.ID, 'travelers_selector_done_button')
        actions.move_to_element(done_button)
        done_button.click()


def search_flights():
    search_button = driver.find_element(By.ID, 'search_button')
    search_button.click()


def show_all():
    while True:
        sleep(3)
        try:
            driver.find_element(By.CSS_SELECTOR, 'button[name="showMoreButton"]').click()
        except:
            break

def get_flight_info():
    flight_list = driver.find_elements(By.CSS_SELECTOR, 'li[data-test-id="offer-listing"]')
    for flight in flight_list:
        ticket_price = flight.find_element(By.CLASS_NAME, 'uitk-price-a11y').text
        flight_info['ticket_price'].append(ticket_price)

        duration = flight.find_element(By.CSS_SELECTOR, 'div[data-test-id="journey-duration"]').text
        flight_info['duration'].append(duration)

        try:
            stops = flight.find_element(By.CSS_SELECTOR, 'div[data-test-id="layovers"]').text
            flight_info['stops'].append(stops)
        except:
            flight_info['stops'].append('None')

        dep_arr_double = flight.find_element(By.CSS_SELECTOR, 'div[data-test-id="arrival-departure"]').text.split('-')
        flight_info['dep_ad'].append(dep_arr_double[0].strip())
        flight_info['arr_ad'].append(dep_arr_double[1].strip())

        airline = flight.find_element(By.CSS_SELECTOR, 'div[data-test-id="flight-operated"]').text
        flight_info['airline'].append(airline)

        times_double = flight.find_element(By.CSS_SELECTOR, 'span[data-test-id="departure-time"]').text.split('-')
        flight_info['dep_time'].append(times_double[0].strip())
        flight_info['arr_time'].append(times_double[1].strip())

        button_after = flight.find_element(By.CSS_SELECTOR, 'button[data-test-id="select-link"]')
        info = button_after.find_element(By.XPATH, 'preceding-sibling::div[1]').text
        flight_info['info'].append(info)


def get_the_data():
    df = pd.DataFrame(flight_info)
    df.to_csv('tickets.csv')
    df.to_excel('tickets.xlsx')
    df.to_json('tickets.json')


departure_ad = input('Leaving from: ')
arrival_ad = input('Going to: ')
date = input('Please enter date in this format: "January 1, 2024": ')
no_of_travelers = input('Enter the number of travelers (max: 6): ')

flight_info = {'ticket_price': [],
               'duration': [],
               'stops': [],
               'dep_ad': [],
               'arr_ad': [],
               'airline': [],
               'dep_time': [],
               'arr_time': [],
               'info': []
               }

options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15)
driver.get('https://www.expedia.com/')
actions = ActionChains(driver)

select_flights()
click_one_way()
select_airports()
select_date()
select_travelers()
search_flights()
show_all()
get_flight_info()
get_the_data()





