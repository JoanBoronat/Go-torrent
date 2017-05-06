from pyactor.context import set_context, create_host, serve_forever


if __name__ == "__main__":
    set_context()
    host = create_host('http://127.0.0.1:1276/')
    serve_forever()
