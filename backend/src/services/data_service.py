from typing import Optional, List, Dict, Any
from sqlalchemy import text
from src.services.db import get_db_connection

class DataService:
    def __init__(self):
        # This acts as our in-memory cache
        self._filter_cache: Dict[str, Any] = {}
        self._is_cache_loaded = False
        

    def refresh_filters(self):
        """
        Fetches unique values from the database and updates the internal cache.
        This is the expensive operation (O(N)).
        """
        conn = get_db_connection()
        try:
            print("Loading transaction filters from Database...")
            options = {}
            
            # Regions
            result = conn.execute(text("SELECT DISTINCT customer_region FROM transactions ORDER BY customer_region"))
            options['regions'] = [row[0] for row in result.fetchall() if row[0] is not None]
            
            # Genders
            result = conn.execute(text("SELECT DISTINCT gender FROM transactions ORDER BY gender"))
            options['genders'] = [row[0] for row in result.fetchall() if row[0] is not None]
            
            # Age range
            result = conn.execute(text("SELECT MIN(age), MAX(age) FROM transactions WHERE age IS NOT NULL"))
            row = result.fetchone()
            options['age_range'] = {
                'min': row[0] if row and row[0] is not None else 0,
                'max': row[1] if row and row[1] is not None else 100
            }
            
            # Product categories
            result = conn.execute(text("SELECT DISTINCT product_category FROM transactions ORDER BY product_category"))
            options['product_categories'] = [row[0] for row in result.fetchall() if row[0] is not None]
            
            # Tags
            result = conn.execute(text("SELECT DISTINCT unnest(string_to_array(tags, ',')) FROM transactions WHERE tags IS NOT NULL AND tags != '' ORDER BY 1"))
            options['tags'] = [row[0] for row in result.fetchall()]
            
            # Payment methods
            result = conn.execute(text("SELECT DISTINCT payment_method FROM transactions ORDER BY payment_method"))
            options['payment_methods'] = [row[0] for row in result.fetchall() if row[0] is not None]
            
            # Update cache
            self._filter_cache = options
            self._is_cache_loaded = True
            print("Filters loaded successfully.")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise e
        finally:
            conn.close()

    def get_filter_options(self) -> Dict[str, Any]:
        """
        Returns the cached filters. O(1) complexity.
        If cache is empty (server restart), it forces a load.
        """
        if not self._is_cache_loaded:
            self.refresh_filters()
        return self._filter_cache

    def get_filtered_transactions(
        self,
        search: Optional[str],
        customer_region: Optional[List[str]],
        gender: Optional[List[str]],
        age_min: Optional[int],
        age_max: Optional[int],
        product_category: Optional[List[str]],
        tags: Optional[List[str]],
        payment_method: Optional[List[str]],
        date_from: Optional[str],
        date_to: Optional[str],
        sort_by: str,
        sort_order: str,
        page: int,
        page_size: int
    ) -> Dict[str, Any]:
        """
        Dynamic search query. This cannot be cached as it depends on user input.
        """
        conn = get_db_connection()
        try:
            conditions = []
            
            # Search
            if search:
                search_term = f"%{search}%"
                conditions.append(f"(customer_name ILIKE '{search_term}' OR phone_number::text ILIKE '{search_term}')")
            
            # Filters
            if customer_region:
                regions = "', '".join(customer_region)
                conditions.append(f"customer_region IN ('{regions}')")
            
            if gender:
                genders = "', '".join(gender)
                conditions.append(f"gender IN ('{genders}')")
            
            if age_min is not None:
                conditions.append(f"age >= {age_min}")
            if age_max is not None:
                conditions.append(f"age <= {age_max}")
            
            if product_category:
                categories = "', '".join(product_category)
                conditions.append(f"product_category IN ('{categories}')")
            
            if tags:
                tags_condition = " OR ".join([f"tags ILIKE '%{tag}%'" for tag in tags])
                conditions.append(f"({tags_condition})")
            
            if payment_method:
                methods = "', '".join(payment_method)
                conditions.append(f"payment_method IN ('{methods}')")
            
            if date_from:
                conditions.append(f"date >= '{date_from}'::timestamp")
            if date_to:
                conditions.append(f"date <= '{date_to}'::timestamp")
            
            where_clause = " AND ".join(conditions) if conditions else "TRUE"
            
            # Sort logic
            sort_map = {'date': 'date', 'quantity': 'quantity', 'customer_name': 'customer_name'}
            sort_column = sort_map.get(sort_by, 'date')
            sort_direction = "DESC" if sort_order.lower() == "desc" else "ASC"
            offset = (page - 1) * page_size

            #Get Total Count
            count_query = f"SELECT COUNT(*) FROM transactions WHERE {where_clause}"
            total_records = conn.execute(text(count_query)).scalar() or 0
            
            total_pages = (total_records + page_size - 1) // page_size
            
            # fetch data
            data = []
            if total_records > 0:
                data_query = f"""
                    SELECT * FROM transactions 
                    WHERE {where_clause}
                    ORDER BY {sort_column} {sort_direction}
                    LIMIT {page_size} OFFSET {offset}
                """
                result = conn.execute(text(data_query))
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in result.fetchall()]

            return {
                "total_records": total_records,
                "total_pages": total_pages,
                "current_page": page,
                "page_size": page_size,
                "data": data,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
            
        finally:
            conn.close()
            
    def shutdown(self):
        
        print("Shutting down DataService...")
        
        self._filter_cache.clear()
        self._is_cache_loaded = False
        try:
            
            
            temp_conn = get_db_connection()
            engine = temp_conn.engine
            temp_conn.close() 
            print("Disposing database engine pool...")
            engine.dispose() 
        except Exception as e:
            print(f"Error closing database engine: {e}")

        print("DataService resources released.")


data_service = DataService()