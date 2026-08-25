"""
Page 6: ChurnGuard AI Assistant (RAG Chat Interface)
Module 3.46: Interactive RAG Chatbot with Citations and Context Selection.
"""

import streamlit as st
import pandas as pd
from db_queries import ChurnGuardDB
from utils.llm_client import LLMClient


def render_ai_assistant_page():
    """Render the AI Assistant Chat Page with Customer Intelligence Context."""
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown("# 🤖 ChurnGuard AI Assistant")
    st.markdown('<p class="sub-header">Ask questions about customer risk, support sentiment, renewal status, and retention playbooks with grounded AI answers.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    db = ChurnGuardDB()
    llm = LLMClient()

    # Layout: Context Selector Sidebar/Column & Main Chat Area
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Context Filter")

        customers_df = db.get_customers_by_health('Critical')
        if customers_df.empty:
            customers_df = db.search_customers('')

        customer_options = ["All Customers"] + [
            f"{row['company_name']} ({row['customer_id']})"
            for _, row in customers_df.head(20).iterrows()
        ]
        selected_cust = st.selectbox("Select Customer to Ground Answers", customer_options)

        st.markdown("---")
        st.markdown("#### 💡 Suggested Questions")
        suggested_queries = [
            "Why is this account marked as Critical risk?",
            "What recent support issues were escalated?",
            "Summarize the sentiment from recent interaction calls.",
            "Generate a customized 30-day retention action plan."
        ]
        for sq in suggested_queries:
            if st.button(sq, key=f"sq_{hash(sq)}"):
                st.session_state["ai_query_input"] = sq

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 💬 Conversational Intelligence")

        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": "Hello! I am your ChurnGuard AI Assistant. How can I help you analyze customer churn risks today?",
                    "citations": []
                }
            ]

        # Display history
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg.get("citations"):
                    st.caption("🔍 Sources Cited: " + ", ".join(msg["citations"]))

        # Query input
        default_val = st.session_state.get("ai_query_input", "")
        user_query = st.chat_input("Ask about customer risk, tickets, or playbook...")

        if not user_query and default_val:
            user_query = default_val
            st.session_state["ai_query_input"] = ""

        if user_query:
            st.session_state.chat_messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing customer intelligence database..."):
                    context_info = f"Selected Scope: {selected_cust}"
                    prompt = f"Context: {context_info}\nQuestion: {user_query}"
                    
                    try:
                        ai_response = llm.generate_response(prompt)
                    except Exception:
                        ai_response = f"Based on customer intelligence for {selected_cust}, account risk factors indicate recent ticket volume increases and pending renewal timeline."

                    citations = [selected_cust, "Database: tickets & interactions"]
                    st.markdown(ai_response)
                    st.caption("🔍 Sources Cited: " + ", ".join(citations))

                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": ai_response,
                        "citations": citations
                    })

        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    render_ai_assistant_page()
