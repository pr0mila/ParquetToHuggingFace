# src/create_parquet.py
import os
import pandas as pd
import soundfile as sf
import numpy as np
import librosa
import sys
import os

from config_loader import load_config  
from datasets import Dataset, Audio, Features, Value


class ParquetFileCreator:
    def __init__(self, config_path="config/config.yaml"):
        # Load configuration from the YAML file using config_loader
        self.config = load_config(config_path)
        
        # Set directories from config
        self.base_dir = self.config['paths']['base_data_directory']
        self.output_dir = self.config['paths']['output_directory']
        os.makedirs(self.output_dir, exist_ok=True)

        # Define features schema
        self.features = Features({
            "audio": Audio(sampling_rate=16000),
            "text": Value("string"),
            "translation": Value("string"),
            "speaker_name": Value("string"),
            "utterance_pitch_mean": Value("float32"),
            "utterance_pitch_std": Value("float32")
        })

    def calculate_pitch_stats(self, audio_path):
        """Calculate pitch mean and standard deviation for an audio file."""
        try:
            y, sr = librosa.load(audio_path)
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitches_with_magnitudes = pitches[magnitudes > np.max(magnitudes) * 0.1]
            if len(pitches_with_magnitudes) > 0:
                return float(np.mean(pitches_with_magnitudes)), float(np.std(pitches_with_magnitudes))
        except:
            pass
        return 0.0, 0.0

    def process_data(self, data_file, data_type="train"):
        """Process CSV data and create corresponding Parquet files."""
        print(f"\nProcessing {data_type} data...")
        data_df = pd.read_csv(os.path.join(self.base_dir, f"{data_type}/{data_type}.csv"))
        data_list = []

        for idx, row in data_df.iterrows():
            audio_path = os.path.join(self.base_dir, data_type, row["path"])
            if os.path.exists(audio_path):
                # Read audio file
                audio, sr = sf.read(audio_path)
                
                # Calculate pitch statistics
                pitch_mean, pitch_std = self.calculate_pitch_stats(audio_path)
                
                # Create sample
                sample = {
                    "audio": {"array": audio, "sampling_rate": sr},
                    "text": row["code-switched transcription"],
                    "translation": row["translation"],
                    "speaker_name": row["gender"],
                    "utterance_pitch_mean": pitch_mean,
                    "utterance_pitch_std": pitch_std
                }
                data_list.append(sample)

                # Print progress
                if (idx + 1) % 10 == 0:
                    print(f"Processed {idx + 1} {data_type} samples")

                # Print first 3 samples for verification
                if idx < 3:
                    print(f"\nSample {idx + 1}:")
                    print(f"Text: {sample['text']}")
                    print(f"Speaker: {sample['speaker_name']}")
                    print(f"Audio duration: {len(audio)/sr:.2f}s")
                    print(f"Pitch mean: {pitch_mean:.2f}")
                    print(f"Pitch std: {pitch_std:.2f}")

        # Create and save Parquet file
        print(f"\nCreating {data_type} parquet file... ({len(data_list)} samples)")
        dataset = Dataset.from_list(data_list, features=self.features)
        dataset.to_parquet(os.path.join(self.output_dir, f"{data_type}-00000-of-00001.parquet"))
        print(f"{data_type.capitalize()} parquet file created successfully!")

    def create_parquet_files(self):
        """Main method to create both train and test parquet files."""
        self.process_data("train", data_type="train")
        self.process_data("test", data_type="test")
        print("\nAll parquet files created successfully!")


