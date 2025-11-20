"""
Tools for the restaurant agent.
"""
import json
import os
from pathlib import Path
from langchain_core.tools import tool
from typing import Optional


@tool
def lookup_menu(category: str = None) -> str:
    """
    Look up menu items from Google Sheets database.
    
    Args:
        category: Optional category to filter by. If not provided, returns all menu items.
    
    Returns:
        A formatted string containing menu items with names and prices.
    """
    try:
        from utils.sheets_db import get_sheets_db
        
        db = get_sheets_db()
        
        # Try to get Menu worksheet, fallback to Stocks if Menu doesn't exist
        try:
            worksheet = db.spreadsheet.worksheet('Menu')
        except:
            worksheet = db.spreadsheet.worksheet('Stocks')
        
        records = worksheet.get_all_records()
        
        if not records:
            return "Menu is currently unavailable. Please try again later."
        
        # Debug: Print first record to see column names
        if records:
            print(f"DEBUG - Available columns: {list(records[0].keys())}")
        
        # If no category specified, return all items
        result = "**Our Menu:**\n\n"
        for item in records:
            # Try different possible column names
            dish_name = (item.get('Dish Name') or 
                        item.get('Item Name') or 
                        item.get('Name') or 
                        item.get('Dish') or 
                        'Unknown')
            
            price = (item.get('Price (INR)') or 
                    item.get('Price') or 
                    item.get('Rate') or 
                    0)
            
            result += f"- {dish_name}: ₹{price}\n"
        
        return result
        
    except Exception as e:
        return f"Unable to fetch menu. Error: {str(e)}"


@tool
def check_food_stock(item_name: Optional[str] = None) -> str:
    """
    Check food stock availability from Google Sheets database.
    
    Args:
        item_name: Optional item name to check. If not provided, returns all stocks.
    
    Returns:
        A formatted string containing stock information.
    """
    try:
        from utils.sheets_db import get_sheets_db
        
        db = get_sheets_db()
        stocks = db.get_food_stocks(item_name)
        
        if not stocks:
            if item_name:
                return f"No stock information found for '{item_name}'."
            return "Stock information is currently unavailable. Please contact the restaurant."
        
        result = "**Current Food Stocks:**\n\n"
        for stock in stocks:
            result += f"- {stock.get('Item Name', 'Unknown')}: "
            result += f"{stock.get('Quantity', 0)} {stock.get('Unit', 'units')} "
            result += f"(₹{stock.get('Price', 0)} per {stock.get('Unit', 'unit')})\n"
            result += f"  Category: {stock.get('Category', 'N/A')}\n"
        
        return result
        
    except Exception as e:
        error_msg = str(e)
        print(f"ERROR in check_food_stock: {error_msg}")
        if "credentials" in error_msg.lower():
            return "Unable to access stock database. Google Sheets credentials are not configured properly."
        elif "sheet" in error_msg.lower():
            return "Unable to access stock information. The Stocks worksheet may be missing."
        return f"Unable to fetch stock information. Error: {error_msg}"


@tool
def get_order_status(order_id: Optional[str] = None, status_filter: Optional[str] = None) -> str:
    """
    Get order information from Google Sheets database.
    
    Args:
        order_id: Optional order ID to look up specific order
        status_filter: Optional status to filter orders (Pending, Completed, Cancelled)
    
    Returns:
        A formatted string containing order information.
    """
    try:
        from utils.sheets_db import get_sheets_db
        
        db = get_sheets_db()
        orders = db.get_orders(status_filter)
        
        if not orders:
            return "No orders found."
        
        # If looking for specific order
        if order_id:
            orders = [o for o in orders if o.get('Order ID', '').upper() == order_id.upper()]
            if not orders:
                return f"Order {order_id} not found."
        
        result = "**Orders:**\n\n"
        for order in orders:
            result += f"- Order ID: {order.get('Order ID', 'N/A')}\n"
            result += f"  Customer: {order.get('Customer Name', 'N/A')}\n"
            result += f"  Items: {order.get('Items', 'N/A')}\n"
            result += f"  Total: ₹{order.get('Total', 0)}\n"
            result += f"  Status: {order.get('Status', 'N/A')}\n"
            result += f"  Time: {order.get('Timestamp', 'N/A')}\n\n"
        
        return result
        
    except Exception as e:
        return f"Unable to fetch order information. Error: {str(e)}"


@tool
def place_order(customer_name: str, items: str, total: float) -> str:
    """
    Place a new order in the Google Sheets database.
    
    Args:
        customer_name: Name of the customer
        items: Description of ordered items
        total: Total price of the order
    
    Returns:
        Confirmation message with order details.
    """
    try:
        from utils.sheets_db import get_sheets_db
        
        db = get_sheets_db()
        success = db.add_order(customer_name, items, total)
        
        if success:
            return f"✅ Order placed successfully!\n\nCustomer: {customer_name}\nItems: {items}\nTotal: ₹{total}\nStatus: Pending"
        else:
            return "❌ Failed to place order. Please try again."
        
    except Exception as e:
        return f"Unable to place order. Error: {str(e)}"


@tool
def search_faqs(query: Optional[str] = None, category: Optional[str] = None) -> str:
    """
    Search frequently asked questions from Google Sheets database.
    
    Args:
        query: Search term to find in questions or answers
        category: Category to filter by (General, Menu, Orders, etc.)
    
    Returns:
        A formatted string containing matching FAQs.
    """
    try:
        from utils.sheets_db import get_sheets_db
        
        db = get_sheets_db()
        faqs = db.get_faqs(category, query)
        
        if not faqs:
            return "No FAQs found matching your query."
        
        result = "**Frequently Asked Questions:**\n\n"
        for faq in faqs:
            result += f"**Q: {faq.get('Question', 'N/A')}**\n"
            result += f"A: {faq.get('Answer', 'N/A')}\n"
            result += f"_(Category: {faq.get('Category', 'N/A')})_\n\n"
        
        return result
        
    except Exception as e:
        return f"Unable to fetch FAQs. Error: {str(e)}"


@tool
def update_food_stock(item_name: str, new_quantity: int) -> str:
    """
    Update the quantity of a food stock item.
    
    Args:
        item_name: Name of the item to update
        new_quantity: New quantity value
    
    Returns:
        Confirmation message.
    """
    try:
        from utils.sheets_db import get_sheets_db
        
        db = get_sheets_db()
        success = db.update_stock(item_name, new_quantity)
        
        if success:
            return f"✅ Stock updated: {item_name} quantity set to {new_quantity}"
        else:
            return f"❌ Failed to update stock for {item_name}"
        
    except Exception as e:
        return f"Unable to update stock. Error: {str(e)}"
        return "Error: Menu file not found. Please contact the restaurant."
    except json.JSONDecodeError:
        return "Error: Unable to read menu data. Please contact the restaurant."
    except Exception as e:
        return f"Error retrieving menu: {str(e)}"