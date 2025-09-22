# 🛩️ MCP Flight

MCP (Model Context Protocol) server for comprehensive flight search and travel planning using the Amadeus API.

## 🚀 Features

### 🔧 **MCP Tools**
- **`search_flights`**: Advanced flight search with comprehensive filters
  - Multi-passenger support (adults, children, infants)
  - Flexible date options (one-way, round-trip)
  - Travel class selection
  - Airline inclusion/exclusion
  - Price and currency filtering
  - Non-stop flight options
- **`search_cities`**: Intelligent city and airport lookup
  - Keyword-based search
  - Country filtering
  - Airport inclusion
  - Configurable result limits

### 📋 **Smart Prompts**
- **`vacation_prompt`**: Comprehensive vacation planning assistant
  - Destination-based recommendations
  - Budget-aware suggestions
  - Seasonal travel optimization
  - Interest-based activity planning
- **`flight_search_prompt`**: Targeted flight search guidance
  - Parameter-driven search assistance
  - Multi-criteria optimization
  - Flexible booking options

### 📚 **Travel Resources**
- **`file:///data/seasons_guide.txt`**: Regional travel seasons database
  - High/low season periods by region
  - Weather and crowd level insights
  - Cost optimization recommendations
- **`file:///data/documents_checklist.txt`**: International travel documentation
  - Region-specific requirements
  - Visa and insurance guidelines
  - Essential document checklists

### 🎨 **Template System**
- **Jinja2-powered templates** for dynamic prompt generation
- **Fallback mechanisms** for robust error handling
- **Customizable travel planning workflows**

## 🏗️ Architecture

Clean **Domain-Driven Design (DDD)** architecture with clear separation of concerns:

```
src/
├── domain/              # 🎯 Business Logic & Rules
│   ├── entities/        # Core business entities (Flight, City, Airport)
│   ├── vo/              # Value objects - Immutable value types (Coordinates, LocationCode)
│   ├── gateways/        # Abstract interfaces for external services
│   ├── services/        # Domain business logic
│   └── exceptions/      # Domain-specific exceptions
├── infrastructure/      # 🔧 External Integrations
│   ├── external/        # Amadeus API client & authentication
│   ├── gateways/        # Concrete gateway implementations
│   ├── config/          # Application configuration
│   └── container.py     # Dependency injection container
├── application/         # 📋 Use Cases & Orchestration
│   ├── services/        # Application services
│   └── dto/             # Data transfer objects
└── presentation/        # 🎨 MCP Interface Layer
    ├── mcp/             # MCP tools, prompts, resources
    └── templates/       # Jinja2 template files
```

## 📦 Installation

### Prerequisites
- **Python 3.12+**
- **uv** (recommended) or **pip**

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd mcp-flight

# Install dependencies (recommended)
uv sync

# Alternative: pip installation
pip install -e .
```

## 🔧 Configuration

### Amadeus API Setup
Configure your Amadeus API credentials using environment variables:

1. **Get Amadeus Credentials:**
   - Visit [Amadeus for Developers](https://developers.amadeus.com/)
   - Create a free account
   - Generate API key and secret

2. **Set Environment Variables:**
   ```bash
   # Required variables
   export AMADEUS_API_KEY="your_amadeus_api_key"
   export AMADEUS_API_SECRET="your_amadeus_api_secret"
   
   # Optional: API base URL (defaults to test environment)
   export AMADEUS_API_BASE="https://test.api.amadeus.com"
   ```

3. **Alternative: Use .env file:**
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env with your credentials
   nano .env
   ```

### Environment Variables Reference
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AMADEUS_API_KEY` | ✅ Yes | - | Your Amadeus API key |
| `AMADEUS_API_SECRET` | ✅ Yes | - | Your Amadeus API secret |
| `AMADEUS_API_BASE` | ❌ No | `https://test.api.amadeus.com` | API base URL (use `https://api.amadeus.com` for production) |

## 🚀 Usage

### Running the MCP Server
```bash
# Direct execution
python mcp_server.py

# With uv
uv run python mcp_server.py

# As installed package
mcp-flight
```

### MCP Client Integration
Add to your MCP client configuration (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "flight": {
      "command": "/home/user/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/path/to/mcp-flight",
        "mcp_server.py"
      ],
      "env": {
        "AMADEUS_API_KEY": "your_amadeus_api_key",
        "AMADEUS_API_SECRET": "your_amadeus_api_secret",
        "AMADEUS_API_BASE": "https://test.api.amadeus.com"
      }
    }
  }
}
```

**Configuration Options:**
- Replace `/path/to/mcp-flight` with the actual path to your project directory
- Set your Amadeus API credentials in the `env` section
- For production, change `AMADEUS_API_BASE` to `https://api.amadeus.com`

## 🛠️ Available MCP Components

### Tools
| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `search_flights` | Search flight offers | `origin_location_code`, `destination_location_code`, `departure_date`, `adults`, `return_date`, `max_price` |
| `search_cities` | Find cities and airports | `keyword`, `country_code`, `max_results`, `include` |

### Prompts
| Prompt | Description | Use Case |
|--------|-------------|----------|
| `vacation_prompt` | Vacation planning assistant | Complete trip planning with budget and preferences |
| `flight_search_prompt` | Flight search guidance | Targeted flight searches with specific criteria |

### Resources
| Resource | Description | Content |
|----------|-------------|---------|
| `file:///data/seasons_guide.txt` | Travel seasons by region | Optimal travel times, pricing insights |
| `file:///data/documents_checklist.txt` | Travel documentation | Visa, insurance, and document requirements |

## 🧪 Technology Stack

- **Python 3.12+** - Modern Python with latest type hints
- **FastMCP** - MCP server framework
- **HTTPX** - Async HTTP client for API calls
- **Jinja2** - Template engine for dynamic prompts
- **aiofiles** - Async file operations
- **Amadeus API** - Comprehensive travel data

## 📁 Project Structure

```
mcp-flight/
├── mcp_server.py           # 🚀 Main entry point
├── pyproject.toml          # 📦 Project configuration & dependencies
├── README.md               # 📖 This documentation
├── data/                   # 📊 Travel reference data
│   ├── seasons_guide.txt   # Regional travel seasons
│   └── documents_checklist.txt # Travel documentation guide
└── src/                    # 💻 Source code
    ├── domain/             # Business logic layer
    ├── infrastructure/     # External integrations
    ├── application/        # Use cases & orchestration
    └── presentation/       # MCP interface & templates
```

### Architecture Principles
- **Domain-Driven Design** for business logic clarity
- **Dependency Injection** for testability
- **Clean Architecture** for maintainability
- **Async/Await** for performance
- **Type Hints** for code safety

## 🌟 Key Benefits

- **🔍 Comprehensive Search**: Advanced flight and city search capabilities
- **🎯 Smart Planning**: AI-powered vacation planning assistance
- **📊 Data-Driven**: Seasonal insights and documentation guidance
- **🏗️ Scalable Architecture**: Clean DDD structure for easy extension
- **⚡ High Performance**: Async operations for fast responses
- **🛡️ Type Safe**: Full type coverage for reliability
---