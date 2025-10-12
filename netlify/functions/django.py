import os
from django.core.wsgi import get_wsgi_application
from serverless_wsgi import handle_request

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "budget_backend.settings")  # <-- change
application = get_wsgi_application()

def handler(event, context):
    return handle_request(application, event, context)
