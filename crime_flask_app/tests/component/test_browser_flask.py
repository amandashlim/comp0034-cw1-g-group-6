from time import sleep
import pytest
from selenium.webdriver.common.by import By
from flask_login import current_user

@pytest.mark.usefixtures('chrome_driver', 'run_app')
class Test1:
    def test_app_is_running(self):
        self.driver.get("http://127.0.0.1:5000/")
        assert self.driver.title == 'Home'

    def test_signup_succeeds(self):
        """
        Test that a user can create an account using the signup form if all fields are filled out correctly,
        and that they are redirected to the index page.
        """
        #Check if user is loged in
        # Go to the home page
        self.driver.get('http://127.0.0.1:5000/logout')
        self.driver.implicitly_wait(5)
        self.driver.get('http://127.0.0.1:5000/home')

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
        assert self.driver.current_url == 'http://127.0.0.1:5000/home'

        # Assert success message is flashed on the index page
        message = self.driver.find_element(By.ID, "success-flash").text
        assert "User created!" in message
        self.driver.get('http://127.0.0.1:5000/logout')
        self.driver.implicitly_wait(5)

    def test_signup_passwords_not_matching(self):
        """
        Test that a user can create an account using the signup form if all fields are filled out correctly,
        and that they are redirected to the index page.
        """
        # Go to the home page
        self.driver.get('http://127.0.0.1:5000/logout')
        self.driver.implicitly_wait(5)
        self.driver.get('http://127.0.0.1:5000/')

        # Click signup menu link
        # See https://www.selenium.dev/documentation/webdriver/waits/
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "nav-signup-btn").click()


        # Test person data
        email = "lana.kane@isis.com"
        username = "Monster Hands"
        password1 = "DangerZone"
        password2 = "Phraaaaaasing"

        # Fill in registration form
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password1").send_keys(password1)
        self.driver.find_element(By.ID, "password2").send_keys(password2)
        self.driver.find_element(By.ID, "btn-signup").click()

        # Assert that browser redirects to index page
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == 'http://127.0.0.1:5000/signup'

        # Assert success message is flashed on the index page
        message = self.driver.find_element(By.ID, "error-flash").text
        assert "Passwords don't match!" in message
        self.driver.get('http://127.0.0.1:5000/logout')
        self.driver.implicitly_wait(5)

    def test_login_succeeds(self):
        """
        Test that a user can create an account using the signup form if all fields are filled out correctly,
        and that they are redirected to the index page.
        """
        # Go to the home page
        self.driver.get('http://127.0.0.1:5000/logout')
        self.driver.implicitly_wait(5)
        self.driver.get('http://127.0.0.1:5000/home')

        # Click signup menu link
        # See https://www.selenium.dev/documentation/webdriver/waits/
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "nav-login-btn").click()

        # Test person data
        email = "pepe1@gmail.com"
        password = "123456"

        # Fill in registration form
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "btn-login").click()

        # Assert that browser redirects to index page
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == 'http://127.0.0.1:5000/home'

        # Assert success message is flashed on the index page
        message = self.driver.find_element(By.ID, "success-flash").text
        assert "Logged in!" in message
        self.driver.get('http://127.0.0.1:5000/logout')
        self.driver.implicitly_wait(5)

    def test_signup_errors(self, sign_up_list):
        """
        Test that a user can create an account using the signup form if all fields are filled out correctly,
        and that they are redirected to the index page.
        """
        # Go to the home page
        self.driver.get('http://127.0.0.1:5000/logout')
        self.driver.implicitly_wait(5)
        self.driver.get('http://127.0.0.1:5000/')

        # Click signup menu link
        # See https://www.selenium.dev/documentation/webdriver/waits/
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "nav-signup-btn").click()

        # Test person data
        for i in range(0, len(sign_up_list['email'])):
            print(i)
            email = sign_up_list['email'][i]
            username = sign_up_list['username'][i]
            password1 = sign_up_list['password1'][i]
            password2 = sign_up_list['password2'][i]

            # Fill in registration form
            self.driver.find_element(By.ID, "email").send_keys(email)
            self.driver.find_element(By.ID, "username").send_keys(username)
            self.driver.find_element(By.ID, "password1").send_keys(password1)
            self.driver.find_element(By.ID, "password2").send_keys(password2)
            self.driver.find_element(By.ID, "btn-signup").click()

            # Assert that browser redirects to index page
            self.driver.implicitly_wait(10)
            assert self.driver.current_url == 'http://127.0.0.1:5000/signup'

            # Assert success message is flashed on the index page
            message = self.driver.find_element(By.ID, "error-flash").text
            assert sign_up_list['error_messages'][i] in message
            self.driver.get('http://127.0.0.1:5000/logout')
            self.driver.implicitly_wait(5)

def document_initialised(driver):
    return driver.execute_script("return initialised")