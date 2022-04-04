from time import sleep
import pytest
from selenium.webdriver.common.by import By

@pytest.mark.usefixtures('chrome_driver', 'run_app')
class TestMyAppBrowser:
    def test_app_is_running(self):
        self.driver.get("http://127.0.0.1:5000/")
        assert self.driver.title == 'Home'

    def test_signup_succeeds(self):
        """
        Test that a user can create an account using the signup form if all fields are filled out correctly,
        and that they are redirected to the index page.
        """
        # Go to the home page
        self.driver.get('http://127.0.0.1:5000/')

        # Click signup menu link
        # See https://www.selenium.dev/documentation/webdriver/waits/
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "nav-signup-btn").click()

        # Test person data
        email = "sterling.archer@isis.com"
        username = "The Duchess"
        password1 = "DangerZone"
        password2 = "DangerZone"

        # Fill in registration form
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password1").send_keys(password1)
        self.driver.find_element(By.ID, "password2").send_keys(password2)
        self.driver.find_element(By.ID, "btn-signup").click()

        # Assert that browser redirects to index page
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == 'http://127.0.0.1:5000/'

        # Assert success message is flashed on the index page
        message = self.driver.find_element(By.ID, "success-flash").text
        assert f"User created!" in message


def document_initialised(driver):
    return driver.execute_script("return initialised")