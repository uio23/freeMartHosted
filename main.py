from freemart import create_app


app, socket = create_app()

if __name__ == '__main__':
    app.run()
