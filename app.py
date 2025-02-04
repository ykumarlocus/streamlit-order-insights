import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    file_path = "Order Data (For Data Studio) - ShipFlex.csv"
    df = pd.read_csv(file_path)
    
    # Convert date columns to datetime
    date_columns = ["Order Date", "COMPLETED AT", "CANCELLED AT"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

df = load_data()

# Function to process user queries
def query_insights(user_query):
    user_query = user_query.lower()

    if "total orders" in user_query:
        return f"Total number of orders: {df.shape[0]}"

    elif "completed orders" in user_query:
        completed_orders = df[df["Terminal STATUS"] == "COMPLETED"].shape[0]
        return f"Total completed orders: {completed_orders}"

    elif "canceled orders" in user_query:
        canceled_orders = df[df["Terminal STATUS"] == "CANCELLED"].shape[0]
        return f"Total canceled orders: {canceled_orders}"

    elif "best carrier" in user_query or "highest sla compliance" in user_query:
        best_carrier = df[df["SLA Compliance"] == "ON_TIME"]["CARRIER NAME"].value_counts().idxmax()
        return f"Carrier with the highest SLA compliance: {best_carrier}"

    elif "average delivery time" in user_query:
        df_filtered = df.dropna(subset=["Order Date", "COMPLETED AT"])
        df_filtered["Delivery Time"] = (df_filtered["COMPLETED AT"] - df_filtered["Order Date"]).dt.total_seconds() / 3600
        avg_delivery_time = df_filtered["Delivery Time"].mean()
        return f"Average delivery time: {round(avg_delivery_time, 2)} hours"

    elif "most common cancellation reason" in user_query:
        common_reason = df["Cancellation REASON DESCRIPTION"].dropna().value_counts().idxmax()
        return f"Most common cancellation reason: {common_reason}"

    elif "top city for orders" in user_query:
        top_city = df["CITY"].value_counts().idxmax()
        return f"City with the most orders: {top_city}"

    elif "top state for orders" in user_query:
        top_state = df["STATE"].value_counts().idxmax()
        return f"State with the most orders: {top_state}"

    elif "orders per month" in user_query:
        df["Month"] = df["Order Date"].dt.strftime('%Y-%m')
        orders_per_month = df["Month"].value_counts().sort_index()
        fig, ax = plt.subplots()
        orders_per_month.plot(kind='bar', title="Orders Per Month", ax=ax)
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Orders")
        ax.set_xticklabels(orders_per_month.index, rotation=45)
        st.pyplot(fig)
        return "Orders per month plotted."

    return "Sorry, I couldn't understand your query. Try asking about orders, cancellations, delivery times, etc."

# Streamlit UI
st.title("📊 AI-Powered Order Insights")
st.write("Ask a question about your order data, and I'll provide insights!")

user_query = st.text_input("Type your question here:", "")

if st.button("Get Answer"):
    if user_query:
        result = query_insights(user_query)
        st.write(result)
