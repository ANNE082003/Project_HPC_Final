# PROJECT-HPC
TIFR INTERNSHIP
## Languages/Components Used

- Frontend: Python
- Backend: Python
- Database: MySQL

## Installation

```
git clone
```

Note: Configure your application in the `config.py` and database and make sure the database and URI are set up correctly

## Initial Setup:

```
-Create and Activate Virtual environment
-pip install virtualenv
-virtualenv env
-.\env\Scripts\activate.ps1
```
## Install dependencies
```
 pip install Flask torch torchvision nltk
```
## Install nltk package
```
-(venv) python
>>> import nltk
>>> nltk.download('punkt')
```
Modify `intents.json` with different intents and responses for Chatbot if needed for future use

## Run
```
python train.py
```
This will dump data.pth file. And then run
the following command to test it in the console.
```
python chat.py
```


```
pip install -r requirements.txt
```

```
python run.py
```


## Functions

- Register and Login
- Different Portal for Admin and User
- Admin- Manage users,publications and faqs
-User-landing page,upload publications and view faqs
-Support Chatbot

## Technical Domain

- Create using Python
- Flask for the Web
- SQLAlchemy for Database
- Bootstrap for the UI
- Other Library like Flask-login, Flask-bcrypt
-NLP,Neural Network
