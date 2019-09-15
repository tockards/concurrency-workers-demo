import tornado.ioloop
import tornado.web
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from time import sleep
import tornado.gen

class MainHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=10)

    @run_on_executor
    def sleep_sleep(self, sleep_time):
        sleep(sleep_time)
        return sleep_time

    @tornado.gen.coroutine
    def get(self):
        self.write("hellao")
        sleep_time = yield self.sleep_sleep(10)
        self.write("Hello, world {}".format(sleep_time))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
