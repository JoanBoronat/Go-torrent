from pyactor.context import set_context, create_host, serve_forever


if __name__ == "__main__":
    set_context()
    port = '1277'
    host = create_host('http://127.0.0.1:' + port + '/')
    print "Host listening on port", port
    serve_forever()
