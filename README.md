# Code Review AI Project

## Overview
This project is a FastAPI-based web application that integrates with GitHub and OpenAI’s GPT to automate code reviews. 
The application fetches code from a given GitHub repository, analyzes it using GPT, and returns feedback, 
including code comments, ratings, and conclusions.

## Features
- **FastAPI Backend**: Serves as the main API framework for the application.
- **Integration with GitHub**: Fetches code from GitHub repositories for analysis.
- **OpenAI GPT Integration**: Uses GPT-4 to provide detailed code review comments and suggestions.
- **Redis Caching**: Caches analysis results to improve performance and reduce repeated calls to the GPT API.
- **Dockerized Environment**: Ensures easy setup and deployment using Docker and Docker Compose.

## Project Structure
```
project-root/
|-- app/
|   |-- api/
|   |   |-- routes.py
|   |-- core/
|   |-- models/
|   |-- services/
|   |   |-- github_service.py
|   |   |-- gpt_service.py
|   |   |-- cache_service.py
|-- tests/
|-- pyproject.toml
|-- poetry.lock
|-- Dockerfile
|-- docker-compose.yml
|-- README.md
```

## Prerequisites
- **Docker**: Ensure Docker is installed and running.
- **Poetry**: Used for Python dependency management (handled during Docker build).
- **Git**: Required to clone the project and manage GitHub integration.

## Installation and Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd project-root
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the project root with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   GITHUB_TOKEN=your_github_token
   REDIS_URL=redis://redis:6379/0
   ```

3. **Build and Run the Application**:
   Use Docker Compose to build and start the services:
   ```bash
   docker-compose up --build
   ```

   This will:
   - Build the FastAPI application.
   - Set up Redis for caching.

4. **Access the Application**:
   The FastAPI application will be available at:
   ```
   http://localhost:8000
   ```

## Usage
- **POST /review**: Endpoint to submit a GitHub repository URL and receive an automated code review.
- Example payload:
  ```json
  {
    "github_repo_url": "https://github.com/user/repository",
    "assignment_description": "Create a Python Library for downloading a folder in a GitHub repository.",
    "candidate_level": "Junior"
  }
  ```
- **Response**:
  ```json
  {
    "found_files": ["file1.py", "file2.py"],
    "comments": "Detailed code review comments.",
    "rating": "4 out of 5",
    "conclusion": "Overall, the code quality is satisfactory with minor improvements suggested."
  }
  ```

## Troubleshooting Tips
- **Poetry Not Found**: Ensure the `PATH` includes Poetry’s bin directory.
- **Docker Build Failures**: Check for unsupported Python versions or missing dependencies.
- **Redis Connection Issues**: Verify that Redis is running and accessible at `REDIS_URL`.

## Future Enhancements
- Expand support for additional programming languages.
- Integrate more comprehensive testing and CI/CD pipelines.
- Enhance caching strategies for even faster responses.

## Contributing
Contributions are welcome! Fork the repository and submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any inquiries or support, reach out to [your-email@example.com].

