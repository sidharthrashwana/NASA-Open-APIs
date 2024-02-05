# NASA Space App Challenge

## Overview
This is a Flask web application developed for the NASA Space App Challenge. The application provides users with information related to astronomy, near-Earth objects, and Coronal Mass Ejections (CME) based on NASA's APIs.

## Features
1. **Home Page:**
    - Route: `/`
    - Displays the main page of the application.

2. **Navigate Page:**
    - Route: `/navigate`
    - Provides navigation links to different sections of the application.

3. **Astronomy Picture of the Day (APOD):**
    - Route: `/apod`
    - Allows users to input a date and retrieve the Astronomy Picture of the Day from NASA's API.
    - Displays the HD image, explanation, and title of the selected date.

4. **Near-Earth Object Web Service (NeoWS):**
    - Route: `/neows`
    - Allows users to input a start date and end date to retrieve information about Near-Earth Objects within that date range.
    - Displays details such as ID, NEO Reference ID, name, NASA JPL URL, absolute magnitude, estimated diameter, hazard status, and close approach data.

5. **Coronal Mass Ejection (CME):**
    - Route: `/donkiCME`
    - Allows users to input a start date and end date to retrieve information about Coronal Mass Ejections from NASA's API.
    - Displays details such as activity ID, catalog, start time, source location, active region number, links, notes, CME analyses, and linked events.

## Prerequisites
- Python 3.x
- Flask
- Flask-WTF
- Flask-SQLAlchemy

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    ```

2. Create virtual env
    ```bash
    python3.10 -m venv .venv
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Navigate to the project directory.
2. Run the Flask application:
    ```bash
    python app.py
    ```
3. Access the application in your web browser at `http://127.0.0.1:5000/`.

## Configuration
- Add your NASA API key to the designated placeholders in the `app.py` file.

## Credits
This project is developed for the NASA Space App Challenge by Sidharth Rashwana.
