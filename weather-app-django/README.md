<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WeatherAPP Django Setup</title>
</head>
<body>
    <h1>WeatherAPP_Django_Final Setup</h1>

    <h2>Clone the Project</h2>
    <pre>
        <code>
git init
git clone https://github.com/DominicD213/WeatherAPP_Django_Final.git
cd weather-app-django
        </code>
    </pre>

    <h2>Set Up a Virtual Environment</h2>
    <pre>
        <code>
python3 -m venv .venv
source .venv/bin/activate
        </code>
    </pre>

    <h2>Install Required Packages</h2>
    <pre>
        <code>
pip install django
pip install python-dotenv
pip install requests
        </code>
    </pre>

    <h2>Run the Django Server</h2>
    <pre>
        <code>
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
        </code>
    </pre>

    <h2>Deactivate the Virtual Environment</h2>
    <pre>
        <code>
deactivate
        </code>
    </pre>
</body>
</html>
