"""
StreetWhere Image Download Script
Automatically downloads streetwear product images from high-quality sources
"""

import requests
import os
from urllib.parse import urlparse
import time

# High-quality streetwear product image URLs
PRODUCT_IMAGES = {
    'hoodies': [
        'https://images.unsplash.com/photo-1556821840-3a63f95609a7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',  # Black hoodie
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Gray hoodie
        'https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # White hoodie
        'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Orange hoodie
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Blue hoodie
        'https://images.unsplash.com/photo-1620143504942-1b7e5c1c6342?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Maroon hoodie
    ],
    't-shirts': [
        'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Black t-shirt
        'https://images.unsplash.com/photo-1583743814966-8936f37f3804?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # White t-shirt
        'https://images.unsplash.com/photo-1576566588028-4147f3842f27?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Graphic t-shirt
        'https://images.unsplash.com/photo-1582552938357-32b906df40cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Vintage t-shirt
        'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Orange t-shirt
        'https://images.unsplash.com/photo-1571945153237-4929e783af4a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Navy t-shirt
    ],
    'sneakers': [
        'https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # White sneakers
        'https://images.unsplash.com/photo-1595950653106-6c9739b7817c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Black sneakers
        'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Red sneakers
        'https://images.unsplash.com/photo-1556906781-9a412961c28c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # High-top sneakers
        'https://images.unsplash.com/photo-1600269452121-4f2416e55c28?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Vintage sneakers
        'https://images.unsplash.com/photo-1512374382149-233c42b6a83b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Running sneakers
    ],
    'jackets': [
        'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Denim jacket
        'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Leather jacket
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Bomber jacket
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Track jacket
        'https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Windbreaker
        'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Puffer jacket
    ],
    'pants': [
        'https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Black jeans
        'https://images.unsplash.com/photo-1582552938357-32b906df40cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Distressed jeans
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Joggers
        'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Cargo pants
        'https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Sweatpants
        'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Shorts
    ],
    'accessories': [
        'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Baseball cap
        'https://images.unsplash.com/photo-1521369909029-2afed882baee?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Sunglasses
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Backpack
        'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Chain necklace
        'https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Watch
        'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',  # Beanie
    ]
}

def download_image(url, filepath):
    """Download image from URL and save to filepath"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"✓ Downloaded: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"✗ Failed to download {url}: {e}")
        return False

def main():
    """Download all streetwear product images"""
    base_dir = r"c:\Users\user\Desktop\shopifydj\image ni dj"
    
    # Ensure base directory exists
    os.makedirs(base_dir, exist_ok=True)
    
    for category, urls in PRODUCT_IMAGES.items():
        category_dir = os.path.join(base_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        print(f"\n📁 Downloading {category.title()} images...")
        
        for i, url in enumerate(urls, 1):
            filename = f"{category}_{i:02d}.jpg"
            filepath = os.path.join(category_dir, filename)
            
            # Skip if file already exists
            if os.path.exists(filepath):
                print(f"⚠ Skipping {filename} (already exists)")
                continue
            
            download_image(url, filepath)
            time.sleep(1)  # Be respectful to the server
    
    print(f"\n🎉 All images downloaded to: {base_dir}")
    print("\nImage structure:")
    for category in PRODUCT_IMAGES.keys():
        category_dir = os.path.join(base_dir, category)
        if os.path.exists(category_dir):
            file_count = len([f for f in os.listdir(category_dir) if f.endswith('.jpg')])
            print(f"  📂 {category}: {file_count} images")

if __name__ == "__main__":
    print("🏪 StreetWhere Image Downloader")
    print("=" * 40)
    main()
