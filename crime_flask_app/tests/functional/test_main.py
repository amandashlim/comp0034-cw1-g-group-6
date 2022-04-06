def test_index_page_valid(test_client):
    """
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (HTTP GET request)
    THEN a success response code (200) is received ()
    """
    response = test_client.get("/")
    assert response.status_code == 200


def test_no_login_page_valid(test_client, app_paths_no_login):
    """
    GIVEN a Flask application is running and user is not logged in
    WHEN pages that dont require login are requested (HTTP GET request)
    THEN a success response code (200) is received ()
    """
    for i in app_paths_no_login:
        response = test_client.get(i)
        assert response.status_code == 200


def test_no_login_page_invalid(test_client, app_paths_login):
    """
    GIVEN a Flask application is running and user is not logged in
    WHEN pages that require login are requested (HTTP GET request)
    THEN a redirect response code (302) or permanent redirect response (308) is received ()
    """
    for i in app_paths_login:
        response = test_client.get(i)
        assert response.status_code in [302,308]


def test_dashboard_dash_render(client):
    """
    GIVEN a user is logged in
    WHEN the user accesses the dashboard page
    THEN the webpage should display the render of the dash app
    """
    with client:
        client.post('/login',
                    data = dict(email='pepe1@gmail.com', password='123456'),
                    follow_redirects=True)
        access_dashboard = client.get("/dashboard/")
        html = access_dashboard.data.decode()
        assert '<script id="_dash-renderer" type="application/javascript">var renderer = new DashRenderer();</script>' in html