upstream daphne {
    server app:9000;
}

server {
    listen 8000;
    client_max_body_size 50M;

    location / {
        proxy_pass http://daphne;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

    location /ws/ {
        proxy_pass http://daphne;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        add_header Cross-Origin-Opener-Policy "same-origin";

        proxy_redirect off;
        proxy_set_header Host $host;
    }
    
    location /static {
        alias /vol/static;
    }
}