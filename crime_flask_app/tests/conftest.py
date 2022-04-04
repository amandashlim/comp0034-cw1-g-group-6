import multiprocessing

import pytest
from selenium.webdriver import Chrome, ChromeOptions

from crime_flask_app import create_app, db
from crime_flask_app.models import User, Post


@pytest.fixture(scope='session')
def app():
    app = create_app()
    yield app

@pytest.fixture(scope='session')
def setUp():
    db.create_all()
    db.session.add(User(email="admin@admin.com",username="admin",password='admin'))
    db.session.add(Post(title="Admin Test Post Title",text="Admin Test Post Text",author='admin'))
    db.session.commit()


@pytest.fixture(scope='session')
def test_client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def app_paths_no_login():
    app_paths = ["/","/home","/login","/signup"]
    yield app_paths


@pytest.fixture()
def app_paths_login(username="pepe1"):
    app_paths = ["/dashboard","/blog","/create_post",f"/{username}",f"posts/{username}"]
    yield app_paths


@pytest.fixture(scope='class')
def chrome_driver(request):
    """ Selenium webdriver with options to support running in GitHub actions
    Note:
        For CI: `headless` and `disable-gpu` not commented out
        For running on your computer: `headless` and `disable-gpu` to be commented out
    """
    options = ChromeOptions()
    options.add_argument("--headless")  # use for GitHub Actions CI
    options.add_argument('--disable-gpu') # use for GitHub Actions CI
    options.add_argument("--window-size=1920,1080")
    chrome_driver = Chrome(options=options)
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()


@pytest.fixture(scope='class')
def run_app(app):
    """
    Fixture to run the Flask app for Selenium browser tests
    """
    multiprocessing.set_start_method("fork")  # Needed in Python 3.8 and later
    process = multiprocessing.Process(target=app.run, args=())
    process.start()
    yield process
    process.terminate()


@pytest.fixture()
def sign_up_list():
    credential_dict = {'email':["pepe1@gmail.com","povey.grovey@hotmail.com",
                                "damn_crackers@ritz.salt","channel5newsbaby@awesome.yt",
                                "bReXiT_wAs_gOoD@dumb.ville"],
                       'username':["peperonicoli","pepe1","iTs_a_sLuR","5","BadKindOfBJ"],
                       "password1":["123456","235346","cracker","AMURICA","BJ"],
                       "password2":["123456","235346","saltine","AMURICA","BJ"],
                       "error_messages":['Email is already in use.',"Username is already in use.",
                                         "Passwords don\'t match!","Username is too short.",
                                         "Password is too short."]}
    yield credential_dict
'''
@pytest.fixture(scope='session')
def db(app):
    """
    Return a session wide database using a Flask-SQLAlchemy database connection.
    """
    with app.app_context():
        db.app = app
        db.create_all()
    yield db
    db.drop_all()


# https://docs.pytest.org/en/latest/how-to/fixtures.html#autouse-fixtures-fixtures-you-don-t-have-to-request
@pytest.fixture(scope='function', autouse=True)
def session(db, app):
    """ Roll back database changes at the end of each test """
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        options = dict(bind=connection, binds={})
        sess = db.create_scoped_session(options=options)
        db.session = sess
        yield sess
        sess.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope='module')
def user_details():
    user_details = {
        'first_name': 'Amelie',
        'last_name': 'Martin',
        'password_text': 'Metpolice1',
        'email': 'ameliemartin@email.com'
    }
    yield user_details
'''

'''
@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client
'''
