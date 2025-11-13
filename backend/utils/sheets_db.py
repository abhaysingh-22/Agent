"""
Google Sheets database helper module.
Handles all interactions with Google Sheets as a database.
"""
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GoogleSheetsDB:
    """Manages Google Sheets database operations."""
    
    def __init__(self):
        """Initialize Google Sheets connection."""
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
        
        # Make credentials path absolute
        if not os.path.isabs(self.credentials_path):
            backend_dir = Path(__file__).parent.parent
            self.credentials_path = backend_dir / self.credentials_path
        
        self.client = None
        self.spreadsheet = None
        self._connect()
    
    def _connect(self):
        """Establish connection to Google Sheets."""
        try:
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Authenticate
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                str(self.credentials_path), scope
            )
            self.client = gspread.authorize(credentials)
            
            # Open the spreadsheet
            self.spreadsheet = self.client.open_by_key(self.sheet_id)
            print("✅ Successfully connected to Google Sheets!")
            
        except FileNotFoundError:
            print(f"❌ Credentials file not found: {self.credentials_path}")
            print("Please follow GOOGLE_SHEETS_SETUP.md to set up credentials.")
            raise
        except Exception as e:
            print(f"❌ Failed to connect to Google Sheets: {str(e)}")
            raise
    
    def get_food_stocks(self, item_name: Optional[str] = None) -> List[Dict]:
        """
        Get food stock information.
        
        Args:
            item_name: Optional item name to filter by
            
        Returns:
            List of dictionaries containing stock information
        """
        try:
            worksheet = self.spreadsheet.worksheet('Stocks')
            records = worksheet.get_all_records()
            
            if item_name:
                # Filter by item name (case-insensitive)
                records = [
                    r for r in records 
                    if item_name.lower() in r.get('Item Name', '').lower()
                ]
            
            return records
        except Exception as e:
            print(f"Error fetching food stocks: {str(e)}")
            return []
    
    def get_orders(self, status: Optional[str] = None) -> List[Dict]:
        """
        Get order information.
        
        Args:
            status: Optional status to filter by (e.g., 'Pending', 'Completed')
            
        Returns:
            List of dictionaries containing order information
        """
        try:
            worksheet = self.spreadsheet.worksheet('Orders')
            records = worksheet.get_all_records()
            
            if status:
                # Filter by status (case-insensitive)
                records = [
                    r for r in records 
                    if r.get('Status', '').lower() == status.lower()
                ]
            
            return records
        except Exception as e:
            print(f"Error fetching orders: {str(e)}")
            return []
    
    def add_order(self, customer_name: str, items: str, total: float) -> bool:
        """
        Add a new order to the Orders sheet.
        
        Args:
            customer_name: Name of the customer
            items: Description of ordered items
            total: Total price
            
        Returns:
            True if successful, False otherwise
        """
        try:
            worksheet = self.spreadsheet.worksheet('Orders')
            
            # Get current timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Get next order ID
            records = worksheet.get_all_records()
            next_id = f"ORD-{len(records) + 1:03d}"
            
            # Add new row
            new_row = [next_id, customer_name, items, total, 'Pending', timestamp]
            worksheet.append_row(new_row)
            
            print(f"✅ Order {next_id} added successfully!")
            return True
            
        except Exception as e:
            print(f"Error adding order: {str(e)}")
            return False
    
    def get_faqs(self, category: Optional[str] = None, search_query: Optional[str] = None) -> List[Dict]:
        """
        Get FAQ information.
        
        Args:
            category: Optional category to filter by
            search_query: Optional search term to find in questions or answers
            
        Returns:
            List of dictionaries containing FAQ information
        """
        try:
            worksheet = self.spreadsheet.worksheet('FAQs')
            records = worksheet.get_all_records()
            
            if category:
                # Filter by category (case-insensitive)
                records = [
                    r for r in records 
                    if r.get('Category', '').lower() == category.lower()
                ]
            
            if search_query:
                # Search in questions and answers
                search_lower = search_query.lower()
                records = [
                    r for r in records 
                    if search_lower in r.get('Question', '').lower() 
                    or search_lower in r.get('Answer', '').lower()
                ]
            
            return records
        except Exception as e:
            print(f"Error fetching FAQs: {str(e)}")
            return []
    
    def update_stock(self, item_name: str, new_quantity: int) -> bool:
        """
        Update the quantity of a stock item.
        
        Args:
            item_name: Name of the item to update
            new_quantity: New quantity value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            worksheet = self.spreadsheet.worksheet('Stocks')
            
            # Find the item
            cell = worksheet.find(item_name)
            if cell:
                # Update quantity (assuming Quantity is in column 3)
                worksheet.update_cell(cell.row, 3, new_quantity)
                
                # Update Last Updated date
                from datetime import datetime
                today = datetime.now().strftime('%Y-%m-%d')
                worksheet.update_cell(cell.row, 6, today)
                
                print(f"✅ Stock updated for {item_name}")
                return True
            else:
                print(f"❌ Item '{item_name}' not found")
                return False
                
        except Exception as e:
            print(f"Error updating stock: {str(e)}")
            return False


# Create a singleton instance
_db_instance = None

def get_sheets_db() -> GoogleSheetsDB:
    """Get or create the Google Sheets database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = GoogleSheetsDB()
    return _db_instance
