#!/bin/bash
#!/bin/bash

echo "Performing application setup..."

# Run migrations (if applicable)
echo "Running database migrations..."


python ao_website/manage.py makemigrations --noinput;
python ao_website/manage.py migrate --noinput;
python ao_website/manage.py collectstatic --noinput;
echo "Starting Django server..."
python ao_website/manage.py runserver 0.0.0.0:8000
