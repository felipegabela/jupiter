## Quick Start

To get this project up and running locally on your computer:
1. Set up a python virtual environment
2. Assuming you have Python setup, run the following commands:

   pip3 install -r requirements.txt
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py collectstatic
   python3 manage.py test # Run the standard tests. These should all pass.
   python3 manage.py createsuperuser # Create a superuser
   python3 manage.py runserver
   ```
3. Open a browser to `http://127.0.0.1:8000/admin/` to open the admin site
4. Open tab to `http://127.0.0.1:8000` to see the main site, with your new objects.