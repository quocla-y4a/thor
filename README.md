Chatbot Puppy: AI Assistant for BI Team

**Chatbot Puppy** is an intelligent, professional, and friendly AI assistant designed to empower the Business Intelligence (BI) team. Built on the GPT-4o-mini core, Puppy efficiently answers internal knowledge queries and provides expert financial data analysis.

**Key Features**

**Internal Knowledge Consultant**:
- Answers questions based on documents stored in the knowledge_base/ folder (PDFs).
- Provides clear, complete, and accurate summaries, synthesizes information, and highlights key insights from internal documents.

**Financial Data Analyst (Google Sheet)**:
- Generates professional, data-driven commentary for financial and operational metrics (e.g., GMV, Net Sales, COGS, A&P).
- Compares performance against budget, YoY, and MoM trends.
- Explains what happened, why it happened, and its business implications.

General-Purpose Chat Assistant:
- Handles general queries not related to internal knowledge or financial data.
- Offers informative, polite, and engaging responses.

**How It Works**

Puppy intelligently determines the user's intent to activate the most relevant role:
- **Internal Knowledge Queries**: Searches and processes PDF files from the knowledge_base/ directory.
- **Financial Data Analysis**: Reads and analyzes structured data from a designated Google Sheet via read_data_gqs.py, providing expert commentary.
- **General Questions**: Responds using its broad knowledge base from the GPT-4o-mini model.
