from crime_flask_app import create_app

m_app = create_app()


if __name__ == '__main__':
    m_app.run(debug=True)


