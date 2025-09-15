# Rent Hunting Agentic AI

An intelligent AI-powered system designed to streamline the apartment hunting process by automating property searches, scheduling viewings, and managing client communications.

## 🚀 Features

- **Intelligent Property Search**: Automated extraction of rental listings from various sources
- **Calendar Management**: Smart scheduling system for apartment viewings
- **Email Communication**: Automated email notifications and appointment confirmations
- **Database Integration**: TiDB integration for efficient data management
- **Multi-city Support**: Configurable city and country data extraction
- **Client Management**: Comprehensive client profile and preference tracking

## 📁 Project Structure

```
├── app.py                     # Main application entry point
├── calendar_utils.py          # Calendar and scheduling utilities
├── city_data_extractor.py     # City and location data extraction
├── email_server.py           # Email handling and SMTP server
├── tidb_customer_tool.py     # TiDB database operations
├── test_email_template.py    # Email template testing
├── data/                     # Data storage
│   └── country_and_city_urls.yaml
├── email_templates/          # HTML email templates
│   └── apartment_appointment.html
├── mcp_tools/               # MCP (Model Context Protocol) tools
│   ├── cli.py
│   └── framework.py
├── models/                  # Data models and configuration
│   ├── client_model.py
│   └── config.yaml
└── tmp/                     # Temporary files
    └── agent.db
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/minhtrantrong/rent_hunting_agentic_AI.git
   cd rent_hunting_agentic_AI
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration:
   - Database credentials (TiDB)
   - Email server settings
   - API keys for property search services
   - Other service configurations

## ⚙️ Configuration

### Database Setup
The application uses TiDB for data storage. Configure your database connection in the `.env` file:

```env
TIDB_HOST=your_tidb_host
TIDB_PORT=4000
TIDB_USER=your_username
TIDB_PASSWORD=your_password
TIDB_DATABASE=rent_hunting
```
### Import the prepared data to the TiDB database 'rent_hunting', at the table name 'rents'
From the TiDB web application, select Data > Import 
Select 'Upload a local file', then select the 'rents.csv' in the data directory
Data types: low_price and high_price columns are BIGINT(), others columns are VARCHAR(255)
Database name: rent_hunting
Table name: rents

### City Data Configuration
Modify `data/country_and_city_urls.yaml` to add or update supported cities and their data sources.

## 🚀 Usage

### Running the Main Application
```bash
python app.py
```

### Testing Email Templates
```bash
python test_email_template.py
```

### Testing Database Connection
```bash
python quick_db_test.py
```

### Using MCP Tools
```bash
python -m mcp_tools.cli
```

## 📧 Email Templates

The system includes customizable HTML email templates for:
- Apartment viewing appointments
- Property match notifications
- Booking confirmations

Templates are located in the `email_templates/` directory and can be customized to match your branding.

## 🗃️ Database Schema

The application uses the following key models:
- **Client Model**: Stores client information and preferences
- **Property Data**: Rental listing information
- **Appointments**: Scheduled viewing data
- **Communications**: Email and message logs

## 🔧 API Integration

The system supports integration with various property listing APIs and services. Configure API endpoints and authentication in the respective configuration files.

## 🤖 AI Capabilities

- **Natural Language Processing**: Understanding client preferences and requirements
- **Smart Matching**: AI-powered property recommendation engine
- **Automated Scheduling**: Intelligent calendar management
- **Communication Automation**: Context-aware email generation

## 📊 Monitoring and Logging

The application includes comprehensive logging for:
- Property search activities
- Client interactions
- Email communications
- System performance metrics

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

For email template testing:
```bash
python test_email_template.py
```

For database connection testing:
```bash
python quick_db_test.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation in the `docs/` directory

## 🙏 Acknowledgments

- TiDB for database infrastructure
- OpenAI for AI capabilities
- Contributors and beta testers

---

**Note**: This is a hackathon project focused on demonstrating AI-powered automation in the real estate rental market. The system is designed to be extensible and can be adapted for various rental markets and use cases.