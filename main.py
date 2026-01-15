import requests
import json
import base64

from config import REVE_API_KEY



headers = {
    "Authorization": f"Bearer {REVE_API_KEY}", 
    "Accept": "application/json",
    "Content-Type": "application/json"
}

class ReveApi:
    def __init__(self, api_key):
        self.URL = "https://api.reve.com/v1/"
        self.headers = {
            "Authorization": f"Bearer {api_key}", 
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        


    def generate_reve_image(self,
        prompt,
        aspect_ratio="16:9",
        version="latest",
        save_json="reve_output.json",
        save_image="reve_image.png"
    ):
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "version": version
        }

        try:
            response = requests.post(
                
                self.URL + "image/create",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            result = response.json()

            # Save JSON response
            if save_json:
                with open(save_json, "w") as f:
                    json.dump(result, f, indent=4)

            print(f"Request ID: {result.get('request_id')}")
            print(f"Credits used: {result.get('credits_used')}")
            print(f"Credits remaining: {result.get('credits_remaining')}")

            # Convert base64 image to PNG
            if result.get("image"):
                try:
                    image_data = base64.b64decode(result["image"])

                    if save_image:
                        with open(save_image, "wb") as img_file:
                            img_file.write(image_data)

                    print(f"Image saved to {save_image}")
                except Exception as e:
                    print(f"Failed to decode base64 image: {e}")

            if result.get("content_violation"):
                print("Warning: Content policy violation detected")
            else:
                print("Image generated successfully")

            return result

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Failed to parse response: {e}")
            return None
    def safe_reve_image(self, base64_string, file_path):
        decoded_data = base64.b64decode(base64_string)
        with open(file_path, "wb") as file:
            file.write(decoded_data)
        print(f"Image saved to {file_path}")


reve_api = ReveApi(REVE_API_KEY)