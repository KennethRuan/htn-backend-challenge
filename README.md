# Hack the North Backend Challenge 2023

Submission for the 2023 HTN BE Challenge. 

The project implements the requested API features using Django and SQLite.

## Features

These are the features currently supported by the API:
-   All Users Endpoint
-   User Information Endpoint
-   Updating User Data Endpoint
-   Skills Frequency Endpoint
-   Query Parameter Filtering for Skills Frequency (Min/Max Freq)

## Installation

The backend setup utilizes Docker for dependencies. To begin, make sure that you have Docker installed on a Linux system.
If you are on Windows, you can follow this [installation guide](https://docs.docker.com/desktop/install/windows-install/) provided by Docker. 

To setup the project, start by cloning the repository and navigating into its directory
```sh
git clone https://github.com/KennethRuan/htn-backend-challenge
cd htn-backend-challenge
```

At this point, all of the project files will have been installed. To get the initial hacker data into the database, we can run the JSON parser script.
Note, if data has already been put into the `hackers` or `skills` tables in the database, they will be reset.
```sh
python3 ./scripts/parser.py
``` 

Afterwards, run
```sh
docker-compose up
```

From here, the Docker image and container will automatically be setup. 
After it is up and running, the API endpoint will be hosted at `localhost:8000`.

## Implementation Details

<details>
<summary><b>Database Structure</b></summary><br>

The information for participants is stored in two tables in an SQLite database.
The `hackers` table consists of all the general user data outside of skills. It's SQL schema is as follows
```sql
CREATE TABLE IF NOT EXISTS hackers (
    hacker_id INTEGER,
    name TEXT NOT NULL,
    company TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    PRIMARY KEY (hacker_id AUTOINCREMENT)
);
```

The `skills` table consists of skills data. Each skill has a name, rating and a Foreign Key that associates it with a user. 
It's SQL schema is as follows
```sql
CREATE TABLE IF NOT EXISTS skills (
    skill_id INTEGER,
    name TEXT NOT NULL,
    rating TEXT NOT NULL,
    hacker_id INTEGER,
    PRIMARY KEY (skill_id AUTOINCREMENT),
    FOREIGN KEY (hacker_id) REFERENCES hackers(hacker_id)
);
```

</details>

<details>
<summary><b>API Structure</b></summary><br>

This project is implemented using Django's ORM. The majority of the response handling code can be found under the `/backend/hackerapi` directory.

`views.py` - Implementation of all of the API views. This is how all of the API endpoints and their respective GET or PUT functionality are implemented for this project.

`serializers.py` - Helper classes that map Django models into simple datatypes. Used to generate JSON response when an API endpoint is hit. 

`urls.py` - Links each of the views to an API endpoint.

</details>

<details>
<summary><b>All Users Endpoint</b></summary><br>

This feature is implemented as outlined in the challenge. The endpoint returns a list of all user data from the database in a JSON format.

The endpoint also returns the `company` and `phone` fields, in addition to the fields shown in the GraphQL example.

</details>

<details>
<summary><b>User Information Endpoint</b></summary><br>

This feature is implemented as outlined in the challenge. This endpoint returns the user data for a specific user.

Each user is identified with a primary key.

</details>

<details>
<summary><b>Updating User Data Endpoint</b></summary><br>

This feature is implemented as outlined in the challenge. This endpoint allows you to update a given user's data by accepting data in a JSON format and returns the updated user data as the response.

This feature supports partial updating and the updating/creation of skills.

</details>

<details>
<summary><b>Skills Endpoint</b></summary><br>

This feature is implemented as outlined in the challenge. This endpoint shows a list of skills and frequency info about them.

This feature supports query parameter filtering. You may specify a `min_frequency`, `max_frequency` or both.

</details>