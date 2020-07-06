from app import app

if __name__ == "__main__":
    app.run(debug=True)

'''
export FLASK_APP=run.py
export FLASK_ENV=development (by default the FLASK_ENV is production)
'''