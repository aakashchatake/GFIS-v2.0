# Unified GFIS Deployment

## Target

Deploy this folder as the public root of:

```text
gfis.chatakeinnoworks.com
```

## Routing

```text
/          Unified GFIS front page
/level-1/  Existing GFIS website
/level-2/  New Level 2 research workbench
```

## Security

Level 2 contains research, diary, notes, and document references. Before publishing real private documents, enable one of:

- Nginx basic auth for `/level-2/`
- Cloudflare Access for `/level-2/`
- FastAPI login and role-based access

## Nginx Sketch

```nginx
server {
    server_name gfis.chatakeinnoworks.com;
    root /var/www/gfis-unified;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /level-2/ {
        auth_basic "GFIS Level 2";
        auth_basic_user_file /etc/nginx/.gfis-level2.htpasswd;
        try_files $uri $uri/ /level-2/index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8010/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

