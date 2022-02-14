import pytest
from dash.testing.application_runners import import_app
from selenium.webdriver.chrome.options import Options


def pytest_setup_options():
    options = Options()
    # Uncomment the following if testing on GitHub actions, the browser needs to run in headless mode
    options.add_argument('--disable-gpu')
    #options.add_argument('--headless')
    return options
'''
@pytest.fixture(scope='function')
def run_crime_app(dash_duo):
    app = import_app("app.crime_app")
    yield dash_duo.start_server(app)
'''