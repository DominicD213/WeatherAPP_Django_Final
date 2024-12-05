# WeatherAPP_Django_Final

A simple Django application that provides weather data using the OpenWeatherMap API.

---

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Clone the Project
```bash
git init
git clone https://github.com/DominicD213/WeatherAPP_Django_Final.git
cd weather-app-django

Set Up a Virtual Environment

cd into the weather_app_django folder

python3 -m venv .venv
source .venv/bin/activate

Install Required Packages

bash
Copy code
pip install django
pip install python-dotenv
pip install requests

Run the Django Server
bash
Copy code
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
