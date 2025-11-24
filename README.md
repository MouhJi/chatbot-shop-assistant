# TMDT New 2 - E-commerce & RAG Chat Application

This is a full-stack e-commerce application integrated with a RAG (Retrieval-Augmented Generation) AI server to provide intelligent product inquiries. The project consists of three main components: a React frontend, a Node.js/Express backend, and a Python/FastAPI RAG server.

# Demo:

<img width="800" height="800" alt="image" src="https://github.com/user-attachments/assets/76444064-15c8-4273-bf4f-c423cd942a60" />



<img width="800" height="800" alt="image" src="https://github.com/user-attachments/assets/0553307d-e599-4de0-b810-90df66794b6e" />


##  Project Structure

- **client/**: Frontend application built with React and Vite.
- **server/**: Backend REST API built with Node.js and Express.
- **rag_server/**: AI Service for RAG functionality using FastAPI, ChromaDB, and Google Gemini.

##  Tech Stack

### Client
- **Framework**: React (Vite)
- **UI Libraries**: Ant Design, Material UI, Bootstrap
- **State/Data**: Axios, Context API (assumed)
- **Features**: Google OAuth, Charts (Chart.js), Rich Text Editor (TinyMCE)

### Server (Backend)
- **Runtime**: Node.js
- **Framework**: Express.js
- **Database**: MongoDB (Mongoose)
- **Authentication**: JWT, Google Auth
- **Services**: Cloudinary (Image Upload), Nodemailer (Email), VNPAY (Payments), Google Generative AI

### RAG Server (AI)
- **Framework**: FastAPI (Python)
- **Orchestration**: LangChain
- **Vector DB**: ChromaDB (via `langchain-chroma`)
- **Embeddings**: HuggingFace (via `langchain-huggingface`)
- **LLM**: Google Gemini (via `langchain-google-genai`)

##  Prerequisites

Before you begin, ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v18 or higher)
- [Python](https://www.python.org/) (v3.9 or higher)
- [MongoDB](https://www.mongodb.com/) (Local or Atlas connection string)

##  Installation & Setup

### 1. Backend Server Setup
Navigate to the `server` directory and install dependencies:

```bash
cd server
npm install
```

Create a `.env` file in the `server` directory with the following variables (example):
```env
PORT=5000
MONGO_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
GEMINI_API_KEY=your_gemini_api_key
# Add VNPAY and other configs as needed
```

### 2. RAG Server Setup
Navigate to the `rag_server` directory and install dependencies:

```bash
cd rag_server
pip install -r requirements.txt
```

Create a `.env` file in the `rag_server` directory:
```env
GEMINI_API_KEY=your_gemini_api_key
MONGO_URI=mongodb://localhost:27017
CHROMA_DB_PATH=./chroma_db
```

### 3. Client Setup
Navigate to the `client` directory and install dependencies:

```bash
cd client
npm install
```

Create a `.env` file in the `client` directory (if needed):
```env
VITE_API_URL=http://localhost:5000
VITE_RAG_API_URL=http://localhost:8000
```

##  Running the Application

You will need to run all three services simultaneously. It is recommended to use three separate terminal windows.

**Terminal 1: Backend Server**
```bash
cd server
npm start
```
*Runs on port 5000 (default)*

**Terminal 2: RAG Server**
```bash
cd rag_server
uvicorn main:app --reload --port 8000
```
*Runs on port 8000*

**Terminal 3: Client**
```bash
cd client
npm run dev
```
*Runs on http://localhost:5173 (default)*

##  Features

- **User Authentication**: Login/Register with Email or Google.
- **Product Management**: Browse, search, and view product details.
- **AI Chat Assistant**: Ask questions about products and get answers based on the product catalog (RAG).
- **Cart & Checkout**: Add items to cart and pay via VNPAY.
- **Admin Dashboard**: Manage products, users, and view statistics.

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
