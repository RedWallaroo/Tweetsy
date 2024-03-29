from flask import Flask

app = Flask(__name__)
from app import views

if __name__=='__main__':
	#bind to port if defined, otherwise default
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)