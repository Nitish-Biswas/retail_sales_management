# Retail Sales Management System

## 1. Overview
This project is a full-stack web application designed to manage and visualize large volumes of retail transaction data. It provides a responsive dashboard for browsing sales records with advanced filtering, real-time search, and sorting capabilities. The system is optimized for performance, handling millions of records efficiently using server-side pagination and database indexing.

## 2. Tech Stack

*   **Frontend**: React, Vite, Axios
*   **Backend**: Python, FastAPI, SQLAlchemy, Pandas
*   **Database**: PostgreSQL
*   **Performance**: `pg_trgm` (PostgreSQL Trigram Extension) for fuzzy search, concurrent indexing

## 3. Search Implementation Summary
Search functionality is implemented using a dynamic SQL query builder in the backend (`data_service.py`).
*   **Logic**: Performs case-insensitive matching (`ILIKE`) on **Customer Name** and **Phone Number**.
*   **Optimization**: Uses the PostgreSQL `pg_trgm` extension to create **GIN indexes** (`gin_trgm_ops`). This allows for highly efficient fuzzy search operations even on large datasets, preventing full table scans.

## 4. Filter Implementation Summary
The system supports multi-faceted filtering to narrow down transaction data.
*   **Fields**: Region, Gender, Age Range, Product Category, Tags, Payment Method, and Date Range.
*   **Caching Strategy**: Filter options (e.g., unique regions, categories) are fetched and cached in-memory on server startup (`refresh_filters`). This ensures that the frontend filter dropdowns load instantly without repeatedly querying the database for distinct values.
*   **Query Construction**: Filters are applied dynamically using SQL `IN` clauses for categorical data and comparison operators (`>=`, `<=`) for range data.

## 5. Sorting Implementation Summary
Sorting is handled server-side to ensure accurate ordering across the entire dataset.
*   **Capabilities**: Users can sort by **Date**, **Quantity**, and **Customer Name** in both Ascending and Descending order.
*   **Performance**: Dedicated B-tree indexes are created for each sortable column (e.g., `idx_date_desc`, `idx_quantity_desc`) to ensure that sorting operations are fast and do not require expensive in-memory sorts.

## 6. Pagination Implementation Summary
To handle large datasets efficiently, pagination is implemented using the `LIMIT` and `OFFSET` SQL clauses.
*   **Mechanism**: The backend calculates `total_records` and `total_pages` based on the current active filters.
*   **Response**: The API returns only the requested slice of data (e.g., 10 items) along with metadata (`current_page`, `has_next`, `has_prev`), ensuring the frontend remains lightweight and responsive.

## 7. Setup Instructions

### Prerequisites
*   Node.js & npm
*   Python 3.8+
*   PostgreSQL Database (or Supabase)

### Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the `backend` folder with your database credentials:
    ```env
    user=your_db_user
    password=your_db_password
    host=your_db_host
    port=5432
    dbname=your_db_name
    csv_path=/path/to/dataset.csv
    ```
5.  Start the server:
    ```bash
    uvicorn src.index:app --reload
    ```

### Database Population & Indexing
To ensure fast queries, you must populate the database and create indexes.
1.  **Seed Data**: Run the population script to load data from your CSV.
    ```bash
    python populate_db.py
    ```
2.  **Create Indexes**: Run the indexing script to generate optimization indexes.
    ```bash
    python index_db.py
    ```

### Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Create a `.env` file in the `frontend` folder with your backend credentials:
    ```env
    VITE_API_BASE = [BACKEND_URL] + /api
    ```

3.  Install dependencies:
    ```bash
    npm install
    ```
4.  Start the development server:
    ```bash
    npm run dev
    ```
