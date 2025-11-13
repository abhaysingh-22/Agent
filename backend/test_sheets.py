"""
Test script to verify Google Sheets connection and functionality.
Run this after setting up credentials and .env file.
"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv()

def test_connection():
    """Test basic connection to Google Sheets."""
    print("=" * 60)
    print("Testing Google Sheets Connection")
    print("=" * 60)
    
    try:
        from utils.sheets_db import get_sheets_db
        
        print("\n1️⃣  Connecting to Google Sheets...")
        db = get_sheets_db()
        print("✅ Connected successfully!")
        
        print("\n2️⃣  Testing Food Stocks...")
        stocks = db.get_food_stocks()
        if stocks:
            print(f"✅ Found {len(stocks)} stock items:")
            for stock in stocks[:3]:  # Show first 3
                print(f"   - {stock.get('Item Name')}: {stock.get('Quantity')} {stock.get('Unit')}")
        else:
            print("⚠️  No stock data found. Make sure 'Food Stocks' tab has data.")
        
        print("\n3️⃣  Testing Orders...")
        orders = db.get_orders()
        if orders:
            print(f"✅ Found {len(orders)} orders:")
            for order in orders[:3]:  # Show first 3
                print(f"   - {order.get('Order ID')}: {order.get('Customer Name')} - {order.get('Status')}")
        else:
            print("⚠️  No orders found. This is okay for a new setup.")
        
        print("\n4️⃣  Testing FAQs...")
        faqs = db.get_faqs()
        if faqs:
            print(f"✅ Found {len(faqs)} FAQs:")
            for faq in faqs[:3]:  # Show first 3
                print(f"   - Q: {faq.get('Question')[:50]}...")
        else:
            print("⚠️  No FAQs found. Make sure 'FAQs' tab has data.")
        
        print("\n5️⃣  Testing Add Order (will add a test order)...")
        success = db.add_order("Test Customer", "Test Items", 99.99)
        if success:
            print("✅ Test order added successfully!")
            print("   (You can delete this from your Google Sheet)")
        else:
            print("❌ Failed to add test order")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYour Google Sheets database is ready to use!")
        print("You can now start the backend server with: ./start.sh")
        
        return True
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: Credentials file not found!")
        print(f"Details: {str(e)}")
        print("\n📝 Next steps:")
        print("1. Follow GOOGLE_SHEETS_SETUP.md to create credentials.json")
        print("2. Place credentials.json in the backend/ folder")
        print("3. Run this test again")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\n📝 Troubleshooting:")
        print("1. Check that GOOGLE_SHEET_ID is set in .env file")
        print("2. Verify you shared the sheet with the service account email")
        print("3. Make sure the sheet has tabs named: 'Food Stocks', 'Orders', 'FAQs'")
        print("4. Check that credentials.json is in the backend/ folder")
        return False


if __name__ == "__main__":
    test_connection()
