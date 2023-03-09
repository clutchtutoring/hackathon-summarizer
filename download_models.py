import whisper
from haystack.nodes import TransformersSummarizer

whisper.load_model("base")
TransformersSummarizer(model_name_or_path="philschmid/bart-large-cnn-samsum")
