import tornado.ioloop
import tornado.web
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from time import sleep
import tornado.gen
from tornado.options import define, options

define("sleep_time", default=10, help="seconds to block each request")
define("workers", default=5, help="Number of max_workers to set for ThreadPoolExecutor")
define("port", default=8830, help="Port to expose server on")

class MainHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=options.workers)

    @run_on_executor
    def sleep_sleep(self, sleep_time):
        sleep(sleep_time)
        return sleep_time

    @tornado.gen.coroutine
    def get(self):
        self.write("hellao")
        sleep_time = yield self.sleep_sleep(options.sleep_time)
        self.write("Hello, world {}".format(sleep_time))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
