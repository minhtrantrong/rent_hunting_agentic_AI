# Rent Hunting Agentic AI 🏠🤖

An intelligent AI agent system designed to assist with rent hunting and property search tasks. This project leverages advanced AI models and custom tools to automate and enhance the rental property search experience.

## Features

- **AI-Powered Agent**: Utilizes Google's Gemini model for intelligent conversation and task automation
- **Email Integration**: Send automated emails with calendar event links using SMTP
- **Calendar Integration**: Generate calendar links for property viewings and appointments
- **MCP (Model Context Protocol) Framework**: Extensible server architecture for custom tools
- **Database Storage**: SQLite-based agent session management
- **Multi-Model Support**: Configurable AI model selection through YAML configuration

## Project Structure

```
hackathon_rent_hunting_agentic_AI/
├── app.py                    # Main application entry point
├── email_server.py          # Email MCP server implementation
├── calendar_utils.py        # Calendar link generation utilities
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── models/                 # AI model configuration
│   ├── client_model.py     # Model loading and configuration
│   ├── config.yaml         # Model parameters and settings
│   └── __init__.py
├── mcp_tools/              # MCP framework implementation
│   ├── framework.py        # Core MCP framework
│   ├── cli.py             # Command-line interface
│   └── __init__.py
└── tmp/                    # Temporary files and database
    └── agent.db           # SQLite database for agent sessions
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd hackathon_rent_hunting_agentic_AI
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys and email credentials:
   ```bash
   # LLM API 
   OPENAI_API_KEY="your_openai_key"
   GOOGLE_API_KEY="your_google_api_key"

   # Email Configuration (Gmail App Password)
   EMAIL_USERNAME="your_email@gmail.com"
   EMAIL_PASSWORD="your_app_password"
   ```

## Configuration

### AI Model Configuration

The AI models are configured in `models/config.yaml`. The system currently supports Google's Gemini model with customizable parameters:

- Temperature control for response creativity
- Model version selection
- Custom system instructions

### Email Configuration

Email functionality uses Gmail SMTP by default. To enable email features:

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password for the application
3. Add your credentials to the `.env` file

## Usage

### Running the Application

```bash
python app.py
```

The application will:
- Load the configured AI model (Gemini by default)
- Initialize MCP servers for email and calendar functionality
- Start an interactive agent session

### Key Features

#### Email Integration
The agent can send emails with calendar event integration:
- Property viewing confirmations
- Appointment scheduling
- Follow-up communications
- Calendar invites for property tours

#### Calendar Integration
Automatically generate calendar links for:
- Google Calendar
- Outlook
- Apple Calendar
- ICS file downloads

#### Extensible Architecture
The MCP (Model Context Protocol) framework allows for easy addition of new tools and capabilities.

## Dependencies

### Core Dependencies
- `agno`: AI agent framework
- `google-genai`: Google Gemini API integration
- `python-dotenv`: Environment variable management
- `requests`: HTTP client library
- `beautifulsoup4`: Web scraping utilities
- `pandas`: Data manipulation and analysis

## Development

### Adding New Tools

1. Create a new MCP server by extending `MCPServer`
2. Register the server with the `MCPRegistry`
3. Implement custom tools as methods with proper typing

### Testing

Run the test files to verify functionality:

```bash
python test_agent.py          # Test basic agent functionality
python test_mcp_send_email.py # Test email server functionality
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key | Yes |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI models) | Optional |
| `EMAIL_USERNAME` | Gmail username for email functionality | Optional |
| `EMAIL_PASSWORD` | Gmail app password for email functionality | Optional |

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Model Loading Errors**: Ensure your API keys are correctly set in the `.env` file
2. **Email Functionality**: Verify Gmail app password and 2FA are properly configured
3. **Database Issues**: Delete `tmp/agent.db` to reset the agent session database

### Debug Mode

Set environment variables for additional debugging:
```bash
export DEBUG=1
```

## Architecture

The system is built on a modular architecture:

- **Agent Layer**: Handles AI model interactions and conversation flow
- **MCP Layer**: Provides extensible tool framework for custom functionality  
- **Service Layer**: Email, calendar, and database services
- **Configuration Layer**: YAML-based model and service configuration

This architecture enables easy extension and customization for specific rent hunting workflows and requirements.