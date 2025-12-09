# System Architecture

## 1. Backend Architecture

The backend is built using **Python** and **FastAPI**, designed for high performance and ease of development. It follows a layered architecture to separate concerns.

### Key Components
*   **API Layer (`src/routes`)**: Handles HTTP requests, input validation (Pydantic), and routing. It acts as the entry point for the frontend.
*   **Service Layer (`src/services`)**: Contains the business logic.
    *   **DataService**: Manages transaction retrieval, filtering logic, and caching of filter options. It constructs dynamic SQL queries based on user input.
*   **Database Layer**:
    *   **SQLAlchemy**: Used as the ORM/Query builder for safe SQL construction.
    *   **Pandas**: Utilized for efficient data processing during the initial seeding phase.
*   **Database**: **PostgreSQL** is the persistent storage, heavily optimized with:
    *   **Trigram Indexes (`pg_trgm`)**: For fuzzy matching in search.
    *   **B-Tree Indexes**: For fast sorting and range filtering (Dates, Quantities).

## 2. Frontend Architecture

The frontend is a Single Page Application (SPA) built with **React** and **Vite**. It emphasizes modularity and component reusability.

### Key Components
*   **App Container (`App.jsx`)**: The main state holder. It manages the global state for filters, search queries, pagination, and fetched transaction data. It coordinates the data flow between child components and the API service.
*   **Access/Service Layer (`src/services/api.js`)**: Encapsulates all network requests using **Axios**. It provides typed functions for fetching transactions and filter options, decoupling the UI from the API implementation.
*   **UI Components (`src/components`)**:
    *   `TransactionTable`: A presentational component that renders the data grid.
    *   `FilterPanel`: Manages the multi-faceted filter UI inputs.
    *   `SearchBar`: Handles user search input with debouncing (implied/recommended).
    *   `Pagination`: Renders page controls and communicates page changes to the parent.

## 3. Data Flow

1.  **User Interaction**: The user interacts with the UI (enters search term, selects a filter, changes page).
2.  **State Update**: The `App` component updates its internal state to reflect the new parameters.
3.  **API Request**:
    *   `App.jsx` triggers an effect.
    *   Calls `api.getTransactions()` with the current state as query parameters.
4.  **Backend Processing**:
    *   FastAPI receives the request at `GET /api/transactions`.
    *   `DataService` builds a dynamic SQL query using `SQLAlchemy`.
    *   PostgreSQL executes the optimized query using indexes.
5.  **Response**: The data (records + pagination metadata) is returned to the frontend.
6.  **Render**: React updates the `TransactionTable` with the new data.

## 4. Folder Structure

```
retail_sales_management/
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   │   └── api.py           # API Endpoints
│   │   ├── services/
│   │   │   ├── data_service.py  # Business Logic & Caching
│   │   │   └── db.py            # Database Connection
│   │   └── index.py             # App Entry Point
│   ├── requirements.txt         # Python Dependencies
│   └── .env                     # Backend Environment Variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FilterPanel.jsx
│   │   │   ├── Pagination.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   ├── SortDropdown.jsx
│   │   │   └── TransactionTable.jsx
│   │   ├── services/
│   │   │   └── api.js           # API Integration
│   │   ├── App.jsx              # Main Container
│   │   └── main.jsx             # React Entry Point
│   ├── package.json             # JS Dependencies
│   └── .env                     # Frontend Environment Variables
├── docs/
│   └── architecture.md          # This Document
├── index_db.py                  # Database Indexing Script
├── populate_db.py               # Database Seeding Script
└── README.md                    # Project Documentation
```

## 5. Module Responsibilities

### Backend
*   **`src/index.py`**: Initializes the FastAPI app, configures CORS, and includes routers.
*   **`src/services/data_service.py`**: The core logic engine.
    *   `refresh_filters()`: Loads distinct values from DB on startup for fast UI rendering.
    *   `get_filtered_transactions()`: Constructs SQL WHERE clauses dynamically based on complex user criteria.
*   **`populate_db.py`**: A standalone script to ingest the raw CSV dataset into PostgreSQL, handling type conversion and cleaning.
*   **`index_db.py`**: A dedicated maintenance script to apply database schema optimizations (indexes).

### Frontend
*   **`src/services/api.js`**: Centralizes all API calls. Helps manage endpoints and query string formatting.
*   **`src/App.jsx`**: Acts as the "Controller" view. It handles the logic of combining different filters and state into a cohesive API request.
*   **`src/components/`**: Pure presentational components. They receive data/callbacks via props and are unaware of the application's business logic.
