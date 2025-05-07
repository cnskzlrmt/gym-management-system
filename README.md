# 🏋️ Gym Management System

A backend application for managing gym memberships, workouts, user roles, and AI-driven SQL query generation — built with FastAPI, Oracle DB, OpenAI integration, and LangChain.

## 🚀 Features

- 🔐 **Role-based access control** (Admin, Trainer, Member)
- 🏋️ **Workout program management**
- 💳 **Membership and payment tracking**
- 🧠 **AI-enhanced features** with OpenAI and LangChain for chatbot integration
- 🧑‍💼 **SQL query generation** based on user input, leveraging the schema of the Oracle database
- 🔐 **JWT authentication**
- ⚙️ **FastAPI-based REST API**
- ☁️ **Environment configuration via `.env`**

---

## 🧰 Tech Stack

- **Framework**: FastAPI
- **Database**: Oracle (via `oracledb`)
- **Auth**: JWT (with `python-jose`, `bcrypt`)
- **AI Integration**: OpenAI + LangChain (for chatbot and SQL generation)
- **Others**: `python-dotenv`, `faiss-cpu`, `uvicorn`

---

## 🛠️ Installation

```bash
# clone the repo
git clone https://github.com/cnskzlrmt/gym-management-system.git
cd gym-management-system

# create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# install dependencies
pip install -r requirements.txt
```

## 📂 .env File Example

```ini
DATABASE_URL=oracle://username:password@host:port/service_name
JWT_SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_key
```

⚠️ Make sure `.env` is listed in `.gitignore` and never pushed to GitHub.

## 📌 Run the App

```bash
uvicorn main:app --reload
```

The API will be available at: http://localhost:8000

## 🧠 AI-Powered SQL Query Generation

This project features an AI-powered chatbot that allows users to ask natural language questions about the gym's database, and the system will generate valid SQL queries based on the provided schema. The AI uses OpenAI and LangChain to interpret user input and interact with the Oracle database.

For instance, users can ask questions like:
- "What are the most popular workout programs?"
- "How many members signed up in the last month?"
- "What payments have been made for the 'Yoga' program?"

The system will process the questions, generate SQL queries using the predefined schema, and execute those queries on the Oracle database.

## 📎 Notes

- This project uses Oracle Database. You can run Oracle XE via Docker for local development.
- OpenAI and LangChain are included for AI features such as chatbots and SQL query generation.

## 📄 License

MIT License — feel free to use, modify, and build on it.
