from pyactor.context import set_context, create_host, serve_forever


if __name__ == "__main__":
    set_context()
    host = create_host('http://127.0.0.1:1274/')
    print "Host listening on port 1274"
    serve_forever()
