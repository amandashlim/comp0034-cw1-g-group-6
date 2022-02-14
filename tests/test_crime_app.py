import time
from selenium.webdriver.common.keys import Keys
from dash.testing.application_runners import import_app
from app import visualization as v
v = v.all()


def test_main_header(dash_duo):
    '''
    GIVEN that the app is running
    WHEN we access the homepage of the app
    THEN there should be a main header
    '''
    app = import_app(app_file = "app.crime_app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("H2", timeout = 10)
    main_header = dash_duo.find_element("#main_header").text
    time.sleep(2)
    assert main_header == "Crime in London Overview Dashboard"


def test_selected_borough_on_map (dash_duo):
    '''
    Given that the app is running and the Map visual is selected
    When the user clicks on a borough
    Then the selections set should contain the selected borough
    '''
    app = import_app(app_file="app.crime_app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#visual_charts", timeout=15)

    dash_duo.click_at_coord_fractions("#visual_charts", 0.3, 0.3)
    dash_duo.click_at_coord_fractions("#visual_charts", 0.5, 0.5)
    dash_duo.click_at_coord_fractions("#visual_charts", 0.6, 0.6)
    time.sleep(5)
    a = dash_duo.find_element("#map_statistics")
    assert "Greenwich" == a.text[12:21]

def test_correct_statistics_for_selected_borough_time_crime (dash_duo):
    '''
    Given that the app is running and the Map visual is selected
    When the user clicks on multiple boroughs and selects a specific year and select a specific crime
    Then the statistics shown should be correct
    '''
    app = import_app(app_file="app.crime_app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#visual_charts", timeout=15)

    crime = dash_duo.find_element("#crime_select input")
    crime.send_keys("Sexual")
    crime.send_keys(Keys.RETURN)
    time.sleep(3)
    dash_duo.click_at_coord_fractions("#visual_charts", 0.3, 0.3)
    dash_duo.click_at_coord_fractions("#visual_charts", 0.5, 0.5)
    #dash_duo.click_at_coord_fractions("#visual_charts", 0.6, 0.6)
    time.sleep(3)
    dash_duo.click_at_coord_fractions("#map_slider",0.5,0.5)
    time.sleep(5)
    a = dash_duo.find_element("#map_statistics")
    assert "+39.29%" in a.text










