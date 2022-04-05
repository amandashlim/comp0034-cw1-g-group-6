#
# import time
# from selenium.webdriver.common.keys import Keys
# from crime_dash_app import visualization as v
#
# v = v.all()
#
# # General App tests
#
# def test_tete001_main_header(dash_duo, run_crime_app):
#     '''
#     GIVEN that the crime_dash_app is running
#     WHEN we access the homepage of the crime_dash_app
#     THEN there should be a main header
#     '''
#
#     dash_duo.wait_for_element("H2", timeout = 10)
#     main_header = dash_duo.find_element("#main_header").text
#     time.sleep(2)
#     assert main_header == "Crime in London Overview Dashboard"
#
# def test_tete002_selected_data (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running
#     When we select a specific dataset (Population 2011)
#     Then the default visualization should update (we check with unique legend values)
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     dash_duo.click_at_coord_fractions("#data_select", 0.4, 0.5)
#     time.sleep(5)
#
#     a = dash_duo.find_element("#map")
#     assert "0.1\n0.2\n0.3\n0.4\n0.5\nDrugs" in a.text
#
# def test_tete003_selected_chart_type (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running
#     When the user selects a particular chart type
#     Then only the correct chart should appear
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     crime = dash_duo.find_element("#chart_select input")
#     crime.send_keys("Line")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#
#     map = dash_duo.find_element("#map_row")
#     hist = dash_duo.find_element("#hist_row")
#     line = dash_duo.find_element("#line_row")
#     assert map.text == "" and hist.text == "" and "Line Chart" in line.text
#
# # Map specific tests
#
# def test_tete004_selected_borough_on_map (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running and the Map visual is selected
#     When the user clicks on a borough
#     Then the selections set should contain the selected borough
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     crime = dash_duo.find_element("#chart_select input")
#     crime.send_keys("Map")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#
#     dash_duo.click_at_coord_fractions("#visual_charts", 0.6, 0.5)
#     time.sleep(5)
#     a = dash_duo.find_element("#map_statistics")
#     assert "Newham" == a.text[12:18]
#
# def test_tete005_selected_crime_on_map (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running and the Map visual is selected
#     When the user select a particular crime
#     Then the map will show the correct crime (we check that by checking the legend)
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     crime = dash_duo.find_element("#chart_select input")
#     crime.send_keys("Map")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#
#     crime = dash_duo.find_element("#crime_select input")
#     crime.send_keys("Robbery")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#
#     a = dash_duo.find_element("#map")
#     assert "Robbery" in a.text
#
# def test_tete006_selected_month_on_map (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running and the Map visual is selected
#     When the user select a particular month
#     Then the map will show the correct values for that month (we check that by checking the legend)
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     crime = dash_duo.find_element("#chart_select input")
#     crime.send_keys("Map")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#
#     dash_duo.click_at_coord_fractions("#map_slider", 0.8, 0.3)
#     time.sleep(5)
#
#     a = dash_duo.find_element("#map")
#     assert "20\n30\n40\n50\n60\n70\nDrugs" in a.text
#
# def test_tete007_correct_statistics_for_selected_borough_time_crime (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running and the Map visual is selected
#     When the user clicks on multiple boroughs and selects a specific year and select a specific crime
#     Then the statistics shown should be correct
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     crime = dash_duo.find_element("#chart_select input")
#     crime.send_keys("Map")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#
#     crime = dash_duo.find_element("#crime_select input")
#     crime.send_keys("Sexual")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#     dash_duo.click_at_coord_fractions("#visual_charts", 0.3, 0.3)
#     dash_duo.click_at_coord_fractions("#visual_charts", 0.5, 0.5)
#     time.sleep(3)
#     dash_duo.click_at_coord_fractions("#map_slider",0.5,0.5)
#     time.sleep(5)
#     a = dash_duo.find_element("#map_statistics")
#     assert "+39.29%" in a.text
#
# # Line specific tests
#
# def test_tete008_selected_boroughs_on_line (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running and the Line visual is selected
#     When the user selects multiple boroughs
#     Then the line will show lines with forecasts for those boroughs (we check that by checking the legend)
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     crime = dash_duo.find_element("#chart_select input")
#     crime.send_keys("Line")
#     crime.send_keys(Keys.RETURN)
#
#     crime = dash_duo.find_element("#hist_checklist input")
#     crime.send_keys("West")
#     crime.send_keys(Keys.RETURN)
#     crime.send_keys("Brent")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#
#     a = dash_duo.find_element("#line")
#     assert "Camden" and "Brent" and "Westminster" in a.text
#
# def test_tete009_selected_crime_on_line_chart (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running and the Line visual is selected
#     When the user selects a particular crime
#     Then the line will show the appropriate crime (we check that by checking the legend)
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     crime = dash_duo.find_element("#chart_select input")
#     crime.send_keys("Line")
#     crime.send_keys(Keys.RETURN)
#
#     crime = dash_duo.find_element("#crime_select input")
#     crime.send_keys("Theft")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#
#     a = dash_duo.find_element("#line")
#     assert "Average Theft and Handling Crimes".casefold() in a.text.casefold()
#
# def test_tete010_selected_crime_on_line_stats (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running and the Line visual is selected
#     When the user selects a particular crime
#     Then the line statistics will show the appropriate crime
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     crime = dash_duo.find_element("#chart_select input")
#     crime.send_keys("Line")
#     crime.send_keys(Keys.RETURN)
#
#     crime = dash_duo.find_element("#crime_select input")
#     crime.send_keys("Burglary")
#     crime.send_keys(Keys.RETURN)
#     time.sleep(3)
#
#     a = dash_duo.find_element("#line_statistics")
#     assert "Highest Average Burglary Rate".casefold() \
#            and "Lowest Recorded Burglary Rate".casefold() in a.text.casefold()
#
# def test_tete011_selected_crime_on_line_chart (dash_duo, run_crime_app):
#     '''
#     Given that the crime_dash_app is running and the Line visual is selected
#     When the user selects a particular dataset (Population 2011)
#     Then the line statistics should show the correct boroughs
#     '''
#
#     dash_duo.wait_for_element("#visual_charts", timeout=15)
#
#     crime = dash_duo.find_element("#chart_select input")
#     crime.send_keys("Line")
#     crime.send_keys(Keys.RETURN)
#
#     dash_duo.click_at_coord_fractions("#data_select", 0.4, 0.5)
#     time.sleep(3)
#
#     a = dash_duo.find_element("#line_statistics")
#     assert "Westminster, with rate: 0.453".casefold() in a.text.casefold()
#
#
#
#
#
