from http.server import BaseHTTPRequestHandler, HTTPServer
from pydantic import ValidationError
from order import Order
import subprocess


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_len = int(self.headers.get('Content-Length'))
            order = Order.parse_raw(self.rfile.read(content_len))
            order.order_number = gen_order_number()
        except ValidationError as e:
            pass  # send bad response
        else:
            call_bot(order)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # self.wfile.write(json.dumps({'status': True}).encode())
        return


# todo fix it
def call_bot(order: Order):
    args = f'--coffee_house_id="{data["coffee_house_id"]}" '
    args += f'--order_content="{data["order_content"]}" '
    args += f'--time="{data["time"]}" '
    args += f'--order_number={data["order_number"]} '
    if 'mail' in data:
        args += f'--mail="{data["mail"]}" '
    if 'phone_number' in data:
        args += f'--phone_number="{data["phone_number"]}" '

    subprocess.Popen(f'python bot_waiter.py ' + args)


def gen_order_number() -> int:
    return 0


server_address = ('', 8000)
httpd = HTTPServer(server_address, MyHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.server_close()
