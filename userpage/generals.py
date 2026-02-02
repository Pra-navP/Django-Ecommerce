from .models import *

def setting(request):
    data = {
        'ecom' : Setting.objects.last()

    }
    return data