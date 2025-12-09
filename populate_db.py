import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()  

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
CSV_FILE_PATH = os.getenv("csv_path")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing! Check your .env file.")



def seed_data(csv_path):
    print("⏳ Connecting to Supabase...")
    engine = create_engine(DATABASE_URL)

    try:
        print(f" Reading CSV from: {csv_path}")
        df = pd.read_csv(csv_path)

        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])

        numeric_cols = ['age', 'quantity', 'price_per_unit', 'total_amount', 'final_amount']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        print(f"✨ Prepared {len(df)} rows for insertion.")

        print("🚀 Uploading to Supabase (this may take a minute)...")
        df.to_sql(
            'transactions', 
            engine, 
            if_exists='replace', 
            index=False, 
            chunksize=10000,
            method='multi'
        )
        
        print("Success")
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM transactions"))
            count = result.scalar()
            print(f"📊 Verified Record Count in DB: {count}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    CSV_FILE_PATH = "/Users/nitishbiswas/truEstate_antigravity/truestate_assignment_dataset.csv" 
    seed_data(CSV_FILE_PATH)