# GizmoInventory
Mock inventory website.

## Prerequisites
Python 3, preferably 3.11 or higher.
Pip (if not already installed with Python).

## Execution Notes
Depending on whether your Python install has set up aliased names or not, you may need to invoke the executables by explicit versioned names. In other words, 'python3' instead of 'python', 'pip3' instead of 'pip'.

## Installation

Download project from GitHub

In a command shell, go to the project directory:

cd &lt;root of GizmoInventory&gt;

If using virtualenvs, create and activate one (and install requirements to core Python), otherwise skip this step:

python -m venv .

(on Windows):
Scripts\activate.bat

(on Linux):
source ./bin/activate

Install required Python modules:

pip install -r requirements.txt

## Run
In a command shell, go to the project directory:

cd &lt;root of GizmoInventory&gt;

If using virtualenvs, activate it, otherwise skip this step:

(on Windows):
Scripts\activate.bat

(on Linux):
source ./bin/activate

Start the web server:
python inventory_app.py

In browser, go to http://127.0.0.1:8080/inventory

## Containerization

Simple Dockerfile with Linux base included, modify as needed. 

By default, application runs on port 8080, expose externally as desired.

