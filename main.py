import streamlit as st
from llama_index.core.llms import ChatMessage
from llama_index.llms.ollama import Ollama
from llama_index.core.prompts import PromptTemplate
import logging
import time

logging.basicConfig(level=logging.INFO)

# Database-specific context
bigquery_context = """
### BigQuery Schema: thelook_ecommerce

#### Table: users
- user_id (INT64): Unique identifier for the user.
- first_name (STRING): First name of the user.
- last_name (STRING): Last name of the user.
- email (STRING): Email address of the user.
- country (STRING): Country of the user.
- created_at (TIMESTAMP): Date and time the user was created.

#### Table: products
- product_id (INT64): Unique identifier for the product.
- name (STRING): Product name.
- category (STRING): Category of the product.
- price (FLOAT64): Price of the product.
- inventory (INT64): Number of items in stock.

#### Table: orders
- order_id (INT64): Unique identifier for the order.
- user_id (INT64): ID of the user who made the order.
- product_id (INT64): ID of the purchased product.
- quantity (INT64): Quantity of the product ordered.
- total_price (FLOAT64): Total price of the order.
- order_date (TIMESTAMP): Date and time of the order.

### Use BigQuery syntax in responses:
- Use `STRING` for text fields.
- Use `TIMESTAMP` for datetime fields.
- Use `CAST()` for type conversions.
- Use `STRUCT` and `ARRAY` for nested fields.
"""

redshift_context = """
### Redshift Schema: thelook_ecommerce

#### Table: users
- user_id (INTEGER): Unique identifier for the user.
- first_name (VARCHAR): First name of the user.
- last_name (VARCHAR): Last name of the user.
- email (VARCHAR): Email address of the user.
- country (VARCHAR): Country of the user.
- created_at (TIMESTAMP): Date and time the user was created.

#### Table: products
- product_id (INTEGER): Unique identifier for the product.
- name (VARCHAR): Product name.
- category (VARCHAR): Category of the product.
- price (NUMERIC): Price of the product.
- inventory (INTEGER): Number of items in stock.

#### Table: orders
- order_id (INTEGER): Unique identifier for the order.
- user_id (INTEGER): ID of the user who made the order.
- product_id (INTEGER): ID of the purchased product.
- quantity (INTEGER): Quantity of the product ordered.
- total_price (NUMERIC): Total price of the order.
- order_date (TIMESTAMP): Date and time of the order.

### Use Redshift syntax in responses:
- Use `VARCHAR` for text fields.
- Use `TIMESTAMP` for datetime fields.
- Use `::` for type casting (e.g., `field::VARCHAR`).
- Use `DISTKEY` and `SORTKEY` for optimization hints.
"""

# Prompt template with dynamic context
template = """
You are a SQL assistant helping with queries for a data warehouse. 
Use the provided schema context and follow the syntax rules for the selected database.

### Context:
{context}

### Question:
{query}
"""

# Initialize chat history in session state if not already present
if 'messages' not in st.session_state:
    st.session_state.messages = []

#Tab Label
st.set_page_config(page_title="TextQL")

# Sidebar for model and dialect selection
st.sidebar.title("Settings")
model = st.sidebar.selectbox("Choose a model", ["llama3.2", "mistral"])
dialect = st.sidebar.radio("Select SQL Dialect", ["BigQuery", "Redshift"])
# Sidebar for model selection and notes
st.sidebar.title("Notes & Information")

# Repository, your name, application purpose, and reference to original product
st.sidebar.markdown("""
**Author:** Ethan Chandler  
**Purpose:** This application allows users to input natural language questions, which are then converted into SQL queries for databases such as BigQuery and Redshift. It uses LLMs to generate accurate SQL syntax based on user queries.

### Key Features:
- Conversational interface for querying databases.
- Automatically switches between BigQuery and Redshift SQL dialects.
- Streamlined LLM integration for fast query generation.
""")

# Dynamically select the context based on the dialect
context = bigquery_context if dialect == "BigQuery" else redshift_context

# Create the prompt template
prompt_template = PromptTemplate(template)
def format_prompt(query):
    return prompt_template.format(context=context, query=query)

# Function to stream chat response based on selected model
def stream_chat(model, messages):
    try:
        llm = Ollama(model=model, request_timeout=120.0)
        
        # Inject dialect-specific context into the first message
        query = messages[-1]["content"]
        formatted_query = format_prompt(query)

        # Stream chat responses from the model
        resp = llm.stream_chat([ChatMessage(role="user", content=formatted_query)])
        
        response = ""
        response_placeholder = st.empty()
        
        for r in resp:
            response += r.delta
            response_placeholder.write(response)
        
        logging.info(f"Model: {model}, Dialect: {dialect}, Query: {query}, Response: {response}")
        return response
    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        raise e

# Main app logic
def main():
    st.title("TextQL")
    
    # Display current dialect
    st.sidebar.markdown(f"**Current Dialect:** `{dialect}`")

    # Prompt for user input
    if prompt := st.chat_input("Your SQL-related question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Generate response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                start_time = time.time()

                with st.spinner("Writing..."):
                    try:
                        # Stream the LLM response
                        response_message = stream_chat(model, st.session_state.messages)
                        duration = time.time() - start_time

                        # Add the assistant's response to the chat history
                        st.session_state.messages.append({"role": "assistant", "content": response_message})
                        st.write(f"Duration: {duration:.2f} seconds")

                    except Exception as e:
                        st.error("An error occurred while generating the response.")
                        logging.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
