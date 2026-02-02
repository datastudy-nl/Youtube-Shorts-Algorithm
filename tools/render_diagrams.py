import zlib
import base64
import os
import requests
import string

# PlantUML Base64 Alphabet: 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_
plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
b64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def plantuml_encode(data):
    """Encodes a string to PlantUML's custom base64 format."""
    # 1. Compress using Deflate (zlib)
    zlibbed = zlib.compress(data.encode('utf-8'))
    # Strip zlib header (first 2 bytes) and checksum (last 4 bytes) for raw deflate
    compressed = zlibbed[2:-4]
    
    # 2. Base64 Encode
    b64_encoded = base64.b64encode(compressed).decode('utf-8')
    
    # 3. Transliterate to PlantUML alphabet
    maketrans = str.maketrans(b64_alphabet, plantuml_alphabet)
    return b64_encoded.translate(maketrans)

def render_puml(puml_path, output_path):
    with open(puml_path, 'r') as f:
        content = f.read()
    
    encoded = plantuml_encode(content)
    url = f"http://www.plantuml.com/plantuml/svg/{encoded}"
    
    print(f"Fetching {puml_path} from {url}...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Saved to {output_path}")
        else:
            print(f"Error fetching {url}: {response.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    puml_dir = "assets/puml"
    svg_dir = "assets/svg"
    
    if not os.path.exists(svg_dir):
        os.makedirs(svg_dir)
        
    for filename in os.listdir(puml_dir):
        if filename.endswith(".puml"):
            puml_path = os.path.join(puml_dir, filename)
            svg_path = os.path.join(svg_dir, filename.replace(".puml", ".svg"))
            render_puml(puml_path, svg_path)
