from queue import Queue
import psycopg2


class OrderHandler:

    orders = Queue()
    current_order_items = None
    current_order = None

    def __init__(self, on_new_order):
        self.on_new_order = on_new_order
        """try:
            self.conn = psycopg2.connect(dbname="wrapper_development", host="localhost", port=5432)
            # self.conn = psycopg2.connect("dbname=wrapper_production user=wrapper")
            self.cur = self.conn.cursor()
            #self.get_table_names()
            #self.get_column_names("order_items")
        except psycopg2.OperationalError:
            print("No db running. Please start the dashboard")
            exit()"""

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
        print("order")
        print(order)
        #id = str(order["id"])
        self.orders.put_nowait(order)
        if self.current_order is None:
            self.current_order = self.orders.get_nowait()
            self.on_new_order()

    """self.cur.execute("SELECT * FROM orders WHERE id = '{0}';".format(order["id"]))
        for order in self.cur.fetchall():
            self.orders.put_nowait(order)
            print("Added new order")
            print(order)"""

    def get_next_order(self):
        if self.current_order is not None:
            current_order_id = str(self.current_order[0])
            self.cur.execute("UPDATE orders SET order_status_id = 3 WHERE id = %s ;", str(current_order_id))
            self.conn.commit()
        if not self.orders.empty():
            self.current_order = self.orders.get_nowait()
            current_order_id = str(self.current_order[0])
            #order_item_ids = ["1","2","3","4"]

            order_item_ids = self.get_order_item_ids(current_order_id)

            order_item_ids_str = ",".join([str(i[0]) for i in order_item_ids])
            #  WHERE id in (%s);" % order_item_ids_str
            current_order_items = {}
            self.cur.execute("SELECT p.name, p.image, pg.id, pg.name FROM products AS p, product_groups AS pg WHERE p.id in (%s) AND p.product_group_id = pg.id;" % order_item_ids_str)
            item_json = {}
            # add new product groups here
            for item in self.cur.fetchall():
                item_json = {
                    "name": item[0],
                    "image": "",
                    "prod_group_id": item[2],
                    "prod_group_name": item[3]
                }
                if item[2] == 1:
                    current_order_items["packaging_style"] = item_json
                elif item[2] == 2:
                    current_order_items["paper"] = item_json
                elif item[2] == 3:
                    current_order_items["band"] = item_json
                elif item[2] == 4:
                    current_order_items["card"] = item_json

            self.current_order_items = current_order_items

            self.cur.execute("UPDATE orders SET order_status_id = 2 WHERE id = %s ;", str(current_order_id))
            self.conn.commit()
            print("Next order")
            print(item_json)
            self.on_new_order()
        else:
            self.current_order = None
            self.current_order_items = None
            # put orchestrator to idle

    def get_order_item_ids(self, order_id):
        self.cur.execute("SELECT p.id FROM orders AS o, order_items AS oi, products AS p WHERE o.id= %s AND p.id = oi.product_id AND o.id = oi.order_id;", str(order_id) )
        return self.cur.fetchall()

    def get_table_names(self):
        self.cur.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in self.cur.fetchall():
            print(table)

    def get_column_names(self, table):

        self.cur.execute("""SELECT *
FROM information_schema.columns
WHERE table_name = '%s';""" % table)
        for col in self.cur.fetchall():
            print(col)
