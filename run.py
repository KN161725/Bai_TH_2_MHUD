from flask import Flask
import route
app=Flask(__name__)

route.set_route(app)
app.secret_key=route.secret_key(58)
if __name__=="__main__":
    app.run(debug=True)

