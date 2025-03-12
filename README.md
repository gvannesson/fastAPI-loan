# FastAPI Loan

FastAPI Loan is a RESTful API built with FastAPI that provides endpoints for loan prediction and related financial analysis. The project leverages modern Python technologies for high performance and scalability, making it a great choice for microservice-based financial applications.

## Features

Loan Prediction Endpoint: Submit loan application data and receive a prediction or risk analysis.  
Data Validation: Uses Pydantic for robust request data validation.  
High Performance: Built with FastAPI to offer asynchronous, high-throughput processing.  
Interactive API Documentation: Auto-generated Swagger UI and ReDoc documentation available at /docs and /redoc.  
Containerized: Docker support for easy deployment across various cloud platforms, including Azure.

## Prerequisites

- Python 3.9+  
- pip  
- Virtual environment tool (e.g., venv or virtualenv)

## Installation

### Clone the Repository

```bash
git clone https://github.com/gvannesson/fastAPI-loan.git
cd fastAPI-loan
```

### Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

The application relies on environment variables for configuration. Create a `.env` file in the root directory (or use your preferred method for managing environment variables) and set values for keys such as:

```dotenv
SECRET_KEY=your_secret_key_here
DATABASE_URL=your_database_connection_url_here
```

Other environment variables as needed.  
Note: The project is configured to load these variables using tools like `python-dotenv`.

## Running the Application

Start the development server using Uvicorn:

```bash
uvicorn main:app --reload
```

This command will start the server on http://127.0.0.1:8000/. With `--reload` enabled, changes in your code will automatically restart the server.

## API Endpoints

The API provides several endpoints, including:

### **GET /**
A welcome endpoint providing basic API info.

### **POST /api/loans/predict**
Accepts JSON payloads containing loan application data and returns a prediction.

Example request payload:

```json
{
  "state": "string",
  "term": 0,
  "no_emp": 0,
  "urban_rural": 0,
  "cat_activities": 0,
  "bank_loan_float": 0,
  "sba_loan_float": 0,
  "franchise_code": 0,
  "lowdoc": true,
  "bank": "string"
}
```

For a full list of endpoints and interactive documentation, visit http://127.0.0.1:8000/docs once the server is running.


## Docker Deployment

The project is containerized for easy deployment. To build and run the Docker container:

### Build the Docker Image

```bash
docker build -t fastapi-loan .
```

### Run the Container

```bash
docker run -d -p 8000:8000 fastapi-loan
```

Your API should now be accessible at http://localhost:8000/.

## Deployment on Azure

For deploying to Azure Container Instances (ACI) or another cloud platform, you can use the provided shell script deploy.sh along with environment variable management (e.g., through Docker Compose or Azure CLI). Make sure to adjust resource allocation and networking settings as needed for production workloads.

## Authors

Gauthier VANNESSON
https://github.com/gvannesson

Hacene ZERROUK
https://github.com/haceneZERROUK 

Samuel THOREZ-DEBRUCQ
https://github.com/SamuelTD

## License

MIT License

Copyright (c) [year] [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


