import sqlalchemy
from sqlalchemy import create_engine


# Class to manage database connections
class DatabaseManager:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = None

    def connect(self):
        """Establish a database connection."""
        if not self.engine:
            self.engine = create_engine(self.db_url)
        return self.engine

    def disconnect(self):
        """Close the database connection."""
        if self.engine:
            self.engine.dispose()
            self.engine = None
           
    # getters for database engine
    def get_engine(self):
        """Get the SQLAlchemy engine."""
        return self.engine  
    
    # fucntion to get list of tables in the database
    def get_tables(self):
        """Get a list of tables in the database."""
        with self.connect().connect() as connection:
            return connection.engine.table_names()
        
    # initialize a connection pool
    def initialize_connection_pool(self, pool_size=5, max_overflow=10, pool_timeout=30):
        """Initialize a connection pool."""
        if not self.engine:
            self.engine = create_engine(self.db_url, 
                                        pool_size=pool_size, 
                                        max_overflow=max_overflow,
                                        pool_timeout=pool_timeout)
        return self.engine
    
    # create connection from pool created. handle if no conenction available in connection pool
    def get_connection(self):
        """Get a connection from the pool."""
        if not self.engine:
            self.connect()
        return self.engine.connect()
    
    # Fucntions to perform basic CRUD operations
    def insert_data(self, table, data):
        """Insert data into a table."""
        with self.get_connection() as connection:
            connection.execute(table.insert(), data)
    
    def read_data(self, query):
        """Execute query provide and return the result"""
        with self.get_connection() as connection:
            return connection.execute(query).fetchall()
    
    def update_data(self, table, data, filters):
        """Update data in a table."""
        with self.get_connection() as connection:
            query = table.update().values(data).where(filters)
            connection.execute(query)
    
    def delete_data(self, table, filters):
        """Delete data from a table."""
        with self.get_connection() as connection:
            query = table.delete().where(filters)
            connection.execute(query)
    
    