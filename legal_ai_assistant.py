import os
import sqlite3
import pandas as pd
from crewai import Agent, Task, Crew, Process
from crewai_tools import NL2SQLTool
from langchain.llms import OpenAI
from typing import Dict, Any
import csv
from pathlib import Path

class LegalAIAssistant:
    def __init__(self, csv_file: str = "litify_matters.csv", db_path: str = "legal_matters.db"):
        self.csv_file = csv_file
        self.db_path = db_path
        self.setup_database_from_csv()
        self.nl2sql_tool = NL2SQLTool(db_uri=f"sqlite:///{db_path}")
        
    def setup_database_from_csv(self):
        """Initialize SQLite database from CSV file with exact Litify structure"""
        # Create CSV file if it doesn't exist
        if not Path(self.csv_file).exists():
            self.create_sample_csv()
        
        # Read CSV and create database
        try:
            df = pd.read_csv(self.csv_file)
            
            # Create database connection
            conn = sqlite3.connect(self.db_path)
            
            # Create table with Litify field names (matching your exact structure)
            create_table_query = """
            CREATE TABLE IF NOT EXISTS litify_pm__Matter__c (
                Id TEXT PRIMARY KEY,
                litify_pm__Display_Name__c TEXT,
                litify_pm__Client__r TEXT,
                litify_pm__Client__r_bis_Full_Formatted_Name__c TEXT,
                RecordType TEXT,
                RecordType_Name TEXT,
                bis_Case_Type__c TEXT,
                litify_pm__Status__c TEXT,
                Case_Stage__c TEXT,
                Case_Sub_Stage__c TEXT,
                litify_pm__Open_Date__c TEXT,
                litify_pm__Closed_Date__c TEXT,
                Primary_Legal_Assistant__r TEXT,
                bis_Attorney_Name__c TEXT,
                Primary_Legal_Assistant__r_Name TEXT
            )
            """
            
            conn.execute(create_table_query)
            
            # Insert data from CSV
            for _, row in df.iterrows():
                conn.execute("""
                    INSERT OR REPLACE INTO litify_pm__Matter__c VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(row.fillna('')))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Database created successfully from {self.csv_file}")
            print(f"📊 Loaded {len(df)} records")
            
        except Exception as e:
            print(f"❌ Error setting up database: {e}")
            raise
    
    def create_sample_csv(self):
        """Create the sample CSV file with your exact data structure"""
        csv_content = """Id,litify_pm__Display_Name__c,litify_pm__Client__r,litify_pm__Client__r.bis_Full_Formatted_Name__c,RecordType,RecordType.Name,bis_Case_Type__c,litify_pm__Status__c,Case_Stage__c,Case_Sub_Stage__c,litify_pm__Open_Date__c,litify_pm__Closed_Date__c,Primary_Legal_Assistant__r,bis_Attorney_Name__c,Primary_Legal_Assistant__r.Name
2ed7148386a56d1db9,Morgan Brown,[Account],Morgan Taylor,[RecordType],Billable Matter,WC WC-IN-HOUSE,Closed,Active,,7/21/23,8/31/23,,Taylor Miller,Riley Lee
77934fca56ba4bd509,Avery Taylor,[Account],Jordan Johnson,[RecordType],Personal Injury,PI AUTO-IN-HOUSE MINOR,Closed,Closed,,7/21/23,9/22/23,,Riley Wilson,Morgan Brown
34a706be1613efd297,Avery Wilson,[Account],Avery Wilson,[RecordType],Personal Injury,PI AUTO-IN-HOUSE,Closed,Pre-Lit Settlement,,7/25/23,3/6/24,,Morgan Taylor,Riley Brown
366b94b5409a51fb68,Morgan Davis,[Account],Jordan Johnson,[RecordType],Personal Injury,PI AUTO-IN-HOUSE,Closed,Closed,,7/22/23,9/8/23,,Taylor Davis,Morgan Miller
e804667b98067fa9ea,Morgan Smith,[Account],Alex Lee,[RecordType],Personal Injury,PI AUTO-IN-HOUSE,Closed,Closed,,7/22/23,8/31/23,,Jordan Davis,Avery Smith
ef911165c148f2a077,Riley Davis,[Account],Casey Miller,[RecordType],Personal Injury,PI AUTO-IN-HOUSE,Closed,Closed,,7/24/23,12/7/23,,Jamie Smith,Taylor Taylor
1183a7eb188081cec9,Taylor Wilson,[Account],Taylor Miller,[RecordType],Personal Injury,PI AUTO-IN-HOUSE,Closed,Closed,,7/22/23,9/8/23,,Riley Miller,Alex Davis
5751485a59c7062197,Alex Davis,[Account],Taylor Lee,[RecordType],Personal Injury,PI AUTO-IN-HOUSE,Closed,Pre-Lit Settlement,,7/22/23,1/22/24,,Riley Lee,Alex Taylor
e94b89a4e1ce6e8626,Morgan Smith,[Account],Morgan Davis,[RecordType],Personal Injury,PI AUTO-IN-HOUSE,Closed,Closed,,7/23/23,4/3/24,,Riley Wilson,Taylor Johnson
0ab59367dd16c0a1e9,Alex Lee,[Account],Riley Miller,[RecordType],Personal Injury,PI AUTO-IN-HOUSE,Closed,Pre-Lit Settlement,,7/24/23,6/7/24,,Casey Johnson,Jamie Smith"""
        
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            f.write(csv_content)
        
        print(f"✅ Sample CSV created: {self.csv_file}")
        
    def simulate_salesforce_query(self, soql_query: str) -> dict:
        """Simulate Salesforce API response format"""
        # This simulates how the production system would work with real Salesforce API
        print(f"🔄 Simulating Salesforce SOQL Query: {soql_query}")
        
        # In production, this would be:
        # response = requests.get(f"{sf_instance_url}/services/data/v58.0/query", 
        #                        params={"q": soql_query}, 
        #                        headers={"Authorization": f"Bearer {access_token}"})
        
        # For demo, we'll convert to SQLite and return Salesforce-like format
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert SOQL to SQLite (simplified for demo)
            sqlite_query = soql_query.replace("litify_pm__Matter__c", "litify_pm__Matter__c")
            
            cursor.execute(sqlite_query)
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            
            # Format like Salesforce API response
            records = []
            for row in results:
                record = {
                    "attributes": {
                        "type": "litify_pm__Matter__c",
                        "url": f"/services/data/v58.0/sobjects/litify_pm__Matter__c/{row[0]}"
                    }
                }
                for i, col in enumerate(columns):
                    record[col] = row[i]
                records.append(record)
            
            response = {
                "totalSize": len(records),
                "done": True,
                "records": records
            }
            
            conn.close()
            return response
            
        except Exception as e:
            print(f"❌ Error simulating Salesforce query: {e}")
            return {"totalSize": 0, "done": True, "records": []}
        
    def create_agents(self):
        """Create the specialized agents for the legal AI system"""
        
        # Supervisor Agent
        supervisor_agent = Agent(
            role='Legal Query Supervisor',
            goal='Coordinate and oversee the legal query processing pipeline for Litify/Salesforce data',
            backstory="""You are an experienced legal technology supervisor who ensures 
            that legal queries are processed efficiently and accurately through the proper channels.
            You understand both the technical aspects of Salesforce/Litify integration and legal workflows.""",
            verbose=True,
            allow_delegation=True
        )
        
        # SQL Query Agent (SOQL for Salesforce)
        sql_agent = Agent(
            role='SOQL Query Specialist',
            goal='Transform natural language queries into accurate SOQL queries for Litify/Salesforce database',
            backstory="""You are a Salesforce database specialist with expertise in Litify legal data structures. 
            You understand how legal matter data is organized in Salesforce and can translate business questions 
            into precise SOQL queries. You work specifically with litify_pm__Matter__c objects and related fields.
            You know the Litify field naming conventions and relationship structures.""",
            tools=[self.nl2sql_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Data Analysis Agent
        data_agent = Agent(
            role='Legal Data Analyst',
            goal='Analyze Salesforce query results and provide meaningful insights about legal matters',
            backstory="""You are a legal data analyst who specializes in interpreting 
            Litify/Salesforce legal case data, understanding matter statuses, case types, and legal processes. 
            You understand the structure of Salesforce responses and can provide clear, actionable insights 
            from legal database queries. You're familiar with Litify's case management workflow.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Legal Review Agent
        legal_review_agent = Agent(
            role='Legal Context Reviewer',
            goal='Review responses for legal accuracy and appropriateness',
            backstory="""You are a legal expert who reviews AI-generated responses about 
            legal matters to ensure they are accurate, appropriate, and don't contain 
            misleading legal advice. You understand legal terminology, case management processes,
            and the importance of maintaining attorney-client privilege and ethical boundaries.""",
            verbose=True,
            allow_delegation=False
        )
        
        return {
            'supervisor': supervisor_agent,
            'sql_specialist': sql_agent,
            'data_analyst': data_agent,
            'legal_reviewer': legal_review_agent
        }
    
    def create_tasks(self, agents: Dict[str, Agent], user_query: str):
        """Create tasks for processing the user query"""
        
        # Task 1: SOQL Query Generation
        sql_task = Task(
            description=f"""
            Convert the following natural language query into a SOQL query for the Litify/Salesforce database:
            
            Query: "{user_query}"
            
            Database Schema (litify_pm__Matter__c object):
            - Id: Unique matter identifier
            - litify_pm__Display_Name__c: Matter display name
            - litify_pm__Client__r: Client relationship reference
            - litify_pm__Client__r.bis_Full_Formatted_Name__c: Full client name
            - RecordType: Record type reference
            - RecordType.Name: Record type name (e.g., "Personal Injury", "Billable Matter")
            - bis_Case_Type__c: Case type classification (e.g., "PI AUTO-IN-HOUSE", "WC WC-IN-HOUSE")
            - litify_pm__Status__c: Matter status (e.g., "Closed", "Active")
            - Case_Stage__c: Current case stage (e.g., "Active", "Closed", "Pre-Lit Settlement")
            - Case_Sub_Stage__c: Detailed case sub-stage
            - litify_pm__Open_Date__c: Matter open date
            - litify_pm__Closed_Date__c: Matter closed date
            - Primary_Legal_Assistant__r: Primary legal assistant reference
            - bis_Attorney_Name__c: Assigned attorney name
            - Primary_Legal_Assistant__r.Name: Primary legal assistant name
            
            Generate an accurate SOQL query that would work in production Salesforce environment.
            Execute the query against our demo database to retrieve the relevant data.
            
            Remember: In production, this would be a Salesforce SOQL query like:
            SELECT Id, litify_pm__Display_Name__c, bis_Case_Type__c, litify_pm__Status__c 
            FROM litify_pm__Matter__c 
            WHERE litify_pm__Status__c = 'Active'
            """,
            expected_output="SOQL query and the retrieved data results formatted like Salesforce API response",
            agent=agents['sql_specialist']
        )
        
        # Task 2: Data Analysis
        analysis_task = Task(
            description=f"""
            Analyze the Salesforce/Litify data retrieved from the SOQL query and provide a comprehensive answer 
            to the user's question: "{user_query}"
            
            The data comes from a Litify-powered legal practice management system built on Salesforce.
            
            Focus on:
            1. Direct answer to the user's question
            2. Relevant legal matter statistics or patterns
            3. Case status and stage information
            4. Attorney and staff workload insights
            5. Timeline analysis if relevant
            6. Any notable insights about the legal practice operations
            
            Present the information in a clear, business-friendly format that would be useful 
            for legal practice management and decision-making.
            
            Remember: This data represents real legal matters, so maintain appropriate professional tone.
            """,
            expected_output="Detailed analysis and business intelligence answer to the user's query",
            agent=agents['data_analyst'],
            context=[sql_task]
        )
        
        # Task 3: Legal Review
        review_task = Task(
            description=f"""
            Review the analysis and answer provided for the query: "{user_query}"
            
            This is data from a legal practice management system (Litify/Salesforce), so ensure that:
            1. The response is legally appropriate and doesn't provide legal advice
            2. Legal terminology is used correctly
            3. The information respects attorney-client privilege principles
            4. The response doesn't make inappropriate legal conclusions
            5. Any limitations or caveats are properly noted
            6. The response maintains professional legal industry standards
            
            Consider that this system will be used by legal professionals for practice management,
            not for providing legal advice to clients.
            
            Provide the final, reviewed response with any necessary corrections or clarifications.
            """,
            expected_output="Final, legally-reviewed response appropriate for legal practice management",
            agent=agents['legal_reviewer'],
            context=[analysis_task]
        )
        
        # Task 4: Supervision and Coordination
        supervision_task = Task(
            description=f"""
            Oversee the entire process of answering the user query: "{user_query}"
            
            This query was processed through our Litify/Salesforce integration simulation.
            
            Coordinate between all agents and ensure:
            1. The SOQL query was generated correctly for Salesforce environment
            2. The data analysis provides actionable legal practice insights
            3. The legal review ensures professional standards
            4. The final answer is complete and ready for production use
            
            Provide a summary of the process and the final answer that demonstrates how this 
            system would work in production with real Salesforce/Litify integration.
            
            Include a note about how this query would be executed in production:
            - Real Salesforce API endpoint: https://yourcompany.my.salesforce.com/services/data/v58.0/query
            - OAuth authentication required
            - SOQL query executed against live Litify data
            """,
            expected_output="Process summary and final coordinated response with production notes",
            agent=agents['supervisor'],
            context=[sql_task, analysis_task, review_task]
        )
        
        return [sql_task, analysis_task, review_task, supervision_task]
    
    def process_query(self, user_query: str):
        """Process a user query through the agent system"""
        
        # Create agents
        agents = self.create_agents()
        
        # Create tasks
        tasks = self.create_tasks(agents, user_query)
        
        # Create crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        return result

# Example usage
if __name__ == "__main__":
    # Initialize the legal AI assistant
    assistant = LegalAIAssistant()
    
    # Example queries that work with Litify data structure
    example_queries = [
        "How many personal injury cases are in the system?",
        "Which attorney is handling the most cases?",
        "What are the different case types we have?",
        "Show me all cases handled by Riley Wilson",
        "How many matters are closed vs active?",
        "What's the most common case stage?",
        "Which clients have multiple matters?",
        "Show me all pre-litigation settlements"
    ]
    
    print("Legal AI Assistant - Litify/Salesforce Integration Demo")
    print("=" * 60)
    print("🏛️  Simulating production Salesforce/Litify environment")
    print("📊 Using CSV data that matches Litify field structure")
    print("🔄 Demonstrates SOQL query generation and execution")
    
    while True:
        print("\nExample queries:")
        for i, query in enumerate(example_queries, 1):
            print(f"{i}. {query}")
        
        user_input = input("\nEnter your query number (1-8), custom query, or 'quit' to exit: ")
        
        if user_input.lower() == 'quit':
            break
            
        if user_input.isdigit() and 1 <= int(user_input) <= len(example_queries):
            query = example_queries[int(user_input) - 1]
        else:
            query = user_input
            
        print(f"\n🔍 Processing query: {query}")
        print(f"🏗️  Simulating Salesforce API call...")
        print("-" * 50)
        
        try:
            result = assistant.process_query(query)
            print(f"\n📋 Final Result:")
            print("=" * 50)
            print(f"{result}")
            print("\n🚀 Production Note:")
            print("In production, this would query live Salesforce/Litify data via:")
            print("- Salesforce REST API")
            print("- OAuth authentication")
            print("- Real-time SOQL execution")
            print("- Live legal matter data")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            print("💡 Make sure you have set up your OpenAI API key in the .env file")