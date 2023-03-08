from haystack.nodes import TransformersSummarizer
from haystack import Document
import ffmpeg
import whisper

# Extract Video Audio to mp3
stream = ffmpeg.input("../assets/videos/input.mp4")
stream = ffmpeg.output(stream, "../assets/audios/output.mp3")
ffmpeg.overwrite_output(stream)
ffmpeg.run(stream)

# Transcribe audio to text
model = whisper.load_model("base")
result = model.transcribe("../assets/audios/output.mp3")

# Summarize text
docs = [Document(result["text"])]

summarizer = TransformersSummarizer(model_name_or_path="google/pegasus-xsum")
summary = summarizer.predict(documents=docs)
result = summary[0].meta["summary"]

print(f"summary: {result}")