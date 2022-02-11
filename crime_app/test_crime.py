from dash.testing.application_runners import import_app
from selenium.webdriver.support.ui import WebDriverWait

# Change to test_"2 digits of module""2 digits of file"001_"what the test is doing"

def test_crda001_H1_text_equals(dash_duo):
    """GIVEN that the app is running
    WHEN we access the homepage of the app
    THEN the H1 heading should say "London Crime Rates"""

    app = import_app(app_file = "crime_app.dash_app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("H1", timeout = 4)
    h1_text = dash_duo.find_element("H1").text
    assert h1_text.casefold() == "London Crime Rate Dashboard".casefold()


def test_crda002_show_settings(dash_duo):
    """GIVEN that the app is running
    WHEN we access the homepage of the app
    THEN there should be a paragraph with Select Chart Type
    """

    app = import_app(app_file = "crime_app.dash_app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("H1", timeout = 4)
    filter_selector = dash_duo.find_element("H3").text
    assert filter_selector.casefold() == "Display Settings".casefold()

def test_crda003_default_crime(dash_duo):
    """GIVEN that you launch the app and you land on the homepage
    WHEN look at the Select Crime to Display filter
    THEN the default crime should be Burglary"""

    app = import_app(app_file="crime_app.dash_app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("H1", timeout=4)
    WebDriverWait(dash_duo.driver, 3)
    default_crime = dash_duo.find_element(By.XPATH, "/html/body/div/div/div/div[3]/div[1]/div/div/div[2]/div[1]/div[3]/div/div/div/div[1]").text
    assert default_crime.text() == 'Burglary'.text()








