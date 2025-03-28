#app/key_management.py
import os
import secrets
import string
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_secret_key(length=32):
    """Generate a random secret key of the specified length."""
    # Generate a random string of uppercase, lowercase, digits, and punctuation characters
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(characters) for _ in range(length))
    return secret_key

def check_and_create_secret_key():
    """Check if SECRET_KEY exists in environment variables, if not, generate and store it."""
    # First, check if the SECRET_KEY is already in the environment variables
    secret_key = os.getenv("SECRET_KEY")

    if secret_key is None:
        print("SECRET_KEY not found, generating a new one...")

        # If SECRET_KEY is not found, generate a new one
        secret_key = generate_secret_key()  # Generate a new secret key

        # Write the generated secret key to a .env file
        with open(".env", "a") as env_file:
            env_file.write(f"SECRET_KEY={secret_key}\n")

        # Optionally, set it in the environment temporarily for this session
        os.environ["SECRET_KEY"] = secret_key

        print(f"Generated and stored SECRET_KEY: {secret_key}")
    else:
        print("SECRET_KEY found in environment.")

    return secret_key


