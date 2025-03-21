# Local Natural Language to SQL LLM

## 🚀 **Local LLM-Powered SQL Query Generator**
This is a **local text-to-SQL converter** built using **Streamlit** and **Ollama**, powered by **Llama3.2**. It enables you to interact with your database schema using natural language prompts, generating accurate SQL queries in return.  
 
✅ **Key Benefits:**
- **Local Execution:** No need to share proprietary or sensitive data with external LLMs.  
- **Database-Aware:** Pre-configured for **BigQuery** and **Redshift** schemas, following their specific SQL dialects.  
- **Customizable:** Easily extend the schema and model selection to match your environment.  

💡 This tool is particularly useful when working with **confidential datasets** or **offline environments**, where external LLM access is restricted.

---

## 🛠️ **Setup Instructions**

### 1. **Install Ollama**
Download and install **Ollama** to run local LLMs:  
[Ollama Installation](https://ollama.com/download)
Make sure you have installed minstral and ollama3.2 libraries
(see ollama documentation)

### 2. **Clone the Repository**
```bash
git clone https://github.com/Ethanlchandler/local_textql
```

### 3. **Create and Activate a Virtual Environment**
On Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 5. **Run the Application**
```bash
streamlit run main.py
```

## 💡 **Possible Uses**
This tool can be extended or forked to suit various **data engineering** and **analytical** needs:

- **Data Exploration:**  
  Ask complex SQL questions in natural language to explore datasets without manually writing SQL.  

- **ETL Pipeline Testing:**  
  Quickly generate SQL queries for ETL validation by describing the logic in natural language.  

- **SQL Query Learning:**  
  Use it as an educational tool to learn SQL by converting plain questions into SQL syntax.  

- **Custom Database Support:**  
  Add support for more SQL dialects (PostgreSQL, Snowflake, etc.) by extending the schema context.  

- **Integration with CI/CD:**  
  Automate query generation as part of CI/CD pipelines to validate data changes.  

---

## 🛠️ **Tech Stack**
- **Language Model:** Llama3.2 (or Mistral) via Ollama  
- **Framework:** Streamlit  
- **Languages:** Python  
- **Databases:** BigQuery and Redshift  

---

## 👤 **Author**
**Ethan Chandler**  
- [GitHub](https://github.com/Ethanlchandler)  
- [LinkedIn](https://www.linkedin.com/in/ethan-chandler)  

---

✅ Let me know if you want further modifications, additional sections, or more details!

