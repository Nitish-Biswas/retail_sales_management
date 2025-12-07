import pandas as pd
from typing import List, Optional
from datetime import datetime
from src.models.schemas import TransactionSchema, FilterParams, PaginatedResponse

class DataService:
    def __init__(self, csv_path: str):
        """Initialize with CSV file path"""
        self.df = pd.read_csv(csv_path)
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare and clean data"""
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['Age'] = pd.to_numeric(self.df['Age'], errors='coerce')
        self.df['Quantity'] = pd.to_numeric(self.df['Quantity'], errors='coerce')
        self.df['Price per Unit'] = pd.to_numeric(self.df['Price per Unit'], errors='coerce')
        self.df['Discount Percentage'] = pd.to_numeric(self.df['Discount Percentage'], errors='coerce')
        self.df['Total Amount'] = pd.to_numeric(self.df['Total Amount'], errors='coerce')
        self.df['Final Amount'] = pd.to_numeric(self.df['Final Amount'], errors='coerce')
        
        # Handle missing values
        self.df.fillna('', inplace=True)
    
    def apply_filters(self, filters: FilterParams) -> pd.DataFrame:
        """Apply all filters to dataframe"""
        df = self.df.copy()
        
        # Search filter (case-insensitive)
        if filters.search:
            search_term = filters.search.lower()
            mask = (
                (df['Customer Name'].str.lower().str.contains(search_term, na=False)) |
                (df['Phone Number'].astype(str).str.lower().str.contains(search_term, na=False))
            )
            df = df[mask]
        
        # Customer Region filter
        if filters.customer_region:
            df = df[df['Customer Region'].isin(filters.customer_region)]
        
        # Gender filter
        if filters.gender:
            df = df[df['Gender'].isin(filters.gender)]
        
        # Age Range filter
        if filters.age_min is not None:
            df = df[df['Age'] >= filters.age_min]
        if filters.age_max is not None:
            df = df[df['Age'] <= filters.age_max]
        
        # Product Category filter
        if filters.product_category:
            df = df[df['Product Category'].isin(filters.product_category)]
        
        # Tags filter
        if filters.tags:
            tags_pattern = '|'.join([t.lower() for t in filters.tags])
            df = df[df['Tags'].astype(str).str.lower().str.contains(tags_pattern, na=False)]
        
        # Payment Method filter
        if filters.payment_method:
            df = df[df['Payment Method'].isin(filters.payment_method)]
        
        # Date Range filter
        if filters.date_from:
            df = df[df['Date'] >= filters.date_from]
        if filters.date_to:
            df = df[df['Date'] <= filters.date_to]
        
        return df
    
    def apply_sorting(self, df: pd.DataFrame, filters: FilterParams) -> pd.DataFrame:
        """Apply sorting to filtered dataframe"""
        sort_by = filters.sort_by
        sort_order = filters.sort_order.lower() == 'asc'
        
        sort_map = {
            'date': 'Date',
            'quantity': 'Quantity',
            'customer_name': 'Customer Name'
        }
        
        sort_column = sort_map.get(sort_by, 'Date')
        
        return df.sort_values(by=sort_column, ascending=sort_order)
    
    def get_paginated_data(self, filters: FilterParams) -> PaginatedResponse:
        """Get paginated filtered and sorted data"""
        # Apply filters
        filtered_df = self.apply_filters(filters)
        
        # Apply sorting
        sorted_df = self.apply_sorting(filtered_df, filters)
        
        total_records = len(sorted_df)
        total_pages = (total_records + filters.page_size - 1) // filters.page_size
        
        # Calculate pagination
        start_idx = (filters.page - 1) * filters.page_size
        end_idx = start_idx + filters.page_size
        
        paginated_df = sorted_df.iloc[start_idx:end_idx]
        
        # Convert to response format
        data = []
        for _, row in paginated_df.iterrows():
            try:
                data.append(TransactionSchema(
                    transaction_id=str(row.get('Transaction ID', '')),
                    date=row.get('Date'),
                    customer_id=str(row.get('Customer ID', '')),
                    customer_name=str(row.get('Customer Name', '')),
                    phone_number=str(row.get('Phone Number', '')),
                    gender=str(row.get('Gender', '')),
                    age=int(row.get('Age', 0)) if pd.notna(row.get('Age')) else 0,
                    customer_region=str(row.get('Customer Region', '')),
                    customer_type=str(row.get('Customer Type', '')),
                    product_id=str(row.get('Product ID', '')),
                    product_name=str(row.get('Product Name', '')),
                    brand=str(row.get('Brand', '')),
                    product_category=str(row.get('Product Category', '')),
                    tags=str(row.get('Tags', '')),
                    quantity=int(row.get('Quantity', 0)) if pd.notna(row.get('Quantity')) else 0,
                    price_per_unit=float(row.get('Price per Unit', 0)) if pd.notna(row.get('Price per Unit')) else 0,
                    discount_percentage=float(row.get('Discount Percentage', 0)) if pd.notna(row.get('Discount Percentage')) else 0,
                    total_amount=float(row.get('Total Amount', 0)) if pd.notna(row.get('Total Amount')) else 0,
                    final_amount=float(row.get('Final Amount', 0)) if pd.notna(row.get('Final Amount')) else 0,
                    payment_method=str(row.get('Payment Method', '')),
                    order_status=str(row.get('Order Status', '')),
                    delivery_type=str(row.get('Delivery Type', '')),
                    store_id=str(row.get('Store ID', '')),
                    store_location=str(row.get('Store Location', '')),
                    salesperson_id=str(row.get('Salesperson ID', '')),
                    employee_name=str(row.get('Employee Name', ''))
                ))
            except Exception as e:
                print(f"Error processing row: {e}")
                continue
        
        return PaginatedResponse(
            total_records=total_records,
            total_pages=total_pages,
            current_page=filters.page,
            page_size=filters.page_size,
            data=data,
            has_next=filters.page < total_pages,
            has_prev=filters.page > 1
        )
    
    def get_filter_options(self) -> dict:
        """Get available options for all filters"""
        try:   
            return {
                'regions': sorted(self.df['Customer Region'].unique().tolist()),
                'genders': sorted(self.df['Gender'].unique().tolist()),
                'age_range': {
                    'min': int(self.df['Age'].min()),
                    'max': int(self.df['Age'].max())
                },
                'product_categories': sorted(self.df['Product Category'].unique().tolist()),
                'tags': sorted(self.df['Tags'].unique().tolist()),
                'payment_methods': sorted(self.df['Payment Method'].unique().tolist())
            }
        except Exception as e:
            print("error in filter", e)