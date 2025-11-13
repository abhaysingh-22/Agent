// Get DOM elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');

// API endpoint
const API_URL = 'http://localhost:8000/chat';

// Message storage
let messageHistory = [];

// Load messages from localStorage
function loadMessages() {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
        messageHistory = JSON.parse(saved);
        // Clear current messages except the initial greeting
        const initialMessage = chatMessages.querySelector('.message');
        chatMessages.innerHTML = '';
        if (messageHistory.length === 0 && initialMessage) {
            chatMessages.appendChild(initialMessage);
        } else {
            messageHistory.forEach(msg => {
                addMessageToDOM(msg.content, msg.isUser);
            });
        }
    }
}

// Save messages to localStorage
function saveMessages() {
    localStorage.setItem('chatHistory', JSON.stringify(messageHistory));
}

// Add message to DOM only
function addMessageToDOM(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'agent-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add message to chat (with persistence)
function addMessage(content, isUser = false) {
    messageHistory.push({ content, isUser, timestamp: Date.now() });
    saveMessages();
    addMessageToDOM(content, isUser);
}

// Add typing indicator
function addTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent-message typing-indicator';
    messageDiv.id = 'typingIndicator';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<span></span><span></span><span></span>';
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Send message to backend
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, true);
    
    // Clear input
    userInput.value = '';
    
    // Show typing indicator
    addTypingIndicator();
    
    // Disable input while processing
    userInput.disabled = true;
    sendButton.disabled = true;
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Add agent response
        addMessage(data.reply);
        
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        addMessage('Sorry, I encountered an error. Please make sure the backend is running on http://localhost:8000');
    } finally {
        // Re-enable input
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault(); // Prevent any form submission
        sendMessage();
    }
});

// Clear chat functionality
const clearButton = document.getElementById('clearButton');
clearButton.addEventListener('click', () => {
    if (confirm('Are you sure you want to clear the chat history?')) {
        messageHistory = [];
        localStorage.removeItem('chatHistory');
        chatMessages.innerHTML = '';
        // Add back the initial greeting
        addMessageToDOM('Hello! Welcome to our restaurant. How can I help you today?', false);
    }
});

// Load saved messages on page load
loadMessages();

// Focus input on load
userInput.focus();