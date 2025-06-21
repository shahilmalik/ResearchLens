> [!IMPORTANT]  
> There are two versions of the project that differ in the backend implementation. The first version (main branch) uses
the Object Relational Mapper (ORM) from Django to interact with the database, which is a convenient way to interact with
the database using Python objects. This means, that you can define your database schema using Python classes and Django
will handle the SQL queries for you. For instance, if you would like to get all papers, ORM executes a SQL query in the 
background to select all papers and outputs a list of Paper objects. However, the goal of the course and project is to
learn how to use databases and to write SQL queries directly. Therefore, the second version (custom-queries branch) does
not use Django ORM, but instead uses raw SQL queries to interact with the database. Both versions have the same functionality, however, they cannot use the same database.

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

5. Access the frontend at [http://localhost:3000](http://localhost:3000) and backend at [http://localhost:8000](http://localhost:8000) in your browser.


6. Start the scraping process by clicking on the button in the frontend. This will scrape the arXiv website for scientific documents and store them in the database.

## Technologies Used

### Database

#### Schema
The project uses PostgreSQL as the database management system. The database runs in a Docker container for an easy setup
and will be automatically created and configured when the application is started. The database schema is defined via the models in
[`backend/researchlens/models.py`](backend/researchlens/models.py) file.

#### Insertions and Queries
We use Django's Object Relational Mapper (ORM) to interact with the database in the main branch.

### XML
The API from arXiv provides the data in XML format. We use the `xml.etree.ElementTree` module from Python's standard library
to parse the XML data and extract the relevant information. The code for parsing the XML data is implemented in
[`backend/researchlens/tasks.py`](backend/researchlens/tasks.py).

### Extensions
We use several small extensions to enhance the functionality of the project:
- pgvector: A library to store and query vectors in PostgreSQL. We use it to store the embeddings (vectors of size 384) of the documents in the database.
- Cascade delete: We use `ON DELETE CASCADE` in the database schema to automatically delete related rows when a row is deleted. This is useful to keep the database clean and avoid unused rows. 
- datatype JSON: We use the JSON data type to store the keywords of the documents in the database. This is convenient to store
  the keywords as a list of strings and query them easily.
- Django ORM: In the main branch, we use Django's Object Relational Mapper (ORM) to interact with the database. This allows us to define the database schema using Python classes and provides a convenient way to query the database using Python objects. This is useful for large projects where you want to avoid writing raw SQL queries and instead use Python objects to interact with the database. However, for the purpose of this course and project, we also provide a version that uses raw SQL queries to interact with the database (see custom-queries branch).