from curses import window
from dash.testing.application_runners import import_app
from selenium.webdriver.support.ui import WebDriverWait

# Change to test_"2 digits of module""2 digits of file"001_"what the test is doing"

def test_crcr001_H1_text_equals(dash_duo):
    """GIVEN that the app is running
    WHEN we access the homepage of the app
    THEN the H1 heading should say "Crime rates in London boroughs"""

    app = import_app(app_file = "crime_app.app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout = 4)
    h1_text = dash_duo.find_element("h1").text
    assert h1_text.casefold() == "Crime rates in London boroughs"


def test_crcr002_open_preview(dash_duo):
    """GIVEN that the homepage is open
    WHEN we click on a preview of a figure
    THEN the figure is opened on a seperate webpage"""

    app = import_app(app_file = "crime_app.app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("figure 1", timeout = 4)   # See what figure ID is after 
    button = dash_duo.find_element_by_id("ADD THE ID NB")
    action = button.click() 
    result = open

