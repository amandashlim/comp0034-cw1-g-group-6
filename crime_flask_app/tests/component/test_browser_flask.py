import pytest

@pytest.mark.usefixtures('chrome_driver', 'run_app')
class TestMyAppBrowser:
    def test_app_is_running(self):
        self.driver.get("http://127.0.0.1:5000/")
        assert self.driver.title == 'Home page'