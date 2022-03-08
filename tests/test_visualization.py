from crime_dash_app import visualization as v

v = v.all()


def test_imported_data():
    '''
    Given all class is called
    When the class is called
    Then the class should get the data automatically
    '''

    assert v.df.shape == (288, 26)


def test_reformating_shape():
    '''
    Given the class is called
    When reformat function is used
    Then the function should return the correct datashape
    '''

    assert v.reformat(v.df).shape == (768, 13)


def test_reformating_columns(reformat_columns):
    '''
    Given the class is called
    When reformat function is used
    Then the function should return the data with specific columns
    '''

    assert list(v.reformat(v.df).columns) == reformat_columns


def test_crime_list(crime_list):
    '''
    Given the class is called
    When the class is called
    Then the function should return the list of crimes
    '''

    assert list(v.crime_list) == crime_list


def test_borough_list(borough_list):
    '''
    Given the class is called
    When the class is called
    Then the function should return the list of boroughs
    '''

    assert list(v.borough_list) == borough_list


def test_date_list(date_list):
    '''
    Given the class is called
    Whem the class is called
    Then the function should return the list of dates
    '''

    assert list(v.date_list) == date_list


def test_get_highlights(borough_list, geo_borough_dict):
    '''
    Given the class is called
    When the selections are passed into get_highlights
    Then the function should return the geojson file for those selections (boroughs)
    '''
    for i in borough_list:
        subgeo = geo_borough_dict[i]
        assert v.get_highlights([i])['features'][0]['properties'] == subgeo


def test_map_statistics():
    '''
    Given the class is called
    When the statistics_map function is called
    Then the function should return the correct number
    '''

    m = v.statistics_map(df=v.df_r, month="202101",
                         selected_areas=["Camden"],
                         crime="Robbery", m=1)
    mmm = v.statistics_map(df=v.df_r, month="202101",
                           selected_areas=["Brent"],
                           crime="Robbery", mmm=1)
    y = v.statistics_map(df=v.df_r, month="202101",
                         selected_areas=["Camden"],
                         crime="Drugs", y=1)
    assert -27.78 == round(m["Camden"] * 100, 2) and \
           -23.73 == round(mmm["Brent"] * 100, 2) and \
           -23.67 == round(y["Camden"] * 100, 2)


