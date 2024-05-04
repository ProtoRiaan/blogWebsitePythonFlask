

from flaskblog import create_app
from dotenv import load_dotenv

load_dotenv()


app = create_app()
app.config['SECRET_KEY'] = 'e9dceceade0fd5391b936a3e849595f8'

if __name__ == '__main__':
    app.run(host="0.0.0.0")
    

