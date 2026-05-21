
import pandas as pd
import zipfile
import os
import glob
import pandas as pd
from datetime import datetime

# logger function
from datetime import datetime


def log_event(message, log_file="log_file.txt"):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'  # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now()  # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(log_file, "a") as f:
        f.write(timestamp + ',' + message + '\n')


def unzip_file(zip_file, output_folder):
    # create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)


# functions to extract different file formats


def extract_csv(file_to_process) -> pd.DataFrame:
    dataframe = pd.read_csv(file_to_process)
    return dataframe


def extract_json(file_to_process) -> pd.DataFrame:
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe


def extract_xml(file_to_process) -> pd.DataFrame:
    """Extracts data from an XML file and returns a DataFrame."""
    return pd.read_xml(file_to_process)


# extract data from all files and concatenate into a single DataFrame
def extract_data(path_to_files) -> pd.DataFrame:
    """
    Extracts data from all files in the specified directory and concatenates them into a single DataFrame."""
    all_files = glob.glob(path_to_files + "/*")
    dataframe_list = []
    for file in all_files:
        if file.endswith(".csv"):
            dataframe_list.append(extract_csv(file))
        elif file.endswith(".json"):
            dataframe_list.append(extract_json(file))
        elif file.endswith(".xml"):
            dataframe_list.append(extract_xml(file))
    return pd.concat(dataframe_list, ignore_index=True)


# load to a csv file
def load_data(target_file, transformed_data: pd.DataFrame):
    transformed_data.to_csv(target_file, index=False)
