import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pydantic import ValidationError

from SendingOrderBot import SendingOrderBot
from order import Order
import subprocess


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_len = int(self.headers.get('Content-Length'))
            order = Order.parse_raw(self.rfile.read(content_len))
            order.order_number = gen_order_number()
        except ValidationError as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'msg': str(e)}).encode())
        else:
            call_bot(order)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode())
        return


def call_bot(order: Order) -> None:
    # subprocess.Popen(f"python test.py --order='{order.json(exclude_none=True)}'")  thinkit
    # thinkit сдалать это на потоках
    bot = SendingOrderBot(order)
    bot.send_message()


def gen_order_number() -> int:
    return 0


server_address = ('', 8000)
httpd = HTTPServer(server_address, MyHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()
