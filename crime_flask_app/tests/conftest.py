import pytest
from crime_flask_app.models import User, Post, Comment
from crime_flask_app import create_app, db, config


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
