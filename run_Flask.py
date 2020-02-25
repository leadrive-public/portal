import os
import application

app=application.create_app()

if __name__=="__main__":
    app.run("0.0.0.0", 8000, debug=True)
    pass
