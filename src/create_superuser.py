import os
import sys
import django

# Setup Django
sys.path.append('/Users/vadimaskarov/PycharmProjects/calc-teacher-hours/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.user.models import CustomUser

# Create superuser
user = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='password123',
    first_name='Admin',
    last_name='User'
)
print(f'Superuser {user.username} created successfully!')