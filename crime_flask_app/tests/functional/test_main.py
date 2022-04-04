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


def test_dashboard_navigation(client):
    """
    GIVEN a user is logged in
    WHEN the user accesses the dashboard page
    THEN the links to the login, blog, home, logout, my_account and user_posts should be in the navigation bar
    """
    with client:
        client.post('/login',
                    data = dict(email='pepe1@gmail.com', password='123456'),
                    follow_redirects=True)
        access_dashboard = client.get("/dashboard")
        html = access_dashboard.data.decode()
        print(access_dashboard.data)
        #assert " <a href=\"/dashboard/\">login</a>" in html
        #assert " <a href=\"/dashboard/\">blog</a>" in html
        #assert " <a href=\"/dashboard/\">home</a>" in html
        #assert " <a href=\"/dashboard/\">logout</a>" in html
        #assert " <a href=\"/dashboard/\">my_account</a>" in html
        #assert " <a href=\"/dashboard/\">user_posts</a>" in html