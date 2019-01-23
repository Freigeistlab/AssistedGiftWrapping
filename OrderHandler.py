from queue import Queue
import psycopg2


class OrderHandler:

    orders = Queue()
    current_order_items = None
    current_order = None

    def __init__(self, on_new_order):
        self.on_new_order = on_new_order
        self.conn = psycopg2.connect(dbname="wrapper_development", host="localhost", port=5432)
        # self.conn = psycopg2.connect("dbname=wrapper_production user=wrapper")
        self.cur = self.conn.cursor()
        self.get_table_names()

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
        if self.current_order is not None:
            current_order_id = str(self.current_order[0])
            self.cur.execute("UPDATE orders SET order_status_id = 3 WHERE id = %s ;", str(current_order_id))
            self.conn.commit()
        if not self.orders.empty():
            self.current_order = self.orders.get_nowait()
            order_item_ids = ["1","2","3","4"]

            # order_item_ids = self.current_order["orderProducts"]
            order_item_ids_str = ",".join(order_item_ids)
            #  WHERE id in (%s);" % order_item_ids_str
            current_order_items = {}
            self.cur.execute("SELECT p.name, p.image, pg.id, pg.name FROM products AS p, product_groups AS pg WHERE p.id in (%s) AND p.product_group_id = pg.id;" % order_item_ids_str)

            # add new product groups here
            for item in self.cur.fetchall():
                if item[2] == 1:
                    current_order_items["packaging_style"] = item
                elif item[2] == 2:
                    current_order_items["paper"] = item
                elif item[2] == 3:
                    current_order_items["band"] = item
                elif item[2] == 4:
                    current_order_items["card"] = item

            self.current_order_items = current_order_items

            current_order_id = str(self.current_order[0])
            self.cur.execute("UPDATE orders SET order_status_id = 2 WHERE id = %s ;", str(current_order_id))
            self.conn.commit()
            self.on_new_order()
        else:
            self.current_order = None
            self.current_order_items = None
            # put orchestrator to idle

    def get_table_names(self):
        self.cur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in self.cur.fetchall():
            print(table)