import os
import pytest
from dash.testing.application_runners import import_app
from selenium.webdriver.chrome.options import Options
from app import visualization as v

v = v.all()


def setup_module():
    os.environ['no_proxy'] = 'localhost'


def pytest_setup_options():
    options = Options()
    # Uncomment the following if testing on GitHub actions, the browser needs to run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    return options


@pytest.fixture(scope='function')
def run_crime_app(dash_duo):
    app = import_app("app.crime_app")
    yield dash_duo.start_server(app)


@pytest.fixture(scope="module")
def reformat_columns():
    c = ['Borough', 'Date', 'Burglary', 'Criminal Damage', 'Drugs',
         'Fraud or Forgery', 'Other Notifiable Offences', 'Robbery',
         'Sexual Offences', 'Theft and Handling', 'Violence Against the Person',
         'Total Crime', 'Average Crime']
    yield c


@pytest.fixture(scope="module")
def borough_list():
    boroughs = ['Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley', 'Camden',
                'Croydon', 'Ealing', 'Enfield', 'Greenwich', 'Hackney',
                'Hammersmith and Fulham', 'Haringey', 'Harrow', 'Havering', 'Hillingdon',
                'Hounslow', 'Islington', 'Kensington and Chelsea', 'Kingston upon Thames',
                'Lambeth', 'Lewisham', 'Merton', 'Newham', 'Redbridge', 'Richmond upon Thames',
                'Southwark', 'Sutton', 'Tower Hamlets', 'Waltham Forest', 'Wandsworth',
                'Westminster']
    yield boroughs


@pytest.fixture(scope="module")
def crime_list():
    crimes = ['Burglary', 'Criminal Damage', 'Drugs',
              'Fraud or Forgery', 'Other Notifiable Offences', 'Robbery',
              'Sexual Offences', 'Theft and Handling', 'Violence Against the Person']
    yield crimes


@pytest.fixture(scope="module")
def date_list():
    dates = ['201910', '201911', '201912', '202001',
             '202002', '202003', '202004', '202005',
             '202006', '202007', '202008', '202009',
             '202010', '202011', '202012', '202101',
             '202102', '202103', '202104', '202105',
             '202106', '202107', '202108', '202109']
    yield dates


@pytest.fixture(scope="module")
def geo_borough_dict():
    a = {}
    for i in range(0, 32):
        a[v.geo['features'][i]['properties']['name']] = v.geo['features'][i]['properties']
    yield a
