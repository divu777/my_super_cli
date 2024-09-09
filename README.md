# Weather CLI Application

This is a command-line interface (CLI) application for fetching and storing weather data. It allows users to sign up, log in, fetch weather information for a specific location, and view their search history.
Prerequisites

- Docker and Docker Compose
- Python 3.7 or higher
- pip (Python package installer)

## Setup

### Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Create a virtual environment and activate it(optional):

```bash
python -m venv venv
source venv/bin/activate
# On Windows,
use `venv\Scripts\activate`
# Or just google how to start and activate virtual env
```

### Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Set up the database using Docker:

```bash
docker compose up -d
```

### Install the CLI application:

```bash
pip install -e .
```

## Usage

After setting up, you can use the following commands:

1. Sign up a new user:

```bash
super user signup
```

2. Log in:

```bash
Copysuper user login
```

3. Fetch weather for a location:

```bash
super weather -l <location>
```

4. View your search history:

```bash
super history
```

5. Log out:

```bash
super user logout
```

## Troubleshooting

If you encounter any issues with the database initialization, ensure that the init.sql file is in the same directory as the docker-compose.yml file and has the correct permissions. Or Just message me directly would love to help you set it up.
