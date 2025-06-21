> [!IMPORTANT]  
> There are two versions of the project that differ in the backend implementation. The first version (main branch) uses
the Object Relational Mapper (ORM) from Django to interact with the database, which is a convenient way to interact with
the database using Python objects. This means, that you can define your database schema using Python classes and Django
will handle the SQL queries for you. For instance, if you would like to get all papers, ORM executes a SQL query in the 
background to select all papers and outputs a list of Paper objects. However, the goal of the course and project is to
learn how to use databases and to write SQL queries directly. Therefore, the second version (custom-queries branch) does
not use Django ORM, but instead uses raw SQL queries to interact with the database. Both versions have the same functionality.

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

5. The frontend can be accessed at `http://localhost:3000` and backend at `http://localhost:8000`.
