> [!IMPORTANT]  
> There are two versions of the project that differ in the backend implementation. The first version (django-orm branch) uses
the Object Relational Mapper (ORM) from Django to interact with the database, which is a convenient way to interact with
the database using Python objects. This means, that you can define your database schema using Python classes and Django
will handle the SQL queries for you. For instance, if you would like to get all papers, ORM executes a SQL query in the 
background to select all papers and outputs a list of paper objects. However, the goal of the course and project is to
learn how to use databases and to write SQL queries directly. Therefore, the second version (current branch, main branch) does
not use Django ORM, but instead uses raw SQL queries to interact with the database. Both versions have the same functionality.

# Text Technology Project at University of Stuttgart: ResearchLens: Scraping, Storing, and Analyzing Scholarly Information

The project "ResearchLens: Scraping, Storing, and Analyzing Scholarly Information" aims to provide
a tool to find scientific articles or documents from arXiv based on text, publication date, and categories.
The application displays the results in a user-friendly way and, additionally, outputs related papers for each paper
in the search results.

## Features
ResearchLens provides the following features:
- Collecting a set of scientific documents from arXiv
- Storing the documents in a PostgreSQL database
- Compute keywords and embeddings for the documents and store them in the database
- Search for scientific documents based on text, publication date, and categories and display the results in a user-friendly way
- Display the keywords of the documents in the search results and get related documents based on the embeddings for each paper

## Setup
The application is built using Docker and Docker Compose, which allows for easy setup and deployment of the application
in a containerized environment. The application consists of a frontend and a backend, which communicate with each other
via a REST API. The frontend is built with React and the backend is built with Django. The application uses PostgreSQL
as the database management system to store the papers.

