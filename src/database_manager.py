import sqlite3


class InventoryDatabase:
    def __init__(self, db_path="inventory.db"):
        # Initialise the database connection and create tables if they don't exist
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates the database tables if they don't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            category TEXT,
            unit_price REAL,
            quantity_in_stock INTEGER DEFAULT 0,
            restock_threshold INTEGER DEFAULT 2
        )''')

        # Create the inventory transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_transactions (
            transaction_id INTEGER PRIMARY KEY,
            item_id INTEGER,
            transaction_type TEXT CHECK(transaction_type IN ('add', 'remove')) NOT NULL,
            quantity INTEGER NOT NULL,
            transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES items(item_id)
        )''')

        # Create the item expirations table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS item_expirations (
            expiration_id INTEGER PRIMARY KEY,
            item_id INTEGER,
            expiration_date TEXT,
            quantity INTEGER,
            FOREIGN KEY (item_id) REFERENCES items(item_id)
        )''')
        self.conn.commit()

        if self.is_empty():
            self.add_initial_items()

    def add_item(self, item_name, category, unit_price, quantity_in_stock, restock_threshold):
        """Insert a new item into the items table"""
        self.cursor.execute('''
            INSERT INTO items (item_name, category, unit_price, quantity_in_stock, restock_threshold)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_name, category, unit_price, quantity_in_stock, restock_threshold))
        self.conn.commit()

    def add_initial_items(self):
        """Insert initial items into the items table"""
        items = [
            ('Milk', 'Dairy', 1.50, 3, 1),
            ('Eggs', 'Poultry', 0.20, 24, 6),
            ('Flour', 'Baking', 0.80, 3, 1),
            ('Sugar', 'Baking', 1.00, 3, 1),
            ('Butter', 'Dairy', 2.00, 2, 1),
            ('Cheese', 'Dairy', 3.50, 3, 1),
            ('Chicken', 'Meat', 5.00, 2, 1),
            ('Beef', 'Meat', 7.00, 3, 1),
            ('Apples', 'Produce', 0.70, 12, 3),
            ('Oranges', 'Produce', 0.60, 12, 3),
            ('Carrots', 'Produce', 0.40, 15, 6),
            ('Potatoes', 'Produce', 0.30, 20, 10),
            ('Olive Oil', 'Pantry', 5.50, 3, 1),
            ('Salt', 'Pantry', 0.50, 3, 1),
            ('Pepper', 'Pantry', 0.75, 3, 1)
        ]
        self.cursor.executemany('''
            INSERT INTO items (item_name, category, unit_price, quantity_in_stock, restock_threshold)
            VALUES (?, ?, ?, ?, ?)
        ''', items)
        self.conn.commit()

    #def add_stock(self, item_id, quantity):
        # Add stock to an item in the items table
        #self.cursor.execute('''
        #    UPDATE items
        #    SET quantity_in_stock = quantity_in_stock + ?
        #    WHERE item_id = ?
        #''', (quantity, item_id))
        #self.conn.commit()

    def remove_item(self, item_id):
        """Remove an item from the items table by item_id"""
        self.cursor.execute("DELETE FROM inventory WHERE item_id = ?", (item_id,))
        self.conn.commit()

    def insert_inventory_transaction(self, item_id, transaction_type, quantity, transaction_date=None):
        """Insert a transaction for adding or removing stock"""
        if transaction_date:
            self.cursor.execute('''
                INSERT INTO inventory_transactions (item_id, transaction_type, quantity, transaction_date)
                VALUES (?, ?, ?, ?)
            ''', (item_id, transaction_type, quantity, transaction_date))
        else:
            self.cursor.execute('''
                INSERT INTO inventory_transactions (item_id, transaction_type, quantity)
                VALUES (?, ?, ?)
            ''', (item_id, transaction_type, quantity))
        self.conn.commit()

    def insert_item_expiration(self, item_id, expiration_date, quantity):
        """Insert an expiration date entry for an item"""
        self.cursor.execute('''
            INSERT INTO item_expirations (item_id, expiration_date, quantity)
            VALUES (?, ?, ?)
        ''', (item_id, expiration_date, quantity))
        self.conn.commit()

    def get_all_items(self):
        """Retrieve all items with their quantity from the items table"""
        self.cursor.execute('SELECT item_name, quantity_in_stock FROM items')
        return self.cursor.fetchall()

    def get_item_by_id(self, item_id):
        """Retrieve a single item by item_id"""
        self.cursor.execute('SELECT * FROM items WHERE item_id = ?', (item_id,))
        return self.cursor.fetchone()

    def get_item_by_name(self, item_name):
        """Retrieve a single item by item_name"""
        self.cursor.execute('SELECT * FROM items WHERE item_name = ?', (item_name,))
        return self.cursor.fetchone()

    def is_empty(self):
        """Check if the items table is empty"""
        self.cursor.execute('SELECT COUNT(*) FROM items')
        count = self.cursor.fetchone()[0]
        if count == 0:
            return True
        return False

    def close(self):
        """
        Close the database connection
        """
        self.conn.close()

