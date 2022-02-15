from app import visualization as v

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


def test_reformating_columns():
    '''
    Given the class is called
    When reformat function is used
    Then the function should return the data with specific columns
    '''

    c = ['Borough', 'Date', 'Burglary', 'Criminal Damage', 'Drugs',
         'Fraud or Forgery', 'Other Notifiable Offences', 'Robbery',
         'Sexual Offences', 'Theft and Handling', 'Violence Against the Person',
         'Total Crime', 'Average Crime']
    assert list(v.reformat(v.df).columns) == c


def test_crime_list():
    '''
    Given the class is called
    When the class is called
    Then the function should return the list of crimes
    '''

    crimes = ['Burglary', 'Criminal Damage', 'Drugs',
              'Fraud or Forgery', 'Other Notifiable Offences', 'Robbery',
              'Sexual Offences', 'Theft and Handling', 'Violence Against the Person']
    assert list(v.crime_list) == crimes


def test_borough_list():
    '''
    Given the class is called
    When the class is called
    Then the function should return the list of boroughs
    '''

    boroughs = ['Barking and Dagenham', 'Barnet', 'Bexley', 'Brent', 'Bromley', 'Camden',
                'Croydon', 'Ealing', 'Enfield', 'Greenwich', 'Hackney',
                'Hammersmith and Fulham', 'Haringey', 'Harrow', 'Havering', 'Hillingdon',
                'Hounslow', 'Islington', 'Kensington and Chelsea', 'Kingston upon Thames',
                'Lambeth', 'Lewisham', 'Merton', 'Newham', 'Redbridge', 'Richmond upon Thames',
                'Southwark', 'Sutton', 'Tower Hamlets', 'Waltham Forest', 'Wandsworth',
                'Westminster']
    assert list(v.borough_list) == boroughs


def test_date_list():
    '''
    Given the class is called
    Whem the class is called
    Then the function should return the list of dates
    '''

    dates = ['201910', '201911', '201912', '202001',
             '202002', '202003', '202004', '202005',
             '202006', '202007', '202008', '202009',
             '202010', '202011', '202012', '202101',
             '202102', '202103', '202104', '202105',
             '202106', '202107', '202108', '202109']
    assert list(v.date_list) == dates


def test_get_highlights():
    '''
    Given the class is called
    When the selections are passed into get_highlights
    Then the function should return the geojson file for those selections (boroughs)
    '''

    subgeo = v.geo['features'][25]['properties']
    assert v.get_highlights(["Camden"])['features'][0]['properties'] == subgeo


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


