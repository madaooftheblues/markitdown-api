# markitdown-api

A FastAPI wrapper around Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library that converts various file formats to Markdown. This API provides a secure, containerized solution for document conversion with simple HTTP endpoints.

## 🚀 Features

- **Wide Format Support**: Convert PowerPoint, Word, Excel, PDF, Images, Audio, HTML, CSV, JSON, XML, ZIP, EPub files and more
- **Secure Authentication**: Bearer token authentication for API security
- **RESTful API**: Simple HTTP POST endpoint for file conversion
- **Docker Ready**: Fully containerized with Docker support
- **Production Ready**: Includes health checks, logging, CORS, and file size limits
- **Easy Deployment**: Optimized for deployment with Coolify
- **Comprehensive Documentation**: Auto-generated API docs with Swagger UI

## 📋 Supported File Formats

- **Office Documents**: `.docx`, `.pptx`, `.xlsx`, `.xls`
- **PDF Files**: `.pdf`
- **Images**: `.jpg`, `.png`, `.gif`, `.bmp`, `.tiff` (with OCR support)
- **Audio Files**: `.wav`, `.mp3` (with speech transcription)
- **Web Formats**: `.html`, `.htm`
- **Data Formats**: `.csv`, `.json`, `.xml`
- **Archives**: `.zip` files (processes contents)
- **E-books**: `.epub`
- **YouTube**: Direct URL processing
- **And more...**

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (for containerization)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/madaooftheblues/markitdown-api.git
   cd markitdown-api
   ```

2. **Initialize the project with uv**
   ```bash
   uv init
   uv venv
   # Activate virtual environment
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   uv add fastapi uvicorn "markitdown[all]" python-multipart
   ```

4. **Configure environment variables**
   ```bash
   echo "API_TOKEN=your-super-secret-api-token-change-this" > .env
   ```

5. **Run the application**
   ```bash
   uv run uvicorn main:app --reload --host 0.0.0.0 --port 8003
   ```

The API will be available at `http://localhost:8003`

## 🐳 Docker Deployment

### Build and Run Locally

```bash
# Build the Docker image
docker build -t markitdown-api:latest .

# Run the container
docker run -d -p 8003:8003 \
  -e API_TOKEN=your-super-secret-api-token-change-this \
  --name markitdown-api \
  markitdown-api:latest
```

### Using Docker Compose

```bash
# Run with docker-compose
docker-compose up -d
```

## 🌐 Production Deployment with Coolify

1. **Push your code to a Git repository**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Configure Coolify**
   - Repository: Your Git repository URL
   - Branch: `main`
   - Build Pack: `Docker`
   - Port: `8003`

3. **Set Environment Variables in Coolify**
   - `API_TOKEN`: Your secure API token
   - `MAX_FILE_SIZE`: Maximum file size in MB (default: 50)

4. **Deploy**
   - Coolify will automatically build and deploy your application
   - SSL certificates are handled automatically

## 📖 API Usage

### Authentication

All endpoints (except health check) require Bearer token authentication:

```bash
Authorization: Bearer your-api-token-here
```

### Endpoints

#### Convert File to Markdown
```http
POST /convert
Content-Type: multipart/form-data
Authorization: Bearer your-api-token-here
```

**Parameters:**
- `file`: The file to convert (multipart/form-data)

**Response:**
```json
{
  "success": true,
  "filename": "document.docx",
  "file_size": 15234,
  "markdown": "# Document Title\n\nContent in markdown format...",
  "metadata": {
    "title": "Document Title",
    "content_length": 1234
  }
}
```

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "markitdown-api"
}
```

#### API Information
```http
GET /
```

Returns API information and supported formats.

### Example Usage

#### Using curl
```bash
# Convert a Word document
curl -X POST "http://localhost:8003/convert" \
  -H "Authorization: Bearer your-api-token-here" \
  -F "file=@document.docx"

# Convert a PDF file
curl -X POST "http://localhost:8003/convert" \
  -H "Authorization: Bearer your-api-token-here" \
  -F "file=@presentation.pdf"
```

#### Using Python requests
```python
import requests

url = "http://localhost:8003/convert"
headers = {"Authorization": "Bearer your-api-token-here"}
files = {"file": open("document.docx", "rb")}

response = requests.post(url, headers=headers, files=files)
result = response.json()

print(result["markdown"])
```

#### Using JavaScript/Node.js
```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

const form = new FormData();
form.append('file', fs.createReadStream('document.docx'));

const response = await axios.post('http://localhost:8003/convert', form, {
  headers: {
    ...form.getHeaders(),
    'Authorization': 'Bearer your-api-token-here'
  }
});

console.log(response.data.markdown);
```

## 🔧 Configuration

### Environment Variables

- `API_TOKEN`: Authentication token for API access (required)
- `MAX_FILE_SIZE`: Maximum file size in MB (default: 50)
- `PYTHONUNBUFFERED`: Set to 1 for better logging in containers

### File Size Limits

The default maximum file size is 50MB. You can adjust this by setting the `MAX_FILE_SIZE` environment variable:

```bash
export MAX_FILE_SIZE=100  # 100MB limit
```

## 📊 API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8003/docs`
- ReDoc: `http://localhost:8003/redoc`

## 🔒 Security Features

- **Bearer Token Authentication**: Secure API access
- **File Size Limits**: Prevent abuse with configurable limits
- **Non-root Container**: Docker container runs as non-root user
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Secure error responses without sensitive information

## 🚦 Health Monitoring

The API includes built-in health monitoring:

- **Health Endpoint**: `/health` for uptime monitoring
- **Docker Health Check**: Built-in container health checks
- **Logging**: Comprehensive logging for debugging and monitoring

## 🔧 Development

### Project Structure
```
markitdown-api/
├── main.py              # FastAPI application
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── pyproject.toml       # Python project configuration
├── uv.lock             # Dependency lock file
├── .env                # Environment variables (local)
├── .dockerignore       # Docker ignore file
├── .gitignore          # Git ignore file
└── README.md           # This file
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/madaooftheblues/markitdown-api/issues) page
2. Create a new issue if needed
3. For urgent matters, contact the maintainers

## 🙏 Acknowledgments

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) - The core document conversion library
- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
- [Coolify](https://coolify.io/) - Deployment platform

## 📈 Roadmap

- [ ] Rate limiting implementation
- [ ] Batch file processing
- [ ] Webhook support for async processing
- [ ] Additional output formats (HTML, etc.)
- [ ] Cloud storage integration (S3, etc.)
- [ ] Advanced OCR options
- [ ] Multi-language support for OCR

---

**Built with ❤️ using FastAPI and Microsoft MarkItDown**