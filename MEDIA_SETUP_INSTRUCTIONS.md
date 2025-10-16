# Media Folder Setup Instructions

## Directory Structure

Your project should have the following structure:

```
Shopify_StoryBook/
├── app.py
├── media/
│   ├── store_one/
│   │   ├── page_1_image_1.jpeg
│   │   ├── page_2_image_1.jpeg
│   │   ├── page_3_image_1.jpeg
│   │   └── ...
│   └── store_two/
│       ├── page_1_image_1.jpeg
│       ├── page_2_image_1.jpeg
│       ├── page_3_image_1.jpeg
│       └── ...
├── stroy_one.py
├── stroy_two.py
└── requirements.txt
```

## Setup Steps

### For Local Development (Windows):

1. Create the media folder:
```cmd
mkdir media
```

2. Move the image folders into media:
```cmd
move store_one media\
move store_two media\
```

### For Server (Linux):

1. Navigate to your project directory:
```bash
cd /home/bestworks-shopifystorybookai/htdocs/shopifystorybookai.bestworks.cloud
```

2. Create the media folder:
```bash
mkdir media
```

3. Move the image folders into media:
```bash
mv store_one media/
mv store_two media/
```

4. Set proper permissions:
```bash
chmod -R 755 media/
```

5. Stop the current uvicorn process:
```bash
# Find the process ID
ps aux | grep uvicorn

# Kill it (replace XXXX with actual PID)
kill XXXX
```

6. Restart uvicorn in background:
```bash
nohup uvicorn app:app --host 0.0.0.0 --port 8000 --workers 3 > app.log 2>&1 &
```

## Nginx Configuration (Optional - for better performance)

Update your nginx configuration to serve static files directly:

```nginx
server {
    listen 80;
    server_name shopifystorybookai.bestworks.cloud;

    # Serve media files directly through nginx
    location /media/ {
        alias /home/bestworks-shopifystorybookai/htdocs/shopifystorybookai.bestworks.cloud/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy API requests to FastAPI
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then reload nginx:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

## New API Response Format

After this change, your API will return image URLs like:
```
https://shopifystorybookai.bestworks.cloud/media/store_one/page_1_image_1.jpeg
https://shopifystorybookai.bestworks.cloud/media/store_two/page_1_image_1.jpeg
```

Instead of:
```
https://shopifystorybookai.bestworks.cloud/static/store_one/page_1_image_1.jpeg
https://shopifystorybookai.bestworks.cloud/static/store_two/page_1_image_1.jpeg
```

## Verify Setup

1. Check if files exist:
```bash
ls -la media/store_one/
ls -la media/store_two/
```

2. Test API endpoint:
```bash
curl http://localhost:8000/
```

3. Test image access:
```bash
curl -I http://localhost:8000/media/store_one/page_1_image_1.jpeg
```

4. Test full API:
```bash
curl -X POST http://localhost:8000/generate-story \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "story_id": 1}'
```

