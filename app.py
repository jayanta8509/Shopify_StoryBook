from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
from stroy_one import story_male_one
from stroy_two import story_male_two
from stroy_one import story_female_one
from stroy_two import story_female_two

# Initialize FastAPI app
app = FastAPI(
    title="Story Generator API",
    description="A FastAPI application for story generation",
    version="1.0.0"
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount media folder for all static files
app.mount("/media", StaticFiles(directory="media"), name="media")


class StoryRequest(BaseModel):
    name: str
    story_id: int
    gender: str

def get_all_page_images(page_number: int, story_folder: str) -> list:
    """Get all images for a specific page"""
    possible_extensions = ['.jpeg', '.jpg', '.png']
    images = []
    image_index = 1
    
    # Keep checking for images until no more are found
    while True:
        found = False
        for ext in possible_extensions:
            image_path = os.path.join("media", story_folder, f"page_{page_number}_image_{image_index}{ext}")
            if os.path.exists(image_path):
                images.append(f"page_{page_number}_image_{image_index}{ext}")
                found = True
                break
        
        if not found:
            break
        image_index += 1
    
    # If no images found, return default
    if not images:
        images.append(f"page_{page_number}_image_1.jpeg")
    
    return images

@app.post("/generate-story")
async def generate_story(request: StoryRequest, req: Request):
    """
    Generate a story based on the name and story_id
    
    Args:
        name: The character name to use in the story
        story_id: The story identifier (e.g., 1 for story_one, 2 for story_two)
    
    Returns:
        A list of pages with page number, content, and image path
    """
    # Map story_id to story function and folder
    story_mapping = {
        1: {"function": story_male_one if request.gender == "male" else story_female_one, "folder": f"store_one/{request.gender}"},
        2: {"function": story_male_two if request.gender == "male" else story_female_two, "folder": f"store_two/{request.gender}"}
    }
    
    if request.story_id not in story_mapping:
        raise HTTPException(status_code=404, detail=f"Story with id '{request.story_id}' not found")
    
    # Get the story function and folder
    story_config = story_mapping[request.story_id]
    pages = await story_config["function"](request.name)
    story_folder = story_config["folder"]
    
    # Get base URL from request
    base_url = str(req.base_url).rstrip('/')
    
    # Build response with page-wise data
    response_pages = []
    for i in range(len(pages)):
        page_number = i + 1
        # Get all images for this page
        images = get_all_page_images(page_number, story_folder)
        
        # Build full URLs for all images
        image_paths = [f"{base_url}/media/{story_folder}/{img}" for img in images]
        
        response_pages.append({
            "page_number": page_number,
            "content": pages[i],
            "image_path": image_paths
        })
    
    return {
        "story_id": request.story_id,
        "name": request.name,
        "pages": response_pages
    }

@app.get("/")
async def root():
    return {
        "message": "Story Generator API",
        "usage": "POST /generate-story with {name: 'your_name', story_id: 1 or 2}",
        "available_stories": [1, 2]
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )