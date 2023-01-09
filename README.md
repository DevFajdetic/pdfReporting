# pdfReporting

## Setup

git clone https://github.com/DevFajdetic/pdfReporting.git
cd pdfReporting
py -m pip install --upgrade pip
py -m pip install --user virtualenv
py -m venv env
.\env\Scripts\activate
pip install requirements.txt

NOTE: Some dependencies are supported only for py ver ~3.9 to set correct python version in virtual env run:
py -3.9 -m venv C:\path-to-this-directory\pdfReporting\env

## Creating UI

Open the editor by typing editor.py inside project directory

Inside editor open templating.ui

Inside app directory
Compile code from XML to python run -> pyuic5 -x templating.ui -o ui.py

DO NOT MODIFY THE PY FILE.

Copy the code in the main ui file instead
