<p align="right">
<img src="https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg" alt="License: CC BY 4.0" />
  <a href="https://huggingface.co/datasets/pr0mila-gh0sh/MediBeng">
    <img src="https://img.shields.io/badge/🤗%20Dataset-MediBeng-yellow?link=https://huggingface.co/datasets/pr0mila-gh0sh/MediBeng" alt="Hugging Face Dataset" />
  </a>
  <a href="https://doi.org/10.57967/hf/5187">
    <img src="https://img.shields.io/badge/DOI-10.57967%2Fhf%2F5187-blue" alt="Dataset DOI" />
  </a>
  <a href="https://doi.org/10.1101/2025.04.25.25326406">
    <img src="https://img.shields.io/badge/medRxiv-10.1101%2F2025.04.25.25326406-0077cc" alt="medRxiv Preprint" />
  </a>
  <a href="https://paperswithcode.com/sota/speech-to-text-translation-on-medibeng?p=medibeng-whisper-tiny-a-fine-tuned-code">
    <img src="https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/medibeng-whisper-tiny-a-fine-tuned-code/speech-to-text-translation-on-medibeng" alt="PWC" />
  </a>
</p>

# ParquetToHuggingFace :package:

This project processes **MediBeng** audio data and creates Parquet files for uploading to Hugging Face. It uses the following two main scripts:

- **`create_parquet.py`**: This script is used to create Parquet files from the synthetic **Bengali-English code-switched audio data** in healthcare settings. :musical_note:
- **`upload_to_huggingface.py`**: This script uploads the Parquet files to Hugging Face, making the **MediBeng** dataset publicly available for sharing and usage. :cloud:

### Explore the MediBeng Dataset : [MediBeng Dataset on Hugging Face](https://huggingface.co/datasets/pr0mila-gh0sh/MediBeng) 🤗

<p align="left">
  <img src="https://raw.githubusercontent.com/pr0mila/ParquetToHuggingFace/main/medbeng.png" width="300"/>
</p>


I followed the steps above to create the **MediBeng** dataset, which contains audio data along with their transcriptions, and uploaded it to Hugging Face. You can explore the dataset [here](https://huggingface.co/datasets/pr0mila-gh0sh/MediBeng).

## Table of Contents
- [1. Cloning the Repository](#1-cloning-the-repository) :book:
- [2. Setting Up the Conda Environment](#2-setting-up-the-conda-environment) :wrench:
- [3. Installing Dependencies](#3-installing-dependencies) :floppy_disk:
- [4. Setting Up Hugging Face Token](#4-setting-up-hugging-face-token) :lock:
- [5. Configuring the `config.yaml`](#5-configuring-the-configyaml) :gear:
- [6. Data Setup](#6-data-setup) :file_folder:
- [7. Running the Scripts](#7-running-the-scripts) :rocket:
- [8. How the Code Works](#8-how-the-code-works) :memo:
- [9. Loading the MediBeng Dataset](#9-loading-the-medibeng-dataset) :arrow_down:
- [10. Summary of Updates](#10-summary-of-updates) :clipboard:

## 1. Cloning the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/pr0mila/ParquetToHuggingFace.git
cd ParquetToHuggingFace
```

## 2. Setting Up the Conda Environment

Create a new Conda environment to run the project:

```bash
conda create --name audio-parquet python=3.9
conda activate audio-parquet
```

## 3. Installing Dependencies

Install the necessary dependencies by using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
Or, install the dependencies

```bash
pip install pandas soundfile numpy librosa datasets
```

This will install all the required libraries and packages to run the project.

## 4. Setting Up Hugging Face Token

You need to set your Hugging Face token as an environment variable to upload data to Hugging Face. Run the following command in your terminal (replace `your_token_here` with your actual token):

```bash
export HUGGINGFACE_TOKEN='your_token_here'
```

You can find your Hugging Face token by visiting [Hugging Face - Account Settings](https://huggingface.co/settings/tokens).

To ensure the token persists across sessions, you can add the `export` command to your shell's configuration file (e.g., `~/.bashrc` or `~/.zshrc`).

## 5. Configuring the `config.yaml`

The `config.yaml` file stores the configuration for the paths and Hugging Face repository settings.

Make sure to update the `config.yaml` according to your local setup. Example:

```yaml
paths:
  base_data_directory: "/path/to/your/raw/data"
  output_directory: "/path/to/store/parquet"

huggingface:
  repo_id: "your_username/your_dataset_name"
  token_env_var: "HUGGINGFACE_TOKEN"
```

- `base_data_directory`: Path to your directory where the raw audio files and CSV files are located (it will be in the `raw data` directory).
- `output_directory`: Path to where the Parquet files will be saved (this will be in the `processed_data` directory).
- `repo_id`: Your Hugging Face repository ID where you want to upload the dataset.

## 6. Data Setup

Place your raw audio data and its corresponding CSV file into the `raw data` directory. The audio files should be in a format that the `create_parquet.py` script can read (e.g., `.wav` files).

Your directory structure should look like this:

```
ParquetToHuggingFace/
├── data/
│   ├── raw_data/
│   │   ├── test/
│   │   └── train/
│   └── processed_data/
├── config.yaml
└── src/
    ├── create_parquet.py
    └── upload_to_huggingface.py
```

## 7. Running the Scripts

### Step 1: Update Config Path in `main.py`

Before running the scripts, make sure to update the path of your `config.yaml` file in `src/main.py` to reflect your local configuration. This will ensure the scripts use the correct settings.

### Step 2: Run `main.py` for Final Output

Once the config path is updated, run the `main.py` file to generate the final output:

```bash
python3 src/main.py
```

## 8. How the Code Works

### `create_parquet.py`:
- The `create_parquet.py` class processes raw audio data and its corresponding CSV file (which contains transcription and translation).
- It calculates pitch statistics (mean and standard deviation) for each audio file.
- The processed data, including audio, transcription, translation, and pitch statistics, is then saved as Parquet files in the `processed_data` directory.

### `upload_to_huggingface.py`:
- The `upload_to_huggingface.py` class logs you into Hugging Face using the token set in your environment.
- It checks whether the repository exists or needs to be created on Hugging Face.
- Finally, it uploads the Parquet files from the `processed_data` directory to your Hugging Face repository.


---

### Final Outcome:


![View of Final Outcome](parquettohuggingface.png)

Once the scripts are successfully run, your data will be stored on Hugging Face as Parquet files, and you will have the ability to share and use them for various machine learning or research purposes.

## 9. Loading the MediBeng Dataset

This guide demonstrates how to load the "MediBeng" dataset for use in your machine learning or research projects.

First, install the necessary dependencies by running the following command:

```bash
pip install datasets[audio]

To begin working with the **MediBeng** dataset, follow these steps to load both the training and test splits.

The code below will load the dataset and allow you to take a quick look at the first three examples from the training split.

```python
from datasets import load_dataset

# Load the dataset with both train and test splits
ds = load_dataset("pr0mila-gh0sh/MediBeng", split=["train", "test"])

# Take the first three examples from the training part
ds_head = ds[0].take(3)
```
## 10. Summary of Updates

1. **Processing Parquet files**: Added steps to convert and process Parquet files containing audio data.
   
2. **Storing on Hugging Face**: Instructions on how to store datasets on Hugging Face after processing them.

3. **Loading from Hugging Face**: After uploading the dataset to Hugging Face, we can load it into the Python environment using the `load_dataset()` method with the appropriate path.

4. **Example of Dataset MediBeng Storing and Loading**: The code snippet demonstrates how to load the MediBeng dataset from Hugging Face.




