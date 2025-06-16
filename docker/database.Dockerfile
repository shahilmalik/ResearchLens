FROM postgres:15

RUN apt-get update \
 && apt-get install -y postgresql-server-dev-15 build-essential git \
 && git clone --depth 1 https://github.com/pgvector/pgvector.git /pgvector \
 && cd /pgvector && make && make install \
 && rm -rf /pgvector \
 && apt-get remove -y postgresql-server-dev-15 build-essential git \
 && apt-get autoremove -y && apt-get clean
