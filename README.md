# Legal AI Assistant - CrewAI Proof of Concept

A sophisticated AI assistant system built with CrewAI that transforms natural language queries into SOQL queries for legal matter databases, specifically designed for Litify/Salesforce legal platforms.

## 🏛️ Overview

This proof of concept demonstrates an agentic AI system that:
- Converts natural language to SOQL queries using NL2SQL
- Analyzes Litify/Salesforce legal matter data intelligently
- Provides legally-appropriate responses
- Maintains quality through multi-agent review process
- Simulates production Salesforce API integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Git (for version control)

### Installation

1. **Clone or download the project files**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the demo setup:**
   ```bash
   python demo_script.py
   ```
   Choose option 3 for first-time setup.

4. **Configure your OpenAI API key:**
   - Edit the `.env` file created during setup
   - Replace `your_openai_api_key_here` with your actual API key

5. **Run the demo:**
   ```bash
   python legal_ai_assistant.py
   ```

## 🤖 Agent Architecture

The system uses 4 specialized agents:

### 1. **Supervisor Agent**
- **Role:** Coordinates the entire workflow
- **Responsibility:** Ensures quality and completeness of responses
- **Can delegate:** Yes

### 2. **SOQL Specialist Agent**
- **Role:** Natural Language to SOQL conversion
- **Tools:** NL2SQL Tool (adapted for Salesforce)
- **Responsibility:** Generate accurate SOQL queries from user questions

### 3. **Data Analyst Agent**
- **Role:** Interprets Salesforce query results
- **Responsibility:** Provides meaningful insights and business intelligence

### 4. **Legal Review Agent**
- **Role:** Legal accuracy validation
- **Responsibility:** Ensures responses are legally appropriate and don't provide legal advice

## 📊 Litify Database Schema

The system works with Litify/Salesforce legal matter data including:

| Litify Field | Description |
|--------------|-------------|
| `Id` | Unique matter identifier |
| `litify_pm__Display_Name__c` | Matter display name |
| `litify_pm__Client__r` | Client relationship reference |
| `litify_pm__Client__r.bis_Full_Formatted_Name__c` | Full client name |
| `RecordType.Name` | Matter classification (Personal Injury, Billable Matter, etc.) |
| `bis_Case_Type__c` | Legal case category (PI AUTO-IN-HOUSE, WC WC-IN-HOUSE, etc.) |
| `litify_pm__Status__c` | Current matter status (Active, Closed, etc.) |
| `Case_Stage__c` | Detailed case progression (Active, Closed, Pre-Lit Settlement) |
| `Case_Sub_Stage__c` | Sub-stage information |
| `litify_pm__Open_Date__c` | Matter open date |
| `litify_pm__Closed_Date__c` | Matter closed date |
| `bis_Attorney_Name__c` | Assigned attorney |
| `Primary_Legal_Assistant__r.Name` | Primary legal assistant |

## 🎯 Demo Queries

The system can handle Litify-specific queries like:
- "How many personal injury cases do we have in the system?"
- "Which attorney is handling the most matters?"
- "What's the breakdown of case stages in our matters?"
- "Show me all matters that were settled pre-litigation"
- "Which clients have the most matters with us?"
- "How many matters were closed this year?"
- "What are the different record types we handle?"
- "Show me the average case duration for closed matters"

## 🔧 Configuration

### Environment Variables (.env)
```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///legal_matters.db
CREWAI_TELEMETRY_OPT_OUT=true
```

### Sample Data Structure
The CSV file (`litify_matters.csv`) contains sample data with exact Litify field structure:
- 10 sample legal matters
- Personal Injury and Workers' Compensation cases
- Various case stages and attorney assignments
- Realistic timeline data

## 📈 Production Readiness

### Current Setup (POC)
- SQLite database simulating Litify data structure
- CSV file with authentic Litify field names
- OpenAI API integration
- SOQL query simulation

### Salesforce/Litify Production Migration Path
1. **API Integration:** Replace CSV with live Salesforce REST API calls
2. **Authentication:** Implement OAuth 2.0 for Salesforce
3. **SOQL Queries:** Convert from SQLite to native SOQL execution
4. **Real-time Data:** Connect to live `litify_pm__Matter__c` objects
5. **Azure Deployment:** Deploy to Azure App Service with Key Vault

### Production SOQL Examples
```sql
-- Count personal injury cases
SELECT COUNT(Id) FROM litify_pm__Matter__c 
WHERE RecordType.Name = 'Personal Injury'

-- Attorney workload analysis
SELECT bis_Attorney_Name__c, COUNT(Id) case_count 
FROM litify_pm__Matter__c 
GROUP BY bis_Attorney_Name__c 
ORDER BY COUNT(Id) DESC

-- Case pipeline analysis
SELECT Case_Stage__c, COUNT(Id) 
FROM litify_pm__Matter__c 
GROUP BY Case_Stage__c
```

## 🛠️ Customization

### Adding New Agents
1. Define agent in `agents.yaml`
2. Create agent instance in `create_agents()`
3. Add corresponding tasks
4. Update crew composition

### Extending Litify Schema
1. Modify `setup_database_from_csv()` method
2. Update SOQL generation prompts
3. Add new Litify custom fields
4. Adjust analysis agent context

### Adding New Tools
1. Import tool in main script
2. Assign to appropriate agent
3. Update agent configuration

## 🔍 Troubleshooting

### Common Issues

**"No module named 'crewai'"**
- Solution: `pip install crewai crewai-tools`

**"Could not find a version that satisfies the requirement sqlite3"**
- Solution: Remove `sqlite3` from requirements.txt (it's built-in to Python)

**"OpenAI API key not found"**
- Solution: Check `.env` file and API key format

**"Database connection failed"**
- Solution: Ensure SQLite database permissions and CSV file exists

**"Agent execution timeout"**
- Solution: Check API rate limits and network connection

## 📋 Next Steps

1. **Immediate (POC)**
   - Test with more complex Litify queries
   - Refine agent prompts for legal terminology
   - Add error handling for SOQL generation

2. **Short-term (Pre-production)**
   - Implement Salesforce Connected App
   - Add OAuth 2.0 authentication
   - Create REST API endpoints

3. **Long-term (Production)**
   - Full Salesforce/Litify integration
   - Azure deployment with security
   - Advanced legal analytics features

## 🚀 Production Integration

In production, the system will:
- Connect directly to Salesforce via REST API
- Execute real SOQL queries against `litify_pm__Matter__c`
- Use OAuth 2.0 authentication
- Process live legal matter data
- Provide real-time legal practice insights

**API Endpoint Example:**
```
GET https://yourcompany.my.salesforce.com/services/data/v58.0/query
?q=SELECT Id, litify_pm__Display_Name__c FROM litify_pm__Matter__c
```

## 🤝 Support

For technical issues or questions:
1. Check the troubleshooting section
2. Review agent logs for specific errors
3. Validate API key and database connections
4. Ensure CSV file matches Litify structure

## 📄 License

This is a proof of concept for demonstration purposes. Production use requires proper licensing and security review.