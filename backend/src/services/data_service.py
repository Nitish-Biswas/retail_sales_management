import pandas as pd
import numpy as np
from typing import Dict, Any

class DataService:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self._prepare_data()
    
    def _prepare_data(self):
        # Convert Date
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        # Numeric columns to clean
        numeric_cols = [
            'Age', 'Quantity', 'Price per Unit', 'Discount Percentage', 
            'Total Amount', 'Final Amount'
        ]
        
        for col in numeric_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Fill NaN values to avoid JSON errors (Essential when not using Models)
        self.df[numeric_cols] = self.df[numeric_cols].fillna(0)
        self.df = self.df.fillna("")

    def apply_filters(self, filters: Dict[str, Any]) -> pd.DataFrame:
        df = self.df.copy()
        
        # Extract values safely from dict
        search = filters.get('search')
        if search:
            search_term = search.lower()
            mask = (
                (df['Customer name'].str.lower().str.contains(search_term, na=False)) |
                (df['Phone Number'].astype(str).str.lower().str.contains(search_term, na=False))
            )
            df = df[mask]
        
        if filters.get('customer_region'):
            df = df[df['Customer region'].isin(filters['customer_region'])]
            
        if filters.get('gender'):
            df = df[df['Gender'].isin(filters['gender'])]
            
        # Age handling
        age_min = filters.get('age_min')
        if age_min is not None:
            df = df[df['Age'] >= age_min]
            
        age_max = filters.get('age_max')
        if age_max is not None:
            df = df[df['Age'] <= age_max]
            
        if filters.get('product_category'):
            df = df[df['Product Category'].isin(filters['product_category'])]
            
        if filters.get('tags'):
            tags_pattern = '|'.join([t.lower() for t in filters['tags']])
            df = df[df['Tags'].astype(str).str.lower().str.contains(tags_pattern, na=False)]
            
        if filters.get('payment_method'):
            df = df[df['Payment Method'].isin(filters['payment_method'])]
            
        # Date handling
        if filters.get('date_from'):
            df = df[df['Date'] >= filters['date_from']]
            
        if filters.get('date_to'):
            df = df[df['Date'] <= filters['date_to']]
            
        return df
    
    def apply_sorting(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        sort_by = filters.get('sort_by', 'date')
        sort_order = filters.get('sort_order', 'desc')
        ascending = sort_order.lower() == 'asc'
        
        sort_map = {
            'date': 'Date',
            'quantity': 'Quantity',
            'customer_name': 'Customer name'
        }
        sort_column = sort_map.get(sort_by, 'Date')
        return df.sort_values(by=sort_column, ascending=ascending)
    
    def get_paginated_data(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Returns a plain dictionary instead of a Pydantic model"""
        
        filtered_df = self.apply_filters(filters)
        sorted_df = self.apply_sorting(filtered_df, filters)
        
        page = filters.get('page', 1)
        page_size = filters.get('page_size', 10)
        
        total_records = len(sorted_df)
        total_pages = (total_records + page_size - 1) // page_size
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_df = sorted_df.iloc[start_idx:end_idx]
        
        # Convert DataFrame directly to list of dicts
        data_list = paginated_df.to_dict(orient='records')
        
        # Handle Timestamps for JSON serialization
        for item in data_list:
            if isinstance(item.get('Date'), pd.Timestamp):
                item['Date'] = item['Date'].isoformat()

        return {
            "total_records": total_records,
            "total_pages": total_pages,
            "current_page": page,
            "page_size": page_size,
            "data": data_list,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
        
    def get_filter_options(self) -> dict:
        return {
            'regions': sorted(self.df['Customer region'].unique().tolist()),
            'genders': sorted(self.df['Gender'].unique().tolist()),
            'age_range': {
                'min': int(self.df['Age'].min()),
                'max': int(self.df['Age'].max())
            },
            'product_categories': sorted(self.df['Product Category'].unique().tolist()),
            'tags': sorted(self.df['Tags'].unique().tolist()),
            'payment_methods': sorted(self.df['Payment Method'].unique().tolist())
        }