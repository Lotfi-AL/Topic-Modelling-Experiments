from csv import DictWriter, DictReader
from pathlib import Path
import os
import pandas as pd
import re
import pickle
import zipfile

from utils.tables_and_plots import display_n_wordclouds

FILE_NAME = "File name"
NUMBER = "Number"
SUBTITLE = "Subtitle"
PROGRAM_ID = "Program ID"
TOKENIZED_SUBTITLES = "Tokenized subtitles"
STAT = "Stat"
VALUE = "Value"
RULE_NAME = "Rule name"
RULE_METHOD = "Rule method"
TOPIC_ID = "Topic ID"
TOPIC_WORDS = "Topic words"
WORD = "Word"
FREQUENCY = "Frequency"
WORD_PAIR = "Word pair"
CO_FREQUENCY = "Co-frequency"


def get_project_root() -> Path:
    return Path(__file__).parent.parent


ROOT_PATH = get_project_root()

def make_excerpt_wordcloud(formatted_topics,num_topics,text_to_show,num_topics_to_show = 8, random_sample=False,seed=None):
    import random
    k = num_topics_to_show
    topic_numeration = None
    if not seed:
        random.seed(41)
    else:
        random.seed(seed)
    if num_topics <= num_topics_to_show:
        k = num_topics
    if random_sample:
        excerpt_topics_indexed = random.sample(list(enumerate(formatted_topics)),k=k)
        excerpt_topics = []
        topic_numeration = []
        for idx,topic in excerpt_topics_indexed:
            topic_numeration.append(idx)
            excerpt_topics.append(topic)
    else:
        excerpt_topics = formatted_topics[:k]

    excerpt_wordcloud = display_n_wordclouds(excerpt_topics, text_to_show,
                                             k,topic_numeration=topic_numeration, dpi=200)
    #f"Sample from {model_name}-{embedding_model}: {data_type}"

    #excerpt_wordcloud.savefig(os.path.join(ROOT_PATH, folder_path_word_cloud, f"{file_name}_wordcloud_sample"))
    return excerpt_wordcloud


def load_from_file(folder_path, file_name,index_col=0) -> pd.DataFrame:
    file_path = os.path.join(
        ROOT_PATH, folder_path, "data", str(file_name))
    df = pd.read_csv(file_path,index_col=index_col)
    return df

def save_preprocessed_df_to_file(folder_path,file_name,df:pd.DataFrame) ->None:
    file_path = os.path.join(ROOT_PATH,folder_path, "data", str(file_name))
    df.to_csv(file_path,)

def write_topics_file(relative_folder_path, file_name,topics):
    file_path = os.path.join(ROOT_PATH, relative_folder_path)
    file_path = os.path.join(file_path,file_name)
    _write_csv_file(file_path, topics, key=TOPIC_ID, value=TOPIC_WORDS,
                    value_formatter=lambda value: ",".join(value))
    
# Load topics of model
def load_model_topics(relative_folder_path, file_name):
    file_path = os.path.join(ROOT_PATH, relative_folder_path)
    file_path = os.path.join(file_path, file_name)
    return _read_csv_file(file_path, key=TOPIC_ID, value=TOPIC_WORDS,
                          key_formatter=lambda key: int(key),
                          value_formatter=lambda value: value.split(","))

def _write_csv_file(file_path, data, key, value, key_formatter=lambda key: key, value_formatter=lambda value: value, reverse_key_value_order=False):
    #from pathlib import Path
    
    #filename = Path(file_path)
    #filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
    
    with open(file_path, encoding="utf-8", mode="w+", newline="") as file:
        writer = DictWriter(file, fieldnames=[key, value], delimiter=";")
        writer.writeheader()
        for (row_key, row_value) in data:
            row = {key: key_formatter(
                row_key), value: value_formatter(row_value)}
            if reverse_key_value_order:
                row = {key: value_formatter(
                    row_value), value: key_formatter(row_key)}
            writer.writerow(row)
            
# Write data word frequencies
def write_word_frequencies_file(relative_folder_path, file_name, word_frequencies):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + r".csv"))
    _write_csv_file(file_path, list(word_frequencies.items()),
                    key=WORD, value=FREQUENCY)


# Load data word frequencies
def load_word_frequencies(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + r".csv"))
    if os.path.exists(file_path):
        return _read_csv_file(file_path, key=WORD, value=FREQUENCY,
                          value_formatter=lambda value: int(value))
    else:
        return None

def load_zipped_word_co_frequencies(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + ".pkl"))
    with zipfile.ZipFile(file_path + ".zip", mode="r") as zipped_file:
        with zipped_file.open(file_name + ".pkl", mode="r") as file:
            return pickle.load(file)
        
        
# Write data word co-frequencies to regular CSV file
def write_word_co_frequencies_file(relative_folder_path, file_name, word_co_frequencies):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + ".csv"))
    _write_csv_file(file_path, word_co_frequencies, key=WORD_PAIR, value=CO_FREQUENCY,
                    key_formatter=lambda key: tuple(
                        re.sub(r"['\)\(]", "", key).split(",")),
                    value_formatter=lambda value: int(value))


# Load data word co-frequencies from regular CSV file
def load_word_co_frequencies(relative_folder_path, file_name):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + ".csv"))
    if os.path.exists(file_path):
        return _read_csv_file(file_path, key=WORD_PAIR, value=CO_FREQUENCY)
    else:
        return None


def _read_csv_file(file_path, key, value, key_formatter=lambda key: key, value_formatter=lambda value: value):
    data = {}
    with open(file_path, "r", encoding="utf-8") as file:
        reader = DictReader(file, delimiter=";")
        for row in reader:
            row_key = key_formatter(row[key])
            row_value = value_formatter(row[value])
            data[row_key] = row_value
    return data


# Write data word co-frequencies to zipped file
def write_word_co_frequencies_zip_file(relative_folder_path, file_name, word_co_frequencies):
    file_path = os.path.join(
        ROOT_PATH, relative_folder_path, str(file_name + ".pkl"))
    with zipfile.ZipFile(file_path + ".zip",
                         mode="w", compression=zipfile.ZIP_DEFLATED) as zipped_file:
        with zipped_file.open(file_name + ".pkl", mode="w", force_zip64=True) as file:
            pickle.dump(word_co_frequencies, file,
                        protocol=pickle.HIGHEST_PROTOCOL)

