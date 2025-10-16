# Shopify StoryBook

A FastAPI-based story generation API that creates personalized, illustrated children's stories. Users can generate custom stories by providing a name, which is dynamically inserted into pre-written story templates.

## Overview

This application serves as a story generator that personalizes narrative content for children. It includes multiple story templates with corresponding illustrations served as static content.

## Features

- **Personalized Story Generation**: Insert custom names into story narratives
- **Multiple Story Templates**: Currently includes two story variations
- **Image Management**: Serves multiple images per page with dynamic path resolution
- **RESTful API**: FastAPI-based endpoints for story generation
- **CORS Support**: Configured for cross-origin requests
- **Static File Serving**: Efficient serving of story illustrations

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **Python-multipart**: For handling multipart form data
- **PyMuPDF (fitz)**: PDF processing capabilities
- **Pillow**: Image processing library
- **Pytesseract**: OCR functionality

## Project Structure

```
Shopify_StoryBook/
├── app.py                 # Main FastAPI application
├── stroy_one.py          # Story template #1
├── stroy_two.py          # Story template #2
├── store_one/            # Images for story #1
│   ├── page_1_image_1.jpeg
│   ├── page_2_image_1.jpeg
│   └── ...
├── store_two/            # Images for story #2
│   └── ...
├── requirements.txt      # Python dependencies
├── Sample_Story.pdf      # Sample story document
└── env/                  # Virtual environment (not tracked)
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Shopify_StoryBook
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     env\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Tesseract OCR Setup** (if using OCR features)
   - Download and install Tesseract OCR from: https://github.com/tesseract-ocr/tesseract
   - Add Tesseract to your system PATH

## Usage

### Starting the Server

Run the application using:

```bash
python app.py
```

The server will start on `http://localhost:8000` with auto-reload enabled.

### API Endpoints

#### 1. Root Endpoint
**GET** `/`

Returns API information and usage instructions.

**Response:**
```json
{
  "message": "Story Generator API",
  "usage": "POST /generate-story with {name: 'your_name', story_id: 1 or 2}",
  "available_stories": [1, 2]
}
```

#### 2. Generate Story
**POST** `/generate-story`

Generates a personalized story based on the provided name and story ID.

**Request Body:**
```json
{
  "name": "Alex",
  "story_id": 1
}
```

**Parameters:**
- `name` (string): The character name to insert into the story
- `story_id` (integer): Story template identifier (1 or 2)

**Response:**
```json
{
  "story_id": 1,
  "name": "Alex",
  "pages": [
    {
      "page_number": 1,
      "content": "In a rainforest that glowed with magic, lived a little boy named Alex...",
      "image_path": [
        "http://localhost:8000/static/store_one/page_1_image_1.jpeg"
      ]
    },
    ...
  ]
}
```

### Example Request

Using `curl`:
```bash
curl -X POST "http://localhost:8000/generate-story" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alex", "story_id": 1}'
```

Using Python `requests`:
```python
import requests

response = requests.post(
    "http://localhost:8000/generate-story",
    json={"name": "Alex", "story_id": 1}
)
print(response.json())
```

## Story Content

### Story #1 & #2: "The Courage Bridge"

An 11-page story about a boy who builds a bridge in a magical rainforest to help his animal friends reach berries across a river. The story teaches themes of:
- Courage and perseverance
- Teamwork and friendship
- Starting small to achieve big dreams

## Static Files

Images are served through static file mounts:
- Story #1 images: `/static/store_one/`
- Story #2 images: `/static/store_two/`

The application automatically detects and serves multiple images per page with support for `.jpeg`, `.jpg`, and `.png` formats.

## Development

### Running in Development Mode

The application includes auto-reload functionality enabled by default:

```bash
python app.py
```

### API Documentation

FastAPI provides automatic interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuration

### CORS Settings

Currently configured to allow all origins (`allow_origins=["*"]`). For production deployment, update this in `app.py:20` to specify allowed domains:

```python
allow_origins=["https://yourdomain.com"],
```

### Server Configuration

Default server settings in `app.py:121-127`:
- **Host**: `0.0.0.0` (accessible from all network interfaces)
- **Port**: `8000`
- **Reload**: `True` (auto-reload on code changes)

## Dependencies

```
fastapi==0.104.1        # Web framework
uvicorn==0.24.0         # ASGI server
python-multipart==0.0.6 # Form data handling
PyMuPDF==1.23.8         # PDF processing
Pillow==10.1.0          # Image processing
pytesseract==0.3.10     # OCR capabilities
```

## Future Enhancements

Potential improvements for the project:
- Add more story templates
- Implement story customization (age ranges, themes)
- Add text-to-speech capabilities
- Create a frontend interface
- Add user authentication
- Implement story saving/favorites
- Support multiple languages
- Add audio narration

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Contact

[Add contact information here]

## Acknowledgments

Story content by Blue Bear