0. Install Docker and Docker Compose on your machine. You can find the installation instructions for your operating system
on the [Docker website](https://docs.docker.com/get-started/get-docker) and [Docker Compose documentation](https://docs.docker.com/compose/install).

1. Clone the repository with the following command:
```bash
git clone https://github.com/shahilmalik/ResearchLens.git
cd ResearchLens
```

2. Create a `.env` file in the root directory of the project with the database credentials. The credentials are used
when generating the database for the first time. For example:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=researchlens
```

3. Build the container images with the following command:
```bash
docker compose build
```

4. Run the application with the following command:
```bash
docker compose up
```

5. Access the frontend at [http://localhost:3000](http://localhost:3000) and backend at [http://localhost:8000](http://localhost:8000) in your browser.


6. Start the scraping process by clicking on the button in the frontend. This will scrape the arXiv website for scientific documents and store them in the database. If you use the application for the first time, it will take some time because the application downloads the deep learning models for computing the embeddings and keywords of the documents. Even after the first run, the scraping process can take some time, depending on the number of documents you want to scrape and process. Alternatively, you can import the data from the [`sql_exports`](sql_exports) directory, which contains some example data. This will speed up the process and you can start using the application immediately.

## Directories
The project is structured into several directories, each serving a specific purpose:
- `backend`: Contains the backend code, which is built with Django and provides the REST API. It includes the logic for scraping the arXiv website, storing the data in the database, and computing the embeddings and keywords for the documents.
- `frontend`: Contains the frontend code, which is built with React and provides the user interface
- `docker`: Contains the Dockerfiles for the backend, frontend, and database services
- `sql_exports`: Contains SQL files with exported data from the database. You can use these files to import data into the database
- `docker-compose.yml`: The Docker Compose file that defines the services, networks, and volumes for the application
- `.env`: The environment file that contains the database credentials and other environment variables

## Technologies Used

### Database

#### Schema
The project uses PostgreSQL as the database management system. The database runs in a Docker container for an easy setup
and will be automatically created and configured when the application is started. The database schema is defined in the 
[`backend/researchlens/migrations/0001_initial.py`](backend/researchlens/migrations/0001_initial.py) file, which
contains the commands to create the tables and their relationships. For simplicity, the schema is also described here:

```sql
--Create the extension for vector operations used for the embedding vectors
CREATE EXTENSION vector;
--Table for storing the authors
CREATE TABLE IF NOT EXISTS researchlens_author (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    institution VARCHAR(255)
);
--Table for storing the papers
CREATE TABLE IF NOT EXISTS researchlens_paper (
    id BIGSERIAL PRIMARY KEY,
    arxiv_id VARCHAR(100) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    published_date DATE NOT NULL,
    keywords JSONB NOT NULL DEFAULT '[]', --Using JSONB to store keywords as a list of strings
    embedding vector(384) NULL, --Using pgvector to store embeddings
    categories TEXT NOT NULL,
    link VARCHAR(255) NULL
);
--Table for storing the many-to-many relationship between papers and authors
CREATE TABLE IF NOT EXISTS researchlens_paper_authors (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES researchlens_paper(id) ON DELETE CASCADE,
    author_id BIGINT NOT NULL REFERENCES researchlens_author(id) ON DELETE CASCADE
);
--Table for storing the paper similarities
CREATE TABLE IF NOT EXISTS researchlens_papersimilarity (
    id BIGSERIAL PRIMARY KEY,
    similarity_score FLOAT NOT NULL,
    source_paper_id BIGINT NOT NULL REFERENCES researchlens_paper(id) ON DELETE CASCADE,
    target_paper_id BIGINT NOT NULL REFERENCES researchlens_paper(id) ON DELETE CASCADE
);
```

The data is stored in three tables. The table `paper` contains the papers with information such as the title, abstract, publication date, and categories. The authors are stored in a separate table `author`, which is linked to the `paper` table via a many-to-many relationship. The table `auhor_paper` is used to store the relationship between authors and papers. The table `papersimilarity` is used to store the similarity between papers based on their embeddings. However, it is not used in the application, because we compute the similarity on-the-fly when the user requests related papers. Nevertheless, this table may be be useful to speed up the retrieval of related papers in the future.

#### Insertions and Queries
We implemented several classes in [`backend/researchlens/object_relational_mapper.py`](backend/researchlens/object_relational_mapper.py)
to interact with the database. These classes map between Python objects and the rows in the tables and have operations to
insert, update, and filter rows from the database. We essentially implemented a custom Object Relational Mapper (ORM). The advantage of this approach is that we can use Python objects in our application to interact with the database and that we have abstracted from raw SQL queries. In a practical application, you would use a library like SQLAlchemy or Django ORM to achieve this. However, for the purpose of this course and project, we implemented our own ORM to understand how it works under the hood. We also provide a version that actually uses Django ORM (see django-orm branch).

### Search Functionality
The search functionality is also implemented in the [`backend/researchlens/object_relational_mapper.py`](backend/researchlens/object_relational_mapper.py). The method `get()` of the class `PaperMapper` takes as input optional search parameters such as text, publication date, and categories. It then dynamically constructs a SQL query based on the provided parameters and executes it to retrieve the matching papers from the database. The results are returned as a list of `Paper` objects. We use the following operations to build the query:

- `INNER JOIN`: To join the `paper` and `author` tables to get the authors of the papers.
- `WHERE`: To filter the results based on the search parameters.
- `TSVECTOR` and `TSQUERY`: To perform matching based on the text content of the papers
- `IN`: To filter based on categories
- `>=`and `<=`: To filter based on publication date

This is how an example query looks like for text search (ocean), publication date (between 2000-01-01 and 2026-01-01), and categories (Physics or Statistics):
```sql
SELECT p.id, p.arxiv_id, p.title, p.abstract, p.keywords, p.published_date, p.link, p.categories, a.id, a.name
FROM researchlens_paper p
INNER JOIN researchlens_paper_authors pa ON p.id = pa.paper_id
INNER JOIN researchlens_author a ON pa.author_id = a.id
WHERE to_tsvector('english', p.title || ' ' || p.abstract || ' ' || a.name) @@ plainto_tsquery('english', 'ocean') AND p.published_date >= '2000-01-01' AND p.published_date <= '2026-01-01' AND p.categories IN ('Physics', 'Statistics')
ORDER BY p.published_date DESC;
```

In the application, we first run the above query but only to get the IDs of matching papers. Then, we apply the pagination to the
list of matching IDs and run another query to select the papers and their authors based on the IDs. A direct quey with pagination was not possible because one paper could yield multiple rows in the result set due to multiple authors. Therefore, we first get the IDs of the matching papers, compute the pagination, and then run a second query to get the papers with details based on the IDs.

### Finding Related Papers
The functionality to get related papers is also implemented in the [`backend/researchlens/object_relational_mapper.py`](backend/researchlens/object_relational_mapper.py). The method `get()` of the class `RelatedPaperMapper` takes as input a paper ID and outputs a list of related papers. We use the following operations to build the query:

- `INNER JOIN`: To join the `paper` and `author` tables to get the authors of the papers.
- `ORDER BY p.embedding <-> '[-0.19108926,0.043524727,...]' ASC`: To sort based on the L2 distance in an ascending order.
- `LIMIT`: To limit the number of results to a specific number (e.g., 10).

This is how an example query looks like to retrieve related papers based on the L2 distance  embedding of a paper with a specific ID (e.g., `paper_id = 12345`):
```sql
SELECT p.id, p.arxiv_id, p.title, p.abstract, p.keywords, p.published_date, p.link, p.categories, a.id, a.name
FROM researchlens_paper p
INNER JOIN researchlens_paper_authors pa ON p.id = pa.paper_id
INNER JOIN researchlens_author a ON pa.author_id = a.id
ORDER BY p.embedding <-> '[-0.19108926,0.043524727,...]' ASC
LIMIT 10;
```

As previously, the query is first run to get the IDs and then a second query is run to get the papers and their authors based on the IDs. This is done to really get 10 related papers, even if a paper has multiple authors.


### XML
The API from arXiv provides the data in XML format. We use the `xml.etree.ElementTree` module from Python's standard library
to parse the XML data and extract the relevant information. The code for parsing the XML data is implemented in
[`backend/researchlens/tasks.py`](backend/researchlens/tasks.py).


### Embeddings and Keywords
We use `SentenceTransformers` to compute the embeddings to find related papers based on their content. We use `KeyBERT` to automatically extract keywords from the papers. The embeddings are stored in the database as vectors using the `pgvector` extension for PostgreSQL. The keywords are stored as a JSON list of strings in the database. The code for computing the embeddings and keywords is implemented in
[`backend/researchlens/tasks.py`](backend/researchlens/tasks.py).


### Extensions
We use several small extensions to enhance the functionality of the project:
- pgvector: A library to store and query vectors in PostgreSQL. We use it to store the embeddings (vectors of size 384) of the documents in the database.
- Cascade delete: We use `ON DELETE CASCADE` in the database schema to automatically delete related rows when a row is deleted. This is useful to keep the database clean and avoid unused rows. 
- datatype JSON: We use the JSON data type to store the keywords of the documents in the database. This is convenient to store
  the keywords as a list of strings and query them easily.
- Django ORM: In the django-orm branch, we use Django's Object Relational Mapper (ORM) to interact with the database. This allows us to define the database schema using Python classes and provides a convenient way to query the database using Python objects. This is useful for large projects where you want to avoid writing raw SQL queries and instead use Python objects to interact with the database. However, for the purpose of this course and project, we also provide a version that uses raw SQL queries to interact with the database (see main branch).
