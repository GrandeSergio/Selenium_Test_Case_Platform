# Selenium Test Case Platform

This Django web application allows users to upload and run Python Selenium test cases. Users can manage their test cases, execute them, and view the execution results.

## Features

- User authentication: Register, login, and manage user accounts.
- Test Case Management: Upload Python Selenium test cases.
- Test Execution: Run uploaded test cases and view the execution results.
- Scheduler: Create schedules to run multiple test cases automatically.

## Prerequisites

- Python 3.x
- Django
- Selenium
- Chrome WebDriver (or other appropriate web driver)

## Setup

1. Clone the repository:


    git clone https://github.com/GrandeSergio/selenium-test-platform.git
    
    cd django-selenium-test-platform


2. Install dependencies:


    pip install -r requirements.txt


3. Configure the database in `settings.py`.


4. Apply migrations:


    python manage.py migrate

5. Create a superuser account:


    python manage.py createsuperuser

6. Run the development server:


    python manage.py runserver


7. Access to the website at `http://localhost:8000/`


## Usage

- Visit the test case management page to upload and manage your test cases.
- Use the scheduler feature to automate test case execution.
- Use history view to search test case executions.