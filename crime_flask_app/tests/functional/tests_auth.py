from crime_flask_app import create_app
def test_logout_redirect(client):
    response = client.get("/logout")
    assert len(response.history) == 1
    assert response.request.path == "/home"