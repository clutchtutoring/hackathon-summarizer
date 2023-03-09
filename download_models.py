import ssl

import whisper
from haystack.nodes import TransformersSummarizer

ssl._create_default_https_context = ssl._create_unverified_context

whisper.load_model("base")
TransformersSummarizer(model_name_or_path="philschmid/bart-large-cnn-samsum")
