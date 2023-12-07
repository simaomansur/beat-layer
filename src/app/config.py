# -----------------------------------------------------------
# Project: BeatBank
# File: config.py
# Description: This file contains the configuration settings
# for the Flask app. It is imported by the __init__.py file
# in the same directory.
#
# Author: Parker Tonra
# -----------------------------------------------------------

import os

# Flask app configuration
from src.app import app
class Config:
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'beatbank.donotreply@gmail.com'
    app.config['MAIL_PASSWORD'] = 'hweaclfuatojowlh'
    app.config['SECURITY_PASSWORD_SALT'] = 'your_generated_salt_here'