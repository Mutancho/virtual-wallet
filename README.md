# Virtual Wallet

## Description
Virtual Wallet is a comprehensive financial management platform designed to facilitate user-to-user transactions, account management, and financial oversight in an intuitive and secure manner. At its core, the application operates on a two-tiered structure: a user interface for individual account holders and an administrative interface for system oversight and user management.

For individual users, Virtual Wallet offers a suite of features enabling seamless monetary transfers, account updates, transaction history viewing, and more. A user-friendly design combined with robust functionality provides a reliable tool for managing one's personal finances.

On the administrative side, Virtual Wallet offers features designed to maintain system integrity and user satisfaction. Admins have access to detailed user data, transactional information, and the ability to manage user access as required, ensuring a safe and efficient operating environment.

## Key Features

### User Side
- **Account Management**: Users can create an account, update their profiles, manage their credit/debit cards, and view their transaction histories.
- **Monetary Transfers**: Users can send and receive money to other users, as well as deposit money into their Virtual Wallet from a linked bank account.
- **Transaction Confirmation**: Each transfer must go through a confirmation step which allows users to confirm or edit their transaction details.
- **Search and Sort Features**: Users can view their transactions filtered by period, recipient, and direction (incoming or outgoing), and sort them by amount and date.

### Admin Side
- **User Management**: Admin users can view a list of all users, search them by phone number, username or email, and block or unblock them as necessary.
- **Transaction Oversight**: Admin users can view all user transactions filtered by period, sender, recipient, and direction (incoming or outgoing), and sort them by amount and date.
- **System Management**: Admin users have access to critical system settings and features designed to maintain the operational integrity of the platform.

## Technical Features
The Virtual Wallet project follows industry-standard best practices including KISS, SOLID, and DRY principles. The application employs a tiered project structure separating business logic, data, and presentation layers.

The project includes a relational database designed to prevent data duplication and empty data fields. The repository includes scripts to create and populate the database.

All project development is managed via GitLab, with a commit history that demonstrates the contribution of all team members.

## Technologies Used

This project utilizes a number of modern technologies and practices:

- **Backend**: FastAPI, a high-performance web framework for building APIs with Python.
- **Frontend**: React, a JavaScript library for building user interfaces.
- **Database**: MariaDB, a highly reliable and performant SQL database system.
- **Database Hosting**: Microsoft Azure, a cloud platform offering reliable and scalable cloud computing services.
- **Authentication**: JSON Web Tokens (JWT), a standard for securely transmitting information between parties as JSON objects.
- **Asynchronous Programming**: Used to handle multiple tasks concurrently for improved application performance.
- **Database Connection Pooling**: A method used to manage database connections for better resource utilization and application performance.
- **Payment Processing**: Stripe API, a powerful and flexible tool for internet commerce.
- **Chat Functionality**: ChatEngine, a service for building chat features.
- **Version Control**: GitLab, a web-based DevOps lifecycle tool that provides a Git-repository manager.
- **Deployment**: Details to be added as the project progresses. 

## Visuals
### Relational Database Schema
![Alt](/images/database_virtual_wallet.JPG)

## Installation
Follow these steps to get a local running version of the project for development and testing purposes.

### Prerequisites 
Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Node.js and npm (for the front end).
- You have installed the latest version of Python (FastAPI runs on Python).
- You have a recent version of MariaDB installed.
- You have Git installed to clone the project.
- You have an account with Azure, ChatEngine, and Stripe, and the ability to generate API keys for these services.

### Steps
1. **Clone the repository in the desired directory  - "git clone  https://gitlab.com/team-group-5/virtual_wallet.git"**
2. **Install backend dependencies "pip install requirements.txt"**
3. **Set up the database**

    - Navigate to the Azure portal.
    - Create a new SQL Database.
    - Retrieve your connection string.
    - Open MySQL Workbench.
    - Connect to the database using the connection string retrieved from Azure.
    - Create a new database for the project: `CREATE DATABASE your_database_name;`.
    - Import the provided SQL files (`e-wallet_database.sql` and `e-wallet_insert_currencies.sql`) to set up the tables and include the supported currencies.

4. **Setting up the .env file**

    Navigate to backend/config and create a file named `.env`. This file will environment variables that your application requires. 

    - `DATABASE_HOSTNAME`= The hostname where your database is hosted. If you are running your database locally, this will be `localhost`. If you are using Azure, this will be the hostname provided by Azure.
    - `DATABASE_PORT`= The port that your database is running on. For MariaDB/MySQL, the default port is typically `3306`.
    - `DATABASE_USERNAME`=The username that your application will use to authenticate with your database.
    - `DATABASE_PASSWORD`= The password that your application will use to authenticate with your database.
    - `DATABASE_NAME`= The name of the database your application will connect to. This should match the name you used when creating the database: `your_database_name`.
    - `SECRET_KEY`= A secret key for your application. This is used in the process of generating secure tokens.
    - `ALGORITHM`= The algorithm your application uses for generating secure tokens.
    - `ACCESS_TOKEN_EXPIRE_MINUTES`= The lifespan of the access token, in minutes.
    - `STRIPE_SECRET_KEY` and `STRIPE_PUBLIC_KEY`= Your secret and public keys for the Stripe API. You will get these from your Stripe account.
    - `BASE_URL`= The base URL of your application, for instance `http://127.0.0.1:8000`.
    - `CHAT_PROJECT_ID` and `CHAT_PRIVATE_KEY`= Your project ID and private key for the Chat Engine. You will get these from your Chat Engine account.

5. **In terminal, within the root directory of main.py use to run the backend server "uvicorn main:app --reload"**

6. **Navigate to frontend directory and install frontend dependencies "npm install"**
7. **Run the front end via terminal "npm start"**


## Usage

Follow the steps below to use the Virtual Wallet application:

1. Ensure that the backend server and database are up and running. Refer to the "Installation" section for instructions on setting up the backend and database.

2. Open your web browser and navigate to the frontend URL or the local development server URL where the React application is hosted.

3. Register a new account or log in if you already have an account.

4. Explore the user interface to perform various actions such as managing your profile, creating wallets, adding a credit/debit card, making transfers to other users, and viewing transaction history.

5. As an admin user, you will have additional privileges to manage users, view user transactions, and perform administrative tasks. You can access the admin panel by logging in with your admin credentials.

6. Additional features to test include, referral system, email verification, email notifications, joint virtual wallets, recurring transactions, and more.

Note: It is important to handle sensitive information, such as real credit card details, carefully during testing. Make sure to use test or dummy data for transactions and avoid using real financial information.

For detailed API documentation, please refer to the [Swagger documentation](<http://127.0.0.1:8000/docs>).

