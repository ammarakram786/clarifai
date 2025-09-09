import secrets
import string

def generate_secure_token(length=32):
    """Generate a secure random token"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_api_bearer_token(length=40):
    """Generate a secure API bearer token"""
    alphabet = string.ascii_letters + string.digits + '-_'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    print("=== SECURE TOKEN GENERATION ===")
    print()
    print("NEW API BEARER TOKEN:")
    print(f"API_BEARER_TOKEN={generate_api_bearer_token()}")
    print()
    print("IMPORTANT SECURITY NOTES:")
    print("1. Replace the old Clarifai PAT with a new one from your Clarifai dashboard")
    print("2. Use the generated API_BEARER_TOKEN above")
    print("3. Never commit these tokens to version control")
    print("4. Set these as environment variables in your deployment platform")
    print()
    print("Required environment variables for deployment:")
    print("- CLARIFAI_PAT (get new one from Clarifai)")
    print("- CLARIFAI_USER_ID")
    print("- CLARIFAI_APP_ID") 
    print("- CLARIFAI_MODEL_ID")
    print("- CLARIFAI_MODEL_VERSION_ID")
    print("- API_BEARER_TOKEN (use the generated one above)")
