"""
This migration script handles the data models of the application and sets up the initial database schema for the
researchlens app. It includes the creation of necessary tables and the vector extension for handling embeddings.
It also establishes relationships between papers and authors, and between papers themselves for similarity scoring.
"""

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    # Operations to create the initial database schema for the researchlens app
    operations = [
        migrations.RunSQL(
            """
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
                keywords JSONB NOT NULL DEFAULT '[]',
                embedding vector(384) NULL,
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
            """,
        ),
    ]
