from queue import Queue
import psycopg2


class OrderHandler:

    orders = Queue()
    current_order = None

    def __init__(self, on_new_order):
        self.on_new_order = on_new_order
        self.conn = psycopg2.connect(dbname="wrapper_development", host="localhost", port=5432)
        # self.conn = psycopg2.connect("dbname=wrapper_production user=wrapper")
        self.cur = self.conn.cursor()

    def get_open_orders(self):
        self.cur.execute("SELECT * FROM orders WHERE order_status_id = 2 ORDER BY created_at ASC")
        for order in self.cur.fetchall():
            self.orders.put_nowait(order)

        self.cur.execute("SELECT * FROM orders WHERE order_status_id = 1 ORDER BY created_at ASC")
        for order in self.cur.fetchall():
            self.orders.put_nowait(order)

        if not self.orders.empty():
            self.get_next_order()

    def add_order(self, order):
        self.orders.put_nowait(order)
        if self.current_order is None:
            self.get_next_order()

    def get_next_order(self):
        current_order_id = str(self.current_order[0])
        if self.current_order is not None:
            self.cur.execute("UPDATE orders SET order_status_id = 3 WHERE id = %s ;", str(current_order_id))
        self.current_order = self.orders.get_nowait()
        current_order_id = str(self.current_order[0])
        self.cur.execute("UPDATE orders SET order_status_id = 2 WHERE id = %s ;", str(current_order_id))
        self.conn.commit()
        self.on_new_order()
