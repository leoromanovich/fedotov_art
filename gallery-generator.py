#!/usr/bin/env python3
import os
import json
import glob
import sys


def generate_gallery_manifest(gallery_dir="gallery"):
    """
    Scans the gallery directory for image files and their matching description files.
    Creates a manifest.json file with the gallery data.

    Expected structure for description files:
    description: Description of the artwork
    year: 2023
    price: $500

    Or simple text files will be used as just the description.
    """
    print(f"Scanning {gallery_dir} directory...")

    # Create gallery directory if it doesn't exist
    os.makedirs(gallery_dir, exist_ok=True)

    # Find all image files
    image_extensions = ["jpg", "jpeg", "png", "gif", "webp"]
    image_files = []

    for ext in image_extensions:
        image_files.extend(glob.glob(f"{gallery_dir}/*.{ext}"))

    # Sort image files alphabetically
    image_files.sort()

    gallery_data = []

    for image_path in image_files:
        base_name = os.path.splitext(image_path)[0]
        description_path = f"{base_name}.txt"

        # Default caption
        caption = "No description available"

        # Read description file if it exists
        if os.path.exists(description_path):
            try:
                with open(description_path, "r", encoding="utf-8") as file:
                    caption = file.read().strip()
            except Exception as e:
                print(f"Error reading description file {description_path}: {e}")
        else:
            print(f"Warning: No description file found for {image_path}")

        # Add to gallery data
        gallery_data.append({"image": image_path, "caption": caption})

    # Write manifest file
    manifest_path = os.path.join(gallery_dir, "manifest.json")
    try:
        with open(manifest_path, "w", encoding="utf-8") as file:
            json.dump(gallery_data, file, indent=2)
        print(f"Created manifest with {len(gallery_data)} images at {manifest_path}")
    except Exception as e:
        print(f"Error writing manifest file: {e}")
        return False

    return True


if __name__ == "__main__":
    # Use custom directory if provided as command line argument
    gallery_dir = sys.argv[1] if len(sys.argv) > 1 else "gallery"

    if generate_gallery_manifest(gallery_dir):
        print("Gallery manifest generated successfully!")
    else:
        print("Failed to generate gallery manifest.")
