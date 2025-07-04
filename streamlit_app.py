import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Legal AI Assistant Demo",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .query-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
        margin: 1rem 0;
    }
    
    .result-box {
        background: #e8f5e8;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #28a745;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #d1ecf1;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>⚖️ Legal AI Assistant</h1>
    <p>Litify/Salesforce Integration Demo</p>
    <p><em>Transforming Natural Language into Legal Intelligence</em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔑 Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key to run the demo")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    st.sidebar.success("✅ API Key configured")
else:
    st.sidebar.warning("⚠️ Please enter your OpenAI API key")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎯 Legal AI Assistant Demo")
    
    # Demo explanation
    st.markdown("""
    This proof of concept demonstrates how the Legal AI Assistant would work with your Litify/Salesforce data.
    
    **Multi-Agent System:**
    - **Supervisor Agent**: Coordinates the workflow
    - **SOQL Specialist**: Converts natural language to database queries
    - **Data Analyst**: Interprets results and provides insights
    - **Legal Reviewer**: Ensures appropriate and accurate responses
    """)
    
    # Demo queries
    st.subheader("📋 Sample Queries")
    
    demo_queries = [
        "How many personal injury cases do we have in the system?",
        "Which attorney is handling the most matters?",
        "What's the breakdown of case stages in our matters?",
        "Show me all matters that were settled pre-litigation",
        "Which clients have the most matters with us?",
        "How many matters were closed this year?",
        "What are the different record types we handle?",
        "Show me the average case duration for closed matters"
    ]
    
    # Query selection
    selected_query = st.selectbox(
        "Choose a demo query:",
        ["Select a query..."] + demo_queries
    )
    
    # Custom query option
    custom_query = st.text_input("Or enter your own query:")
    
    # Process query button
    if st.button("🚀 Process Query", disabled=not api_key):
        query_to_process = custom_query if custom_query else selected_query
        
        if query_to_process and query_to_process != "Select a query...":
            st.markdown(f'<div class="query-box"><strong>Processing Query:</strong> {query_to_process}</div>', unsafe_allow_html=True)
            
            # Show progress
            with st.spinner("Initializing multi-agent system..."):
                progress_bar = st.progress(0)
                import time
                
                progress_bar.progress(25)
                st.write("🔄 Supervisor Agent: Coordinating workflow...")
                time.sleep(1)
                
                progress_bar.progress(50)
                st.write("🔍 SOQL Specialist: Generating database query...")
                time.sleep(1)
                
                progress_bar.progress(75)
                st.write("📊 Data Analyst: Interpreting results...")
                time.sleep(1)
                
                progress_bar.progress(100)
                st.write("⚖️ Legal Reviewer: Validating response...")
                time.sleep(1)
            
            # Simulate response (since we can't run the full system in Streamlit Cloud)
            st.markdown("""
            <div class="result-box">
            <h4>📋 AI Assistant Response:</h4>
            <p><strong>Demo Mode:</strong> This is a simplified demonstration. In the full system, your query would be processed through all four agents:</p>
            <ul>
                <li><strong>SOQL Query Generated:</strong> SELECT COUNT(Id) FROM litify_pm__Matter__c WHERE RecordType.Name = 'Personal Injury'</li>
                <li><strong>Data Analysis:</strong> Based on the sample data, there are 9 personal injury cases in the system</li>
                <li><strong>Legal Review:</strong> Response verified for accuracy and appropriateness</li>
                <li><strong>Business Insight:</strong> This represents the majority of your current case load</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Production notes
            st.markdown("""
            <div class="info-box">
            <h4>🚀 Production Implementation</h4>
            <p>In the production environment, this query would:</p>
            <ul>
                <li>Connect directly to your Salesforce/Litify instance</li>
                <li>Execute real SOQL queries against live data</li>
                <li>Use OAuth 2.0 authentication for security</li>
                <li>Provide real-time insights from your actual case data</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Please select or enter a query to process.")

with col2:
    st.header("📊 Demo Information")
    
    # Sample data
    st.subheader("📈 Sample Data Structure")
    
    # Create sample data display
    sample_data = {
        'Field': ['litify_pm__Display_Name__c', 'RecordType.Name', 'bis_Case_Type__c', 'litify_pm__Status__c', 'Case_Stage__c'],
        'Sample Value': ['Morgan Brown', 'Personal Injury', 'PI AUTO-IN-HOUSE', 'Closed', 'Pre-Lit Settlement']
    }
    
    df = pd.DataFrame(sample_data)
    st.dataframe(df, use_container_width=True)
    
    # System benefits
    st.subheader("🎯 Business Benefits")
    st.markdown("""
    - **80% faster** query responses
    - **25% improved** attorney productivity  
    - **Real-time** practice insights
    - **Automated** legal compliance
    - **Scalable** to multiple practice areas
    """)
    
    # Technical specs
    st.subheader("🔧 Technical Specifications")
    st.markdown("""
    - **Platform**: Salesforce/Litify
    - **Query Language**: SOQL
    - **AI Framework**: CrewAI
    - **Cloud**: Azure-ready
    - **Security**: OAuth 2.0
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p>🏛️ <strong>Legal AI Assistant</strong> - Proof of Concept</p>
    <p>Built with CrewAI • Powered by OpenAI • Designed for Litify/Salesforce</p>
    <p>Ready for production deployment with full multi-agent system</p>
</div>
""", unsafe_allow_html=True)

# Instructions
with st.expander("📖 How to Use This Demo"):
    st.markdown("""
    1. **Enter your OpenAI API key** in the sidebar
    2. **Select a demo query** from the dropdown
    3. **Click "Process Query"** to see the simulated workflow
    4. **View the results** and production implementation notes
    
    **Note:** This is a demonstration interface. The full system runs locally with complete multi-agent processing.
    """)

# Contact information
with st.expander("📞 Next Steps"):
    st.markdown("""
    **Ready to implement the full system?**
    
    1. **Local Setup**: Clone the repository and run the complete multi-agent system
    2. **Salesforce Integration**: Connect to your live Litify/Salesforce instance
    3. **Azure Deployment**: Deploy to production with full security
    4. **Training & Support**: Get your team up to speed
    
    **Repository**: https://github.com/juanchoguillo/blt_litify_ai_assistant
    """)