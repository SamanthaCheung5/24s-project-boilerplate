# Investment Portfolio Management System

This repository is home to the Investment Portfolio Management System, designed to enable efficient tracking and management of financial assets through a Dockerized environment. This system leverages a MySQL database for storing financial data, a Flask application for backend services, and a local AppSmith server for dashboarding and internal tools.

## Project Overview

Our Investment Portfolio Management System aims to offer an intuitive platform for users to monitor their investment portfolios. The system supports functionalities such as account management, transaction processing, and real-time investment performance analytics. Tailored to meet the needs of individual investors and portfolio managers alike, our solution is committed to enhancing investment decision-making processes.

### System Components

- **MySQL Database**: Secures and manages financial data, including user profiles, investment records, and transaction logs.
- **Flask REST API**: Facilitates data operations through HTTP requests, serving as the backbone for our frontend and AppSmith server interactions.
- **AppSmith Server**: Provides a visual interface for rapidly creating and deploying internal tools and dashboards.

## Getting Started

To get this system up and running on your local environment, follow these setup instructions!

### Prerequisites

- Docker Desktop must be installed on your machine to facilitate the building and running of the containers.

### Setup Instructions

1. **Repository Cloning**:
   Start by cloning this repository to your local machine:

   git clone https://github.com/SamanthaCheung5/Investment_Portfolio_Project.git 

2. **Directory Navigation**:
    Change your directory to the project's root:

    cd your-repository

3. **MySQL Secret Configuration**:
    Inside the secrets/ directory, create two text files for the MySQL passwords:

        db_password.txt
        db_root_password.txt

4. **Container Initialization**:
    Launch the Docker containers in detached mode:

    docker compose up -d


## Detailed Architecture

### Database Design
The MySQL database is foundational to our system, comprising several crucial tables:

- **managers**: Contains manager profiles with fields for ID, email, creation details, phone number, and name.
- **users**: Holds user information including links to managers through foreign keys.
- **marketdata**: Stores current and historical pricing information for various assets.
- **historicaldata**: Logs changes in asset prices over time.
- **accounts**: Details financial summaries for users.
- **investments**: Records individual investments of users.
- **portfolios**: Aggregates investments into portfolios assigned to users.
- **performance_indicators**: Keeps track of performance metrics for portfolios.
- **reports**: Generates and stores reports on portfolio performance.
- **retirement_account**: Manages retirement-related financial information.
- **retirement_transaction**: Logs transactions related to retirement accounts.
- **income**: Details income records possibly related to investments.
- **investment_transaction**: Connects transactions to investments and income.
- **instruments**: Catalogs financial instruments used in trades.
- **trades**: Logs trade activities involving financial instruments and accounts.

### Flask App
The Flask application provides:

- **REST API Endpoints**: For managing database resources including users, portfolios, trades, and viewing reports.
- **Security Features**: Implements authentication and authorization to protect data integrity and privacy.

### Docker Configuration
Our Docker environment consists of three main services defined in the docker-compose.yml file: the **Web Service** serves the Flask application, mapping the `./flask-app` directory to `/code` in the container and using `./secrets` for secret files, restarting unless manually stopped. The **Database Service** runs MySQL, mounts `./db` for initialization scripts, uses environment variables and Docker secrets for secure password management, and is configured to restart automatically. The **AppSmith Service** provides tools and dashboards, mapping ports 8080 and 4443 to the container's 80 and 443 respectively, and binds `./stacks` for persistent storage, also with an `unless-stopped` restart policy.

## Project Leads
1. Amy Kupa
2. Megan Jirakulaporn
3. Samantha Cheung
4. Alex Choi

## VIDEO DEMO
[Check out our video demo!](https://drive.google.com/file/d/1vMaKv8nz6zRZ0nFarntGyMGCm0hPSsH_/view?usp=sharing)

