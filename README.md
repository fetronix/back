backend
for dadding locations python manage.py load_locations
fro running the tasks  python manage.py load_locations

# INFORMATION SYSTEMS ADMINISTRATION AND DEVELOPMENT

## OPEN SOURCE TECHNOLOGIES IN WEB DEVELOPMENT

### DEPLOYING DJANGO APP ON A LINUX/UBUNTU SERVER WITH APACHE

### MOVING YOUR APP FROM DEVELOPMENT TO PRODUCTION

Hello community! Today, I want to show you, at a beginner level, how to make your Django app live on production using an Ubuntu server/desktop. We will use server-side software, specifically Apache. In this tutorial, we will set up the server to run on HTTP ports 80 and 8000. Later, I will provide a tutorial on running over HTTPS port 443 with secure SSL.

## Requirements

- **Install Ubuntu**: Make sure you have Ubuntu installed on your server or desktop.
- **Ensure you have a Django app**: Your Django project should be ready for deployment.
- **Internet connection**: Required for installing necessary packages and libraries.

## Steps

### 1. Copy Your Django Project

To get started, you'll need to transfer your Django project folder from a Windows machine to your Ubuntu server using a USB drive.

- **Copy your Django project folder from Windows to a USB drive**: Ensure your Django project is saved on the USB drive.
- **Connect your USB drive to Ubuntu OS**: Plug the USB drive into your Ubuntu system.
- **Open your USB drive**: Navigate to the USB drive in your file manager.
- **Open Terminal**: Right-click inside the USB drive and select 'Terminal' to open a terminal session in the USB drive's directory.
- **Copy the Django project folder**: Run the following command to copy the Django folder and all its contents to the desired location on your Ubuntu server.

  ```python
  sudo cp -r backend /home/kenet/
  ```

  - **backend**: This is the name of your Django app folder.
  - **/home/kenet/**: This is the path where you are copying the folder to on your Ubuntu system.

### 2. Navigate to Your Django App

Once you've copied the project, navigate to the project directory on your Ubuntu server:

- **Navigate to your Django app directory**:

  ```python
  cd /home/kenet/backend/
  ```
- **List files to ensure they are present**:

  ```python
  ls -l
  ```

  Verify that you see these files: `app`, `db.sqlite3`, `manage.py`, `project`, `static`.

### 3. Create Virtual Environment

A virtual environment is essential for managing dependencies and isolating your Django project from other Python projects.

- **Update packages**:

  ```python
  sudo apt update
  ```
- **Install Python 3 and `venv`**:

  ```python
  sudo apt install python3-venv
  ```
- **Create a virtual environment**:

  ```python
  sudo python3 -m venv venv
  ```
- **Activate the virtual environment**:

  ```python
  source venv/bin/activate
  ```
- **Enable write permissions to install libraries in `venv`**:

  ```python
  sudo chmod -R 777 venv
  ```

### 4. Install Required Libraries

Ensure that all necessary Python libraries are installed within your virtual environment.

- **Install Django and other libraries**:

  ```python
  pip install django
  pip install pandas
  pip install plotly
  pip install scikit-learn
  pip install numpy
  pip install django-admin-menu
  pip install django-import-export
  ```

### 5. Run Your Site

Before configuring Apache, ensure your Django app runs correctly.

- **Run your Django application**:

  ```python
  python manage.py runserver
  ```

  Your app should now be accessible at `http://127.0.0.1:8000/` by default.

## Apache Web Server Configurations for HTTP Port 80

### 1. Install Tools to Check IP Address

You'll need to know your server's IP address for configuring Apache.

- **Install `net-tools`**:

  ```python
  sudo apt install net-tools
  ```
- **Check your IP address**:

  ```python
  ifconfig
  ```

  **OR**

  ```python
  ip addr show
  ```

  Note down the server IP address. In my case, it is `10.0.2.15/24`.

### 2. Update Django Settings

Configure your Django settings to ensure compatibility with Apache.

- **Install `gedit` for editing files**:

  ```python
  sudo apt install gedit
  ```
- **Open and edit Django settings**:

  ```python
  sudo gedit /home/kenet/backend/settings.py
  ```
- **Update settings**:

  ```python
  ALLOWED_HOSTS = ["*"]
  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
  ```

  - **ALLOWED_HOSTS**: Set to `["*"]` to allow all hosts (for development; specify allowed hosts in production).
  - **STATIC_URL**: URL prefix for static files.
  - **STATIC_ROOT**: Directory where static files will be collected.

  Remove this line from `settings.py`:

  ```python
  STATICFILES_DIRS = [BASE_DIR / 'static']
  ```
- **Make write permissions on 'static' directory**:

  ```python
  sudo chmod -R 777 static/
  ```

### 3. Create Apache Virtual Host Configuration

- Configure Apache to serve your Django app.

```python
sudo apt update
sudo apt install apache2 libapache2-mod-wsgi-py3 python3-pip
```

- **Create a new Apache configuration file**:

  ```python
  sudo nano /etc/apache2/sites-available/django_project.conf
  ```
- **Add the following configuration**:

  ```apache
  <VirtualHost *:80>
      ServerAdmin admin@kenet
      ServerName 197.136.16.164
      DocumentRoot /home/kenet/backend/project

      Alias /static /home/kenet/backend/static
      <Directory /home/kenet/backend/static>
          Require all granted
      </Directory>

      <Directory /home/kenet/backend/project>
          <Files wsgi.py>
              Require all granted
          </Files>
      </Directory>

      WSGIDaemonProcess backend python-path=/home/kenet/backend/project python-home=/home/kenet/backend/venv
      WSGIProcessGroup backend
      WSGIScriptAlias / /home/kenet/backend/project/wsgi.py

      ErrorLog ${APACHE_LOG_DIR}/error.log
      CustomLog ${APACHE_LOG_DIR}/access.log combined
  </VirtualHost>
  ```

  - **ServerAdmin**: Email address of the server administrator.
  - **ServerName**: Your server's IP address or domain name.
  - **DocumentRoot**: Directory where your Django project is located.
  - **Alias /static**: Maps the URL `/static` to the directory where static files are stored.
  - **Directory**: Permissions for static files and the WSGI script.
  - **WSGIDaemonProcess**: Configures the WSGI daemon process for your Django project.
  - **WSGIScriptAlias**: Path to the WSGI script for your Django project.

### 4. Enable New Site Configuration

Activate the new Apache site configuration and mod_wsgi module.

- **Enable the new site and mod_wsgi module**:

  ```python
  sudo a2ensite django_project.conf
  sudo a2enmod wsgi
  ```
- **Restart Apache**:

  ```python
  sudo systemctl restart apache2
  ```

### 5. Set Permissions

Ensure Apache has the necessary permissions to read and execute files.

- **Ensure Apache has read and execute permissions**:

  ```python
  sudo chown -R www-data:www-data /home/kenet/backend/project
  sudo chmod -R 755 /home/kenet/backend/
  sudo chown -R www-data:www-data /home/kenet/backend/static/
  sudo chmod -R 755 /home/kenet/backend/static/
  ```
- **Enable the site configuration and reload Apache**:

  ```python
  sudo a2ensite django_project.conf
  sudo a2dissite 000-default.conf
  sudo systemctl reload apache2
  ```
- **Ensure Apache has read permission on parent directories**:

  ```python
  sudo chmod 755 /home
  sudo chmod 755 /home/kenet
  sudo systemctl restart apache2
  ```
- **Run your project**: Open a web browser and navigate to `http://197.136.16.164` to see your Django app live.

## Apache Web Server Configurations for HTTP Port 8000

If you prefer to use port 8000 instead of the default port 80, follow these additional steps.

### 1. Update Ports Configuration

Configure Apache to listen on port 8000.

- **Open the ports configuration file**:

  ```python
  sudo gedit /etc/apache2/ports.conf
  ```
- **Change the port from 80 to 8000**:

  ```apache
  Listen 8000
  ```

### 2. Update Virtual Host Configuration

Modify your virtual host configuration to use port 8000.

- **Open the virtual host configuration file**:

  ```python
  sudo gedit /etc/apache2/sites-available/django_project.conf
  ```
- **Change the port from 80 to 8000**:

  ```apache
  <VirtualHost *:8000>
  ```
- **Restart Apache**:

  ```python
  sudo systemctl restart apache2
  ```
- **Run your site**: Open a web browser and navigate to `http://197.136.16.164:8000` to access your Django app on port 8000.

## Conclusion

In this tutorial, you learned how to deploy a Django application on an Ubuntu server using Apache. We covered the following:

1. **Copying Your Django Project**: Transferring your project from Windows to Ubuntu.
2. **Creating and Configuring a Virtual Environment**: Isolating your Python environment.
3. **Installing Required Libraries**: Ensuring all necessary libraries are available.
4. **Running Your Django App**: Testing the application before configuring Apache.
5. **Configuring Apache for HTTP Ports 80 and 8000**: Setting up Apache to serve your Django application.

This setup allows you to deploy and serve your Django application using Apache on your Ubuntu server. For a more secure deployment, consider setting up HTTPS with SSL certificates, which will be covered in a future tutorial.



sudo chown -R www-data:www-data /home/kenet/Pictures/backend
sudo chmod -R 755 /home/kenet/Pictures/backend
sudo chown -R www-data:www-data /home/kenet/Pictures/backend/static/
sudo chmod -R 755 /home/kenet/Pictures/backend/static/

sudo chmod 755 /home
sudo chmod 755 /home/kenet
sudo systemctl restart apache2
