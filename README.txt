## Para hacer el deployment de la aplicación a Heroku seguir los siguientes pasos:
1. Crear una cuenta en Heroku.
2. Instalar Git y Heroku CLI.
3. Descargar el repositorio (https://github.com/felipegabela/jupiter.git).
4. Crear un repositorio vacío nuevo en git y añadir a ese repositorio remoto los archivos que acabaron de descargar.
5. En el archivo jupiter-master/production_scheduler/forms.py des-comentar las lineas 7-15 y   comentar la linea 16. Guardar el archivo.
5. En el archivo jupiter-master/jupiter/settings.py comentar lo que esta después del igual en la linea 13 y pegar lo siguiente ‘710dadac8199a005c65701c18daec149998b60af37e22e8e'
6. En el mismo archivo reemplazar la linea 16 por:  DEBUG = False
7. Guardar el archivo y hacer push a git.
8. Hacer login en heroku a través de la terminal o linea de comandos dentro de la carpeta principal del repositorio  ($ heroku login).
9. Crear una nueva aplicación en heroku ($ heroku create [nombre que le quieran dar]).
10. Vincular el repositorio de git a la aplicación ($ git push heroku master).
11. Instalar PostgreSQL en Heroku en caso de que no este instalado todavía.
12. Crear las migraciones a la base de datos de heroku ($ heroku run python manage.py makemigrations)
13. Ejecutar las migraciones ($ heroku run python manage.py migrate)
14. Crear superuser  ($ heroku run python manage.py createsuperuser)
15. Crear las siguientes variables de ambiente en heroku
      SECRET_KEY="710dadac8199a005c65701c18daec149998b60af37e22e8e"
      SHOPIFY_API_DEV_PASS="c2bf6e5be194d46e2d8b7b6b3b137a4f"
      SHOPIFY_API_DEV_USER=“6e4440f817fb00deef93767c52f24830”
		    *Las credenciales del API de Shopify son de un tienda simulación, puede que 			en el futuro ya no exista esa tienda.
16. En el archivo jupiter-master/production_scheduler/forms.py des-comentar las linea 16 y comentar las lineas 7-15. Guardar el archivo y hacer push a git.
17. En el archivo jupiter-master/jupiter/settings.py en la linea 13 borrar lo que esta después del igual pero mantener lo que esta después del comentario y descomentarlo.
18. Hacer push a heroku ($ git push heroku master).
19. Instalar Sendgrid addon a Heroku y crear una nueva llave.
20. Guardar la llave en las variables de ambiente de Heroku.
21. Abrir aplicación en el navegador y guardar el url. ($ heroku open).

Nota: Tomar en cuenta que el proceso de instalación en heroku puede cambiar.

## Para instalar localmente la aplicación seguir los siguientes pasos:
1. Descargar el código fuente del repositorio (https://github.com/felipegabela/jupiter.git).
2. Instalar las librerías del archivo “requirements.txt”
3. En el archivo jupiter-master/production_scheduler/forms.py des-comentar las lineas 7-15 y   comentar la linea 16. Guardar el archivo.
4. En el archivo jupiter-master/jupiter/settings.py en la linea 18 borrar lo que esta adentro de los corchetes.
5. En el mismo archivo reemplazar la linea 16 por:  DEBUG = False
6. Abrir una terminal o linea de comando en la carpeta raíz y ejecutar las migraciones de Django. ($ python manage.py migrate)
7. Crear superuser ($ python manage.py create superuser)
8. En el archivo jupiter-master/production_scheduler/forms.py des-comentar la linea 16 y comentar las lineas 7-15. Guardar el archivo.
9. Crear las siguientes variables de ambiente:
      SECRET_KEY="710dadac8199a005c65701c18daec149998b60af37e22e8e"
      SHOPIFY_API_DEV_PASS="c2bf6e5be194d46e2d8b7b6b3b137a4f"
      SHOPIFY_API_DEV_USER=“6e4440f817fb00deef93767c52f24830”
		  *Las credenciales del API de Shopify son de un tienda simulación, puede que 			en el futuro ya no exista esa tienda.
10. Crear una cuenta en Sendgrid y crear una nueva llave para acceso al API.
11. Guardar la llave en las variables de ambiente.
12. Correr el servidor ($ python manage.py runserver)
13. Abrir un navegador e ir a la siguiente dirección http://127.0.0.1:8000
