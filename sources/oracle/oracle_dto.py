# Class for Oracle connectivity which inherits fom DatabaseManager
from sources.__init__ import DatabaseManager
import sqlalchemy

class OracleDatabaseManager(DatabaseManager):
    def __init__(self, db_url):
        super().__init__(db_url)
    
    # Additional Oracle-specific methods can be added here
    # For example, methods to handle Oracle-specific data types or queries

    # Read all tables in the Oracle database
    def read_all_tables(self):
        """Read all tables in the Oracle database."""
        tables = self.get_tables()
        data = {}
        for table in tables:
            data[table] = self.read_data(table)
        return data
    
    # describe a table in the Oracle database
    def describe_table(self, table):
        """Describe a table in the Oracle database."""
        with self.get_connection() as connection:
            inspector = sqlalchemy.inspect(connection)
            return inspector.get_columns(table)
        
    # create a new table in the Oracle database
    def create_table(self, table_name, columns):
        """Create a new table in the Oracle database."""
        with self.get_connection() as connection:
            metadata = sqlalchemy.MetaData()
            table = sqlalchemy.Table(table_name, metadata, *columns)
            metadata.create_all(connection)
    
    # Drop a table in the Oracle database
    def drop_table(self, table_name):
        """Drop a table in the Oracle database."""
        with self.get_connection() as connection:
            metadata = sqlalchemy.MetaData()
            table = sqlalchemy.Table(table_name, metadata, autoload_with=connection)
            table.drop(connection)

    # close the connection to the Oracle database
    def close_connection(self):
        """Close the connection to the Oracle database."""
        self.disconnect()
        

    