# 🏥 MediBlaze AI - Advanced Medical Assistant

MediBlaze is an intelligent AI-powered medical assistant that provides comprehensive health information through a modern web interface. It combines medical knowledge base retrieval (RAG) with real-time web search to deliver accurate, up-to-date health guidance.

## ✨ Features

### 🧠 **AI-Powered Health Assistant**

- Advanced medical knowledge base with RAG (Retrieval Augmented Generation)
- Real-time web search for latest medical information
- Smart tool selection - uses RAG first, web search when needed
- Comprehensive health domain coverage

### 🎯 **Health Domains Covered**

- **Diseases & Conditions**: Symptoms, causes, diagnosis, complications
- **Treatments & Medications**: Therapies, drug information, side effects
- **Preventive Health**: Lifestyle changes, diet, exercise, wellness
- **Sexual Health & Education**: Reproductive health, contraception, STI prevention
- **Mental Health**: Stress management, emotional well-being
- **Nutrition**: Dietary guidance, eating habits, food safety
- **Body Changes**: Growth, aging, hormonal changes
- **Health Safety**: First aid, injury prevention

### 💻 **Modern Web Interface**

- Real-time streaming responses with markdown rendering
- Tool usage indicators ("Thinking...", "Searching web...")
- Responsive design with beautiful UI/UX
- Professional medical styling with health emojis

### 🔧 **Technical Features**

- FastAPI backend with async streaming
- LangGraph agent workflow
- Google Gemini AI integration
- Pinecone vector database for RAG
- Real-time Server-Sent Events (SSE)
- Markdown to HTML rendering

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google AI API Key
- Pinecone API Key

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd __MEDIBLAZE
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
   Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_ai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

4. **Run the application**

```bash
python main.py
```

5. **Access the interface**
   Open your browser and navigate to: `http://localhost:8000`

## 🐳 Docker Deployment

### Build and run with Docker

```bash
# Build the image
docker build -t mediblaze .

# Run the container
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your_key \
  -e PINECONE_API_KEY=your_key \
  mediblaze
```

### Docker Compose (Recommended)

```bash
# Create docker-compose.yml with your environment variables
docker-compose up -d
```

## 📁 Project Structure

```
__MEDIBLAZE/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── .env                   # Environment variables (create this)
├── README.md              # This file
│
├── agent/                 # AI Agent components
│   ├── agent.py          # LangGraph agent workflow
│   └── utils/
│       ├── prompt.py     # System prompts and instructions
│       └── tools.py      # RAG and web search tools
│
├── templates/             # Frontend templates
│   └── index.html        # Main web interface
│
├── static/               # Static assets
│   ├── styles.css       # Custom CSS styles
│   ├── doctor-avatar.png # AI assistant avatar
│   └── user-avatar.png   # User avatar
│
└── Data/                 # Knowledge base
    └── Book.pdf         # Medical knowledge source
```

## 🔧 API Endpoints

### **GET /**

Main web interface

### **POST /chat**

Standard chat endpoint

```json
{
  "message": "What are the symptoms of diabetes?"
}
```

### **POST /chat/stream**

Streaming chat with real-time responses

```json
{
  "message": "How to manage stress naturally?"
}
```

### **GET /health**

Health check endpoint

### **GET /docs**

Interactive API documentation

## 🧠 How It Works

### Smart Tool Selection Process:

1. **RAG First**: Searches medical knowledge base for foundational information
2. **Evaluate**: Determines if RAG information is complete and current
3. **Web Search**: Only used when RAG is insufficient for:
   - Recent medical developments
   - Specific lifestyle advice not in knowledge base
   - Current medication information
   - Sexual health education topics
   - Detailed procedures and guidelines

### Response Format:

All responses follow a structured medical format:

```markdown
## 🏥 [Topic Title with Health Emoji]

[Brief overview explaining the topic]

**🎯 Key Points:**

- Point 1 with specific health details
- Point 2 with relevant information
- Point 3 with important facts

**💊 Treatment/Management:**

- Primary treatment approaches
- Lifestyle recommendations
- Prevention strategies

---

> ⚠️ **Important**: Consult healthcare professionals for personalized advice.
```

## 🛡️ Important Disclaimers

- **Educational Purpose Only**: MediBlaze provides educational health information, not medical diagnosis
- **Not Emergency Care**: For medical emergencies, contact emergency services immediately
- **Consult Professionals**: Always consult qualified healthcare professionals for personalized medical advice
- **No Diagnosis**: This tool does not replace professional medical consultation

## 🔐 Environment Variables

| Variable           | Description                      | Required |
| ------------------ | -------------------------------- | -------- |
| `GOOGLE_API_KEY`   | Google AI (Gemini) API key       | Yes      |
| `PINECONE_API_KEY` | Pinecone vector database API key | Yes      |

## 🧪 Testing

### Test the application with curl:

```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the symptoms of diabetes?"}'

# Streaming endpoint
curl -N "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"message": "How to maintain good oral hygiene?"}'
```

### Example Questions to Try:

- "What are the symptoms of diabetes?"
- "How to manage stress naturally?"
- "What foods are good for heart health?"
- "How to maintain good oral hygiene?"
- "What are the benefits of regular exercise?"
- "How to improve sleep quality?"

## 🔄 Development

### Adding New Health Topics:

1. Update knowledge base in `Data/` directory
2. Modify system prompt in `agent/utils/prompt.py`
3. Test with various health queries

### Customizing UI:

- Modify `templates/index.html` for layout changes
- Update `static/styles.css` for styling
- Add new avatars in `static/` directory

## 📝 License

This project is for educational and informational purposes. Please ensure compliance with medical information regulations in your jurisdiction.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:

- Check the [API documentation](http://localhost:8000/docs)
- Review the health check endpoint
- Ensure all environment variables are set correctly

---

**⚠️ Medical Disclaimer**: This AI assistant provides educational health information only. Always consult qualified healthcare professionals for medical advice, diagnosis, and treatment. In case of medical emergency, contact emergency services immediately.
