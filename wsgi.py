import json
from pydantic import ValidationError
from SendingOrderBot import SendingOrderBot
from order import Order

count_orders = 0


def app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_data = environ['wsgi.input'].read(request_body_size)
        response_headers, status, response_data = do_post(request_data)
    else:
        response_data = b'Invalid request type'
        status = '400 Bad Request'
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(response_data)))
        ]

    start_response(status, response_headers)
    return iter([response_data])


def do_post(request_data: str) -> tuple:
    try:
        order = Order.parse_raw(request_data)
        order.order_number = gen_order_number()
    except ValidationError as e:
        response_data = bytes(str(e), encoding='utf-8')
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(response_data)))
        ]
        status = '400 Bad Request'
    else:
        call_bot(order)

        response_data = bytes(f'order_number: {order.order_number}', encoding='utf-8')
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(response_data)))
        ]
        status = '200 OK'

    return response_headers, status, response_data

# todo change this
def gen_order_number() -> int:
    global count_orders
    count_orders += 1
    return count_orders


def call_bot(order: Order) -> None:
    # subprocess.Popen(f"python test.py --order='{order.json(exclude_none=True)}'")  thinkit
    # thinkit сдалать это на потоках
    bot = SendingOrderBot(order)
    bot.send_message()
