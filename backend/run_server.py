#!/usr/bin/env python
"""
Run Django development server on port 5000
"""
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    
    from django.core.management import execute_from_command_line
    
    # Override default port to 5000
    sys.argv = ['manage.py', 'runserver', '0.0.0.0:5000']
    execute_from_command_line(sys.argv)

