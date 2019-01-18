from queue import Queue


class OrderHandler:

    orders = Queue()
    current_order = None

    def __init__(self, on_new_order):
        self.on_new_order = on_new_order

    def get_open_orders(self):
        pass
        # orders = request orders from db sortBy("created_at")
        # self.orders.put_nowait()
        # if orders is not None:
        # self.get_next_order()

    def add_order(self, order):
        self.orders.put_nowait(order)
        if self.current_order is None:
            self.get_next_order()

    def get_next_order(self):
        self.current_order = self.orders.get_nowait()
        self.on_new_order()
