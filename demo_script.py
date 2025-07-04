#!/usr/bin/env python3
"""
Legal AI Assistant Demo Script
Easy setup and demonstration for customer presentation
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Setup the environment for the demo"""
    print("🚀 Setting up Legal AI Assistant Demo Environment")
    print("=" * 50)
    
    # Create .env file with sample configuration
    env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///legal_matters.db

# CrewAI Configuration
CREWAI_TELEMETRY_OPT_OUT=true
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment file created (.env)")
    print("⚠️  Please update your OpenAI API key in the .env file")
    
    # Create sample data CSV with exact Litify structure
    sample_csv = """Id,litify_pm__Display_Name__c,litify_pm__Client__r,litify_pm__Client__r.bis_Full_Formatted_Name__c,RecordType,RecordType.Name,bis_Case_Type__c,litify_pm__Status__c,Case_Stage__c,Case_Sub_Stage__c,litify_pm__Open_Date__c,litify_pm__Closed_Date__c,Primary_Legal_Assistant__r,bis_Attorney_Name__c,Primary_Legal_Assistant__r.Name
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
    
    with open('litify_matters.csv', 'w', newline='', encoding='utf-8') as f:
        f.write(sample_csv)
    
    print("✅ Litify matters CSV created (litify_matters.csv)")
    print("📊 Data matches exact Litify/Salesforce field structure")
    print("🔄 Ready for SOQL simulation")

def run_demo():
    """Run the demo with predefined queries"""
    print("\n🎯 Running Legal AI Assistant Demo")
    print("=" * 50)
    
    # Demo queries for customer presentation - Updated for Litify structure
    demo_queries = [
        {
            "query": "How many personal injury cases do we have in the system?",
            "description": "Count by case type - demonstrates Litify categorization"
        },
        {
            "query": "Which attorney is handling the most matters?",
            "description": "Attorney workload analysis - shows performance metrics"
        },
        {
            "query": "What's the breakdown of case stages in our matters?",
            "description": "Case pipeline analysis - demonstrates workflow insights"
        },
        {
            "query": "Show me all matters that were settled pre-litigation",
            "description": "Settlement analysis - shows case outcome filtering"
        },
        {
            "query": "Which clients have the most matters with us?",
            "description": "Client relationship analysis - demonstrates CRM insights"
        },
        {
            "query": "How many matters were closed this year?",
            "description": "Productivity metrics - shows temporal analysis"
        },
        {
            "query": "What are the different record types we handle?",
            "description": "Practice area overview - shows service categorization"
        },
        {
            "query": "Show me the average case duration for closed matters",
            "description": "Efficiency analysis - demonstrates time tracking"
        }
    ]
    
    print("🎯 Available Demo Queries (Litify/Salesforce Integration):")
    for i, demo in enumerate(demo_queries, 1):
        print(f"{i}. {demo['query']}")
        print(f"   📈 Business Value: {demo['description']}")
        print()
    
    # Initialize the assistant
    try:
        from legal_ai_assistant import LegalAIAssistant
        assistant = LegalAIAssistant(csv_file="litify_matters.csv")
        
        print("✅ Legal AI Assistant initialized with Litify data structure!")
        print("🔗 Simulating Salesforce/Litify API integration")
        print("\n" + "="*60)
        print("🚀 DEMO MODE - Litify/Salesforce Integration Proof of Concept")
        print("="*60)
        
        while True:
            print("\n🎯 Select a demo query (1-8) or enter 'custom' for your own:")
            choice = input("Choice (or 'quit' to exit): ").strip()
            
            if choice.lower() == 'quit':
                break
            elif choice.lower() == 'custom':
                query = input("Enter your custom query: ").strip()
                description = "Custom query for Litify data"
            elif choice.isdigit() and 1 <= int(choice) <= len(demo_queries):
                demo = demo_queries[int(choice) - 1]
                query = demo['query']
                description = demo['description']
            else:
                print("❌ Invalid choice. Please try again.")
                continue
            
            print(f"\n🔍 Processing Litify Query: {query}")
            print(f"📊 Business Purpose: {description}")
            print("🔄 Simulating Salesforce API call...")
            print("-" * 60)
            
            try:
                result = assistant.process_query(query)
                print(f"\n📋 AI Assistant Result:")
                print("=" * 60)
                print(f"{result}")
                
                print(f"\n🚀 Production Implementation Notes:")
                print("- Real Salesforce endpoint: https://yourcompany.my.salesforce.com/services/data/v58.0/query")
                print("- OAuth 2.0 authentication required")
                print("- SOQL query executed against live litify_pm__Matter__c objects")
                print("- Real-time legal matter data from Litify platform")
                print("- Secure API integration with proper error handling")
                
                print("\n" + "="*60)
                
                # Ask if they want to continue
                continue_demo = input("\n🔄 Continue with another query? (y/n): ").strip().lower()
                if continue_demo != 'y':
                    print("✅ Demo completed successfully!")
                    break
                    
            except Exception as e:
                print(f"❌ Error processing query: {e}")
                print("💡 Common issues:")
                print("  - Check OpenAI API key in .env file")
                print("  - Ensure all dependencies are installed")
                print("  - Verify CSV file structure matches Litify format")
                
    except ImportError as e:
        print("❌ Could not import LegalAIAssistant.")
        print(f"Error: {e}")
        print("🔧 Solution: Run 'pip install -r requirements.txt'")
        print("📋 Make sure all CrewAI dependencies are installed")

def main():
    """Main function to run the demo setup"""
    print("🏛️  Legal AI Assistant - CrewAI Proof of Concept")
    print("=" * 60)
    
    print("\nWhat would you like to do?")
    print("1. Setup demo environment")
    print("2. Run demo (requires setup first)")
    print("3. Both (recommended for first time)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        setup_environment()
    elif choice == '2':
        run_demo()
    elif choice == '3':
        setup_environment()
        print("\n" + "="*50)
        input("Press Enter to continue to demo...")
        run_demo()
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()