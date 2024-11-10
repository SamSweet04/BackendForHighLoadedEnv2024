# Load Balancing Configuration

## Overview

We are using **Nginx** as the load balancer to distribute traffic across multiple instances of the Django application. This helps to handle more traffic and improves application availability.

## Configuration

The `nginx.conf` file is set up to balance the load between Django instances running on ports 8001 and 8002.

### Configuration Details

- **upstream django_servers**: Defines a list of application servers. Currently, it includes servers on `127.0.0.1:8001` and `127.0.0.1:8002`.
- **proxy_pass**: Forwards incoming requests to the upstream servers.
- **Headers**: Sets headers to pass client information to the application.

This setup allows Nginx to distribute requests evenly across multiple instances, reducing the load on any single server.

python manage.py runserver 127.0.0.1:8001


docker run --name nginx_load_balancer -p 80:80 -d nginx


python manage.py runserver 127.0.0.1:8002


    http {
        
        upstream django_servers {
            server 127.0.0.1:8001;
            server 127.0.0.1:8002;
            
        }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://django_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    }