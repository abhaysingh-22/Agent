# 🍽️ Restaurant Agent - AI-Powered Restaurant Assistant

An intelligent restaurant assistant built with FastAPI, LangGraph, and Google Sheets as a database. The agent helps customers browse menus, place orders, check order status, and answer FAQs - all powered by OpenAI's GPT models and real-time Google Sheets integration.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-green)
![LangChain](https://img.shields.io/badge/LangChain-0.3.9-orange)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.53-purple)

## ✨ Features

- 🤖 **AI-Powered Assistant**: Uses OpenAI GPT-4.1-mini with LangGraph for intelligent conversations
- 📊 **Google Sheets Database**: Real-time menu, orders, and FAQs management
- 🍛 **Indian Restaurant Focus**: Specialized personality for Indian cuisine with ₹ (INR) pricing
- 🔒 **Boundary Control**: Refuses non-restaurant topics (programming, general knowledge, etc.)
- 💬 **Chat Interface**: Beautiful responsive frontend with message persistence
- 🛠️ **Multiple Tools**: Menu lookup, stock checking, order management, FAQ search
- 🚀 **Auto-Restart**: Automatically kills old processes and restarts cleanly

## 🏗️ Architecture

```
Agent/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main FastAPI application
│   ├── agents/             # LangGraph agent logic
│   │   ├── graph.py        # Agent state graph
│   │   └── tools.py        # Agent tools (menu, orders, FAQs)
│   ├── utils/              # Utility modules
│   │   ├── logger.py       # Logging utilities
│   │   └── sheets_db.py    # Google Sheets integration
│   ├── models/             # Data models
│   │   └── menu.json       # Local menu backup
│   ├── requirements.txt    # Python dependencies
│   ├── start.sh           # Startup script
│   └── .env.example       # Environment template
└── frontend/               # Chat interface
    ├── index.html         # Main HTML
    ├── script.js          # Frontend logic
    └── style.css          # Styling
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- OpenAI API Key
- Google Cloud Service Account (for Sheets API)
- Google Sheet with 3 tabs: `Stocks`, `Orders`, `FAQs`

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/restaurant-agent.git
cd restaurant-agent
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `backend/.env`:

```env
OPENAI_API_KEY=sk-your-actual-openai-key
PORT=8000
GOOGLE_SHEET_ID=your-google-sheet-id
GOOGLE_CREDENTIALS_PATH=credentials.json
```

### 4. Set Up Google Sheets

Follow the detailed guide in [`GOOGLE_SHEETS_SETUP.md`](GOOGLE_SHEETS_SETUP.md):

1. Create Google Cloud project
2. Enable Google Sheets API
3. Create service account
4. Download `credentials.json` → Place in `backend/` folder
5. Create Google Sheet with tabs: `Stocks`, `Orders`, `FAQs`
6. Share sheet with service account email

**Sample Google Sheets Structure:**

**Stocks Tab:**
| Dish Name | Price (INR) |
|-----------|-------------|
| Paneer Butter Masala | 180 |
| Dal Makhani | 150 |
| Chole Bhature | 120 |

See [`SHEETS_TEMPLATE.md`](SHEETS_TEMPLATE.md) for complete sample data.

### 5. Test Connection

```bash
cd backend
source venv/bin/activate
python test_sheets.py
```

You should see:
```
✅ Successfully connected to Google Sheets!
✅ ALL TESTS PASSED!
```

### 6. Start Backend

```bash
cd backend
./start.sh
```

Backend will be available at: `http://localhost:8000`

### 7. Open Frontend

Simply open `frontend/index.html` in your browser, or serve it:

```bash
cd frontend
python3 -m http.server 8080
```

Then visit: `http://localhost:8080`

## 🎯 Agent Capabilities

### ✅ What the Agent CAN Do:

- Greet customers with Indian hospitality ("Namaste! 🍛")
- Show menu from Google Sheets (real-time data)
- Check food stock availability
- Take and manage orders
- Search and answer FAQs
- Provide food recommendations
- Handle inquiries about timings, delivery, payments

### ❌ What the Agent WON'T Do:

- Answer programming/tech questions
- Provide general knowledge (definitions, facts)
- Discuss non-restaurant topics
- Give personal advice unrelated to food

**Example Interaction:**

```
User: "Define polymorphism"
Agent: "I apologize, but I'm specifically designed to help with our 
       restaurant services only. I can assist you with our menu, 
       orders, timings, and food-related questions. How may I help 
       you with that?"
```

## 🛠️ Available Tools

1. **`lookup_menu()`** - Get menu items from Google Sheets
2. **`check_food_stock(item_name)`** - Check ingredient availability
3. **`get_order_status(order_id, status_filter)`** - View orders
4. **`place_order(customer_name, items, total)`** - Create orders
5. **`search_faqs(query, category)`** - Search FAQs
6. **`update_food_stock(item_name, quantity)`** - Update inventory

## 📝 API Endpoints

### POST `/chat`

Send a message to the agent.

**Request:**
```json
{
  "message": "Show me the menu"
}
```

**Response:**
```json
{
  "reply": "Here is the menu:\n- Paneer Butter Masala: ₹180\n...",
  "success": true
}
```

## 🔧 Configuration

### Auto-Restart Feature

The `start.sh` script automatically:
- Checks for processes on port 8000
- Kills existing processes
- Starts fresh backend instance

No more port conflicts! 🎉

### Message Persistence

Frontend automatically saves chat history to localStorage. Messages persist across page refreshes.

## 📚 Documentation

- [`GOOGLE_SHEETS_SETUP.md`](GOOGLE_SHEETS_SETUP.md) - Detailed Google Sheets setup
- [`SHEETS_TEMPLATE.md`](SHEETS_TEMPLATE.md) - Sample data for Google Sheets
- [`QUICK_START_SHEETS.md`](QUICK_START_SHEETS.md) - Quick reference guide

## 🧪 Testing

```bash
# Test Google Sheets connection
cd backend
source venv/bin/activate
python test_sheets.py

# Test API endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me the menu"}'
```

## 🔐 Security Notes

⚠️ **IMPORTANT**: Never commit these files:
- `.env` - Contains your OpenAI API key
- `credentials.json` - Contains Google service account keys

These are already in `.gitignore`, but always verify before pushing!

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent workflow
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [OpenAI](https://openai.com/) - GPT models
- [Google Sheets API](https://developers.google.com/sheets/api) - Database integration

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/restaurant-agent](https://github.com/yourusername/restaurant-agent)

---

Made with ❤️ and 🍛 by [Your Name]
