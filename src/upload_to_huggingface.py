import os
from huggingface_hub import HfApi, create_repo, login
from config_loader import load_config  

class HuggingFaceUploader:
    def __init__(self, config_path="config/config.yaml"):
        # Load configuration from the YAML file using config_loader
        self.config = load_config(config_path)
        self.token = os.getenv(self.config['huggingface']['token_env_var'])

        if not self.token:
            print(f"Error: {self.config['huggingface']['token_env_var']} environment variable not set")
            print(f"Please set your token using: export {self.config['huggingface']['token_env_var']}='your_token_here'")
            return

        try:
            login(token=self.token)
            print("Successfully logged in to Hugging Face")
        except Exception as e:
            print(f"Error logging in: {e}")
            return

        # Initialize Hugging Face API
        self.api = HfApi()

        # Repository details from config
        self.repo_id = self.config['huggingface']['repo_id']

    def create_repo(self):
        """Create repository if it doesn't exist."""
        try:
            create_repo(self.repo_id, repo_type="dataset", exist_ok=True)
            print(f"Repository {self.repo_id} created/verified successfully")
        except Exception as e:
            print(f"Error creating repository: {e}")
            return False
        return True

    def upload_files(self):
        """Upload the Parquet files to Hugging Face."""
        # Path to data folder from config
        data_dir = self.config['paths']['output_directory']

        if not os.path.exists(data_dir):
            print(f"Error: Data directory not found: {data_dir}")
            return

        print(f"\nUploading data folder: {data_dir}")

        try:
            self.api.upload_folder(
                folder_path=data_dir,
                path_in_repo="data",
                repo_id=self.repo_id,
                repo_type="dataset"
            )
            print("Successfully uploaded data folder")
        except Exception as e:
            print(f"Error uploading data folder: {e}")
            return

        print("\nUpload process completed!")
