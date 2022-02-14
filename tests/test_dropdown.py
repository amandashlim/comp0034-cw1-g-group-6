from selenium.webdriver.support.ui import WebDriverWait
from dash.testing.application_runners import import_app


def test_crda001_H1_text_equals(dash_duo):
    app = import_app(app_file="app.crime_app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("H2", timeout=10)
    h1_text = dash_duo.find_element("#crime_select_text").text
    print(h1_text)
    assert h1_text.casefold() == "Select Crime to Display".casefold()
