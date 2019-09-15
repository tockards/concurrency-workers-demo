from tornado.httpclient import AsyncHTTPClient
from tornado import gen
from tornado import ioloop
import functools
import time

@gen.coroutine
def async_fetch_gen(url):
    print ("started {}".format(time.time()))
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    print ("ended {}".format(time.time()))
    raise gen.Return(response.body)


if __name__ == '__main__':
    mk_req = functools.partial(async_fetch_gen, 'http://localhost:8080/backend')
    io_loop = ioloop.IOLoop.current()
    for i in range(100):
        io_loop.add_callback(mk_req)
    io_loop.start()
