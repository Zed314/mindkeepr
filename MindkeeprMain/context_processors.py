from django.conf import settings # import the settings file
import os
# Kept in case we wantto pass paremeters directely to template
#def logout_oath_url(request):
#    return {'LOGOUT_OATH_URL': settings.LOGOUT_OATH_URL}

def is_sso_enabled(request):
    return {"USE_SSO": os.environ.get("USE_SSO","false") == "true"}
