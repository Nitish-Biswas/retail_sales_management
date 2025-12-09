from sqlalchemy import text, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

def reset_and_add_all_indexes():
    engine = create_engine(DATABASE_URL)
    
    with engine.execution_options(isolation_level="AUTOCOMMIT").connect() as conn:
        

        conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        print("Creating ALL Indexes...")
        
        all_indexes = [
            
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_name_trgm ON transactions USING gin (customer_name gin_trgm_ops)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_phone_trgm ON transactions USING gin (CAST(phone_number AS TEXT) gin_trgm_ops)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_tags_trgm ON transactions USING gin (tags gin_trgm_ops)",

            
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_date_desc ON transactions(date DESC)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_date_asc ON transactions(date ASC)",
            
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_quantity_desc ON transactions(quantity DESC)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_quantity_asc ON transactions(quantity ASC)",
            
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_name_asc ON transactions(customer_name ASC)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_customer_name_desc ON transactions(customer_name DESC)",


            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_region ON transactions(customer_region)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_category ON transactions(product_category)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_payment ON transactions(payment_method)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_gender ON transactions(gender)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_age ON transactions(age)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_phone ON transactions(phone_number)", 

            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_region_gender ON transactions(customer_region, gender)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_region_date ON transactions(customer_region, date DESC)",
            "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_age_region ON transactions(age, customer_region)",
        ]

        for sql in all_indexes:
            try:
                name = sql.split("INDEX CONCURRENTLY IF NOT EXISTS ")[1].split(" ON")[0]
                conn.execute(text(sql))
                print(f"      Created: {name}")
            except Exception as e:
                print(f"      Error creating index: {e}")

        print(" Analyzing Table Statistics...")
        conn.execute(text("ANALYZE transactions"))

    
    engine.dispose()

if __name__ == "__main__":
    reset_and_add_all_indexes()