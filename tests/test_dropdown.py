from selenium.webdriver.support.ui import WebDriverWait

def test_default_map(dash_duo):
    dash_duo.wait_for_element("h1", timeout=4)
    WebDriverWait(dash_duo.driver, 3)
    assert 'Display Settings' in dash_duo.find_element("display_settings").text
