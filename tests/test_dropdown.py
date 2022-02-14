from selenium.webdriver.support.ui import WebDriverWait
from dash.testing.application_runners import import_app

def test_default_map(dash_duo):
    app = import_app("crime_app.crime_app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("display_settings", timeout=60)
    WebDriverWait(dash_duo.driver, 3)
    assert 'Display Settings' in dash_duo.find_element("display_settings").text
