import sqlite3

class University():
    def __init__(self, database="data\\university.db"):
        self.database = database
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        print('Database is connected')
        
    def create_table(self, table_name, *args):
        with self.conn:
            self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(args)})")
        print(f'Table {table_name} is created')
            
    def close_connection(self):
        self.conn.close()
        print('Database is closed')
        
    def open_connection(self):
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        print('Database is connected again')
        
    def insert_into_table(self, table_name, *args):
        with self.conn:
            try:
                self.cur.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['?'] * len(args))})", args)
                
            except sqlite3.IntegrityError:
                print("sqlite3.IntegrityError: username is used before")
                
    def delete_from_table(self, table_name, *args):
        with self.conn:
            self.cur.execute(f"DELETE FROM {table_name} WHERE {', '.join(args)}")
        
    # def save_to_db(self):
    #     conn = sqlite3.connect(self.database)
    #     self.cur = conn.cursor()
    #     with conn:
    #         cur.execute("...")
    

    
