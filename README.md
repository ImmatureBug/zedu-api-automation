[![CI - Zedu API Tests](https://github.com/ImmatureBug/zedu-api-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/ImmatureBug/zedu-api-automation/actions/workflows/ci.yml)


Zedu API Automation:

This my task tests the backend APIs of the Zedu platform automatically using  the Python and Pytest. So it basically work like this, instead of manually sending requests in Postman every time, this task runs all the tests with one command and tells you exactly what passed and what failed.

And i built this as part of a  my stage 3 task given to by hng and it is where I had to prove that i can automate API testing properly which include handling authentication, writing clean test code, and catching real bugs along the way.

So what are the requirement you need before starting this task, you will need a Python 3.11 or higher and git installed on your computer

To check,  whether is is installed or you want to check your version open your terminal and run:

```bash
python --version
git --version
```


How do you set up this task:

Step 1:Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/zedu-api-automation
cd zedu-api-automation
```



Step 2:Create a virtual environment

```bash
python -m venv venv
```

Then activate it:

On Windows (Git Bash):
```bash
source venv/Scripts/activate
```

On Mac/Linux:
```bash
source venv/bin/activate
```
so when you see (venv) appear at the start of your terminal. That means that it has worked.



Step 3: Install all dependencies

```bash
pip install -r requirements.txt
```



Step 4: Set up your environment variables

This is important. The project reads your credentials from a `.env` file.

Copy the example file:
```bash
cp .env.example .env
```

Then open `.env` and fill in your real details:
BASE_URL=https://api.zedu.chat/api/v1
EMAIL=your_email_here
PASSWORD=your_password_here

Make sure you use a real Zedu account. If you don't have one, go to https://zedu.chat and register.



Step 5:Running the tests

Run everything at once:
```bash
pytest tests/ -v
```

Run only the auth tests:
```bash
pytest tests/test_auth.py -v
```

Run only the user tests:
```bash
pytest tests/test_users.py -v
```

Run with an HTML report you can open in your browser:
```bash
pytest tests/ -v --html=report.html
```



What each file does:

tests/test_auth.py: This file covers everything related to authentication, and so 29 test cases are covered in total:
1. Login with a valid and invalid credentials.
2. Register with a valid details, duplicate emails, duplicate usernames, empty fields and short passwords.
3. Logout with and without a token.
4. Password reset with a valid and invalid emails.
5. Token validation including malformed and missing tokens.
6. SQL injection and special character attempts.

tests/test_users.py: This file covers user management endpoints and 9 test cases were covered:
1. Getting the current logged in user.
2. Getting all the users.
3. Getting a specific user by ID.
4. All of the above without a token or with a fake token.

utils/auth.py: This is where the login logic lives. Every test that needs a token calls this file instead of logging in manually. No tokens are hardcoded anywhere.

conftest.py: This file sets up shared fixtures that any test can use which include the base URL, auth headers and auth token.

.env: This file holds your credentials. It is cannot and can never be uploaded to GitHub. 
You must create it yourself by copying `.env.example`.

The CI/CD Pipeline: this uses GitHub Actions for continuous integration.

Every time code is pushed to the main branch, the pipeline automatically:
1. Installs all dependencies
2. Runs the full test suite
3. Generates a test report
4. Fails the build if any test fails

The workflow file is located at `.github/workflows/ci.yml`

Environment variables are stored as GitHub Secrets:
- `BASE_URL`: the API base URL
- `EMAIL`: test account email
- `PASSWORD`: test account password


Things I found during testing: While working on this task i discovered some real bugs in the Zedu API, these includes:
1. The login endpoint returns 400 instead of the documented 401 when credentials are wrong.
2. The registration endpoint allows duplicate accounts if you change just the phone number.
3. Short passwords like "ab" are accepted without any validation error.
4. The X-Platform header on logout is not actually enforced.

These are documented in the test names and comments inside the code.


The total test coverage, include;
For the file, we take a look at test_auth.py which we did 29 tests and they all passed.
we have test_user which i did 9 tests and they all passed. the total of everything is 38 tests and they all passed it


What Changed After Stage 3:

After getting feedback from Stage 3, I made some improvements to the project:

The first thing I fixed was replacing `uuid` with the `Faker` library for generating test data. Faker creates more realistic emails and usernames instead of random strings, and it solves the idempotency problem completely so that every test that run gets a new fresh unique data so tests never conflict with previous runs.

I also found one hardcoded email in my tests (`dara@gmail.com`) and replaced it with a dynamically generated one. No real emails should ever appear directly in test code.

Then I added a `utils/schemas.py` file that validates the full structure of API responses such as checking field presence, data types and required values and not just status codes.

Finally I added a GitHub Actions CI pipeline so that every time I push code to GitHub, all 38 tests run automatically without me having to do anything manually.