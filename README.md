# Django Airport Management System

A comprehensive airport management system built using Django and MySQL, providing efficient and streamlined operations for airports.

### Prerequisites

Ensure you have the following installed on your local machine:

- Python 3.8+
- Django 3.1+
- MySQL 8.0+

### Steps

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/django-airport-management.git
    ```

2. Navigate to the project directory:

    ```bash
    cd django-airport-management
    ```

3. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Setup your MySQL database and edit the DATABASE settings in `settings.py`:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database',
            'USER': 'your_mysql_username',
            'PASSWORD': 'your_mysql_password',
            'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }
    ```

5. Apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Run the server:

    ```bash
    python manage.py runserver
    ```

## Usage

The airport management system provides features to manage flights, passengers, staff, and other airport operations.

