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

    def test_new_user_path(self):
        """
        Test when a new user: opens the website it loads correctly,
                            signs up successfully,
                            opens the dashapp and looks at the line chart,
                            and posts a new blog post asking a question
        """
        # Go to the home page
        self.driver.get('http://127.0.0.1:5000/')

        # Click signup menu link
        # See https://www.selenium.dev/documentation/webdriver/waits/
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "nav-signup-btn").click()

        # Test person data
        email = "new.user@noob.ua"
        username = "im a noob"
        password1 = "qwerty"
        password2 = "qwerty"

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

        # Open the dashboard page
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "nav-dashboard-btn").click()
        assert self.driver.current_url == 'http://127.0.0.1:5000/dashboard/'

        # Test if map is showing
        self.driver.implicitly_wait(5)
        map_row = self.driver.find_element(By.ID, "map_row").text
        assert "Map" in map_row

        # Click on blog page
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "dash_nav-blog-btn").click()
        assert self.driver.current_url == 'http://127.0.0.1:5000/blog'

        # Click on Create a new post
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "create_post-btn").click()
        assert self.driver.current_url == 'http://127.0.0.1:5000/create_post'

        # Write a title and content
        self.driver.implicitly_wait(5)
        title = "This is a post title"
        content = "This is the content"
        self.driver.find_element(By.ID, "title").send_keys(title)
        self.driver.find_element(By.ID, "text").send_keys(content)
        self.driver.find_element(By.ID, "post-btn").click()

        # Check if the post is created
        message = self.driver.find_element(By.ID, "success-flash").text
        assert "Post Created" in message

        # Press the back button
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "back-btn").click()
        assert self.driver.current_url == 'http://127.0.0.1:5000/blog'

        # Check if the post is showing up
        posts = self.driver.find_element(By.ID, "posts").text
        assert "im a noob" in posts

        self.driver.get('http://127.0.0.1:5000/logout')
        self.driver.implicitly_wait(5)

    def test_existing_user_edit_post(self):
        """
        Test when an existing user: opens the website it loads correctly,
                           loges in successfully,
                           views his post
                           edits his post successfully
        """
        # Go to the home page
        self.driver.get('http://127.0.0.1:5000/')

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

        # Goto user blog page
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "my_post-btn").click()
        assert self.driver.current_url == 'http://127.0.0.1:5000/posts/pepe1'

        # Click edit post
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "post_dropdown-btn").click
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "edit-btn").click()
        assert self.driver.current_url == 'http://127.0.0.1:5000/edit-post/1'

        # Edit the post
        edit_title = "Pepe Edited a post"
        edit_text = "Pepe is editing babyyy"
        self.driver.find_element(By.ID, "title").send_keys(edit_title)
        self.driver.find_element(By.ID, "text").send_keys(edit_text)
        self.driver.find_element(By.ID, "edit_submit-btn").click()
        message = self.driver.find_element(By.ID, "success-flash").text
        assert "Post successfully updated" in message

        # Goto user posts and check if the post was edited
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "my_post-btn").click()
        post_title = self.driver.find_element(By.ID, "post_1_title").text
        post_text = self.driver.find_element(By.ID, "post_1_text").text
        assert edit_title in post_title
        assert edit_text in post_text


        self.driver.get('http://127.0.0.1:5000/logout')
        self.driver.implicitly_wait(5)


def document_initialised(driver):
    return driver.execute_script("return initialised")