from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime
from pathlib import Path
from stroy_one import story_male_one
from stroy_two import story_male_two
from stroy_one import story_female_one
from stroy_two import story_female_two
from pptx_replacer import PowerPointReplacer
from pptx_to_pdf import pptx_to_pdf

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

class PptxRequest(BaseModel):
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

@app.post("/generate-pptx")
async def generate_pptx(request: PptxRequest, req: Request):
    """
    Generate a personalized PowerPoint storybook
    
    Args:
        name: The character name to use in the story
        story_id: The story identifier (e.g., 1 for story_one, 2 for story_two)
        gender: The gender (male or female)
    
    Returns:
        A JSON response with the download URL for the generated PPTX
    """
    try:
        # Validate story_id
        if request.story_id not in [1, 2]:
            raise HTTPException(status_code=404, detail=f"Story with id '{request.story_id}' not found")
        
        # Validate gender
        if request.gender.lower() not in ["male", "female"]:
            raise HTTPException(status_code=400, detail="Gender must be 'male' or 'female'")
        
        # Map story_id and gender to template files
        template_mapping = {
            (1, "male"): "story_book/Storybook_Template_1_male.pptx",
            (1, "female"): "story_book/Storybook_Template_1_female.pptx",
            (2, "male"): "story_book/Storybook_Template_2_male.pptx",
            (2, "female"): "story_book/Storybook_Template_2_female.pptx"
        }

        template_cover_mapping = {
            (1, "male"): "story_book/cover/Storybook_cover_1_male.pptx",
            (1, "female"): "story_book/Storybook_cover_1_female.pptx",
            (2, "male"): "story_book/Storybook_cover_2_male.pptx",
            (2, "female"): "story_book/Storybook_cover_2_female.pptx"
        }
        
        # Get the appropriate template based on story_id and gender
        template_key = (request.story_id, request.gender.lower())
        template_path = template_mapping.get(template_key)
        template_path_cover = template_cover_mapping.get(template_key)
        
        if not template_path:
            raise HTTPException(status_code=400, detail=f"No template found for story_id={request.story_id} and gender={request.gender}")
        
        # Check if template exists
        if not os.path.exists(template_path):
            raise HTTPException(status_code=500, detail=f"Template file not found: {template_path}")
        
        # Create timestamp for unique folder name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create folder name: name_gender_timestamp (e.g., emma_male_20251030_143025)
        folder_name = f"{request.name.lower()}_{request.gender.lower()}_{timestamp}"
        output_dir = Path("media") / folder_name
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create replacer instance
        replacer = PowerPointReplacer(template_path)
        replacer_cover =  PowerPointReplacer(template_path_cover)
        
        # Prepare replacements
        replacements = {
            '{{Child_Name}}': request.name,
            '{{CHILD_NAME_UPPER}}': request.name.upper()
        }
        
        # Generate output filename
        output_filename = f"{request.name}_Storybook.pptx"
        output_path = output_dir / output_filename
        
        output_filename_cover = f"{request.name}_cover_Storybook.pptx"
        output_path_cover = output_dir / output_filename_cover

        # Replace text and save
        created_file = replacer.replace_text(replacements, str(output_path))

        created_file_cover = replacer_cover.replace_text(replacements, str(output_path_cover))

        # Convert pptx to pdf
        pdf_path = pptx_to_pdf(str(output_path))

        pdf_path_cover = pptx_to_pdf(str(output_path_cover))

        # Extract just the PDF filename from the full path
        pdf_filename = Path(pdf_path).name
        pdf_filename_cover = Path(pdf_path_cover).name

        # Get base URL from request
        base_url = str(req.base_url).rstrip('/')
        
        # Build download URL
        download_url = f"{base_url}/media/{folder_name}/{output_filename}"
        download_url_pdf = f"{base_url}/media/{folder_name}/{pdf_filename}"

        download_cover_url = f"{base_url}/media/{folder_name}/{output_filename_cover}"
        download_cover_url_pdf = f"{base_url}/media/{folder_name}/{pdf_filename_cover}"
        
        return {
            "success": True,
            "message": "PowerPoint generated successfully",
            "name": request.name,
            "story_id": request.story_id,
            "gender": request.gender,
            "download_url": download_url,
            "download_url_pdf": download_url_pdf,
            "download_cover_url": download_cover_url,
            "download_cover_url_pdf": download_cover_url_pdf,
            "status": "success",
            "status_code": 200
        }
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PowerPoint: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Story Generator API",
        "endpoints": {
            "generate_story": "POST /generate-story with {name: 'your_name', story_id: 1 or 2, gender: 'male' or 'female'}",
            "generate_pptx": "POST /generate-pptx with {name: 'your_name', story_id: 1 or 2, gender: 'male' or 'female'}"
        },
        "available_stories": [1, 2],
        "available_genders": ["male", "female"]
    }

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )