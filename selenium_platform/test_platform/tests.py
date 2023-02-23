from django.test import TestCase
import os
from pathlib import Path

# Create your tests here.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'test_platform\\static\\')]
print(STATIC_ROOT)