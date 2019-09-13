#!/usr/bin/env python
import os
import sys
#注意启动的时候是 python manager 0:8090 如果不加0的话就没法外网访问.
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nlp_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
