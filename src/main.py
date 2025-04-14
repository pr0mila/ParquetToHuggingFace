from create_parquet import ParquetFileCreator
from upload_to_huggingface import HuggingFaceUploader

config_path = "/Users/promilaghosh/VS-Code-Projects/ParquetToHuggingFace/config/config.yaml"

def main():
    # Create an instance of the ParquetFileCreator class to create Parquet files
    parquet_creator = ParquetFileCreator(config_path)
    parquet_creator.create_parquet_files()

    # After creating Parquet files, upload them to Hugging Face
    hf_uploader = HuggingFaceUploader(config_path)
    if hf_uploader.create_repo():
        hf_uploader.upload_files()

if __name__ == "__main__":
    main()
