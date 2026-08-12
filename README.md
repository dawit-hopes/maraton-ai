# Maraton AI 🏨🤖

**Maraton AI** is an AI-powered hotel chatbot designed to help guests get quick, natural-language answers about hotel services, facilities, policies, and other frequently asked questions.

The project uses **Retrieval-Augmented Generation (RAG)** to ground AI responses in hotel-specific information rather than relying solely on the model's general knowledge.

## ✨ Features

* 🤖 AI-powered hotel assistant
* 🔎 Retrieval-Augmented Generation (RAG)
* 📚 Hotel knowledge base
* 💬 Natural-language conversations
* 🏨 Answers about hotel services, facilities, and policies
* ⚡ Context-aware responses

## 🏗️ How It Works

```text
                    Guest
                      │
                      ▼
                ┌───────────┐
                │  Chatbot  │
                └─────┬─────┘
                      │
                      ▼
              ┌───────────────┐
              │   RAG System  │
              └───────┬───────┘
                      │
             ┌────────┴────────┐
             ▼                 ▼
      Knowledge Base       AI Model
             │                 │
             └────────┬────────┘
                      ▼
                Hotel Response
```

The chatbot retrieves relevant information from the hotel's knowledge base and provides it as context to the AI model before generating a response.

## 🛠️ Technology

* **Python**
* **LangChain**
* **RAG**
* **LLMs**
* **Vector embeddings**
* **Vector database**

## 🎯 Goal

The goal of Maraton AI is to make hotel information more accessible to guests through a conversational interface, reducing the need to navigate menus, search through documents, or repeatedly ask hotel staff common questions.

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/dawit-hopes/maraton-ai.git
cd maraton-ai
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables and AI provider credentials, then run the application using the project's configured entry point.

## 📄 License

See the `LICENSE` file for licensing information.
