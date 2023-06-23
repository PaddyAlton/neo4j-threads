# neo4j-threads

A project to see whether a graph database such as Neo4J can be used to power a forum-like feature with branching replies.

## Background

This project was inspired by some product conversations I had regarding a 'forum' feature. There are two popular product models in vogue:

1. the 'traditional' forum, with threads containing a set of linear, time-ordered replies
2. the 'branching' forum, with threads containing replies that can have replies, up to an (in principle) unlimited level of nesting

Model (1) is perfectly good for most products (including the one my colleagues ended up building), but plenty of social media sites (e.g. Reddit, Twitter) have apparently-arbitrary nesting of replies/forking of conversations - model (2). I thought it would be interesting to follow this route.

As a 'data' person, my first thought was 'what datastore should I use for this?' To me, the branching conversations make me think immediately of graph databases. One very well-known graph database is [Neo4J](https://neo4j.com/), so that's what I decided to use.

Along the way I got acquainted with [neomodel](https://neomodel.readthedocs.io/en/latest/index.html), an Object Graph Mapper.

### Important note

I've added an MIT license to the project, so feel free to make use of it under those terms. But please note that this was a learning project; I threw in some boilerplate infrastructure stuff, but haven't created a test suite ... and (since I don't plan to deploy this anywhere) I haven't added authentication to any of the routes. If it were deployed as-is, anyone would be able to call any of the routes!

## Setting up

### Preparing the database (first time)

Let's start by preparing the python environment and the graph database:

1. `pipenv run setup`
2. `docker compose up graphdb`

This second command _just_ brings up the Neo4J container. Data are persisted in volumes across restarts (unless you do `docker compose down --volumes`).

The first time you start the database, the user `neo4j` will be set up with a password defined via an environment variable `$NEO4J_AUTH=neo4j/<your password>`. However, a new password _should_ be subsequently set and stored in the `.env` file as the environment variable `$DBPASS`.

This is best done by logging into the Neo4J browser at `http://localhost:7474/browser/` and running `ALTER CURRENT USER SET PASSWORD FROM '<your password>' TO '<your new password>'`.

Next (i.e. _before_ you add any data) you want to apply any database constraints defined in the `src/models.py` file. For convenience, a script has been defined in the `Pipfile`. `pipenv run constraints` will apply the constraints defined in the file.

### Starting the API

To bring up the database and API, use `docker compose up`. At the moment the API is configured to be available at `http://localhost:8765/`.
