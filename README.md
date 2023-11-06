### General description

- The project is a django web application, for creation and sending newsletters to the users' clients base.
- Main stack and tools: Django, Postgres, Celery, Celery-beat, Redis, Bootstrap, HTML.

### Project apps and models

- 'newsletter' app:
    - Newsletter - all the newsletters attributes and settings.
    - NewsletterAttempts - newsletters sending attempts (both one-off and periodic newsletters).
    - EmailServerResponse - (clients email servers responses for each newsletter).
    - Schedule - base regularity modes (daily, weekly, monthly).
- 'client' app:
    - Client - users' clients.
- 'blog' application:
    - Blog - blogs promoting the service.
- 'users' app:
    - User - users of the service.

### Custom user group

- common users:
    - have access to the CRUD mechanism for their own newsletters (created by a request user).
    - have access to the CRUD mechanism for their onw clients (added by a request user).
    - can send one-off newsletters (created by a request user) to their own client base.
    - can launch regular periodic newsletters (created by a request user) to their own client base.
- "manager" group members:
    - have access to all the common users functionality listed above.
    - can terminate and disable regular newsletters (custom permission remove_regular_newsletter).
    - can view and block (custom permission block_user) all the service users.
    - can view newsletters created by all users.

# Install and usage
1. Clone the project from ___ to your local machine.

2. Build a new image and run the project container from the root project directory:
   - docker-compose build
   - docker-compose up

3. Download the testing/example fixture using the command:
   - docker-compose exec app_newsletters_web_app python manage.py loaddata test_fixture.json \
     Available credentials:
     - superuser:
       {
         "email": "test_superuser@mail.com",
         "password": "123"
       }
     - manager:
       {
         "email": "test_manager@mail.com",
         "password": "QWE123qwe123!"
       }
     - common user:
       {
         "email": "test_member@outlook.com",
         "password": "QWE123qwe123!"
       }
   - alternatively you can register a new user over http://127.0.0.1:8000/users/registration/

4. Go to the main page on your browser http://127.0.0.1:8000/ and start working with the web application.
