# Fake configuration file - Development environment
import os
from dotenv import load_dotenv

# This is a fake config file for development
load_dotenv('.env')

DEBUG = True
DATABASE_URL = 'sqlite:///dev.db'
SECRET_KEY = 'fake-dev-key-123'

# Development settings
DEV_MODE = True
LOG_LEVEL = 'DEBUG'
