from flask import Flask

app=Flask(__name__)
import route
route.set_route(app)
if __name__=="__main__":
    app.secret_key=route.secret_key(58)
    app.run(debug=True)

