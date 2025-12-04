from sqlalchemy import create_engine

# Connection string format: mysql+mysqlconnector://user:password@host/db_name
DB_CONNECTION_STR = 'mysql+mysqlconnector://root:Sp!dey71@localhost/traffic_sim'

def get_db_engine():
    return create_engine(DB_CONNECTION_STR)