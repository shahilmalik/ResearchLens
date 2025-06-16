# Text Technology Project at University of Stuttgart: ResearchLens: Scraping, Storing, and Analyzing Scholarly Information

The project "ResearchLens: Scraping, Storing, and Analyzing Scholarly Information" aims to provide
a tool to find, analyze, and visualize scientific articles or documents from arXiv based on their title,
abstracts, and metadata.

## Features

- Collecting a set of scientific documents
- Search for scientific documents and get related documents

## Setup

1. Clone the repository with the following command:
```bash
https://github.com/shahilmalik/ResearchLens.git
cd ResearchLens
```

2. Create a `.env` file in the root directory of the project with the database credentials. For example:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=researchlens
```

3. Build the containers with the following command:
```bash
docker compose build
```

4. Run the application with the following command:
```bash
docker compose up
```

5. The backend can be accessed at `http://localhost:8000`.
