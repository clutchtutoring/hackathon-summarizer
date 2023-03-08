import os
from haystack.nodes import TransformersSummarizer
from haystack import Document
from pySmartDL import SmartDL
import ffmpeg
import whisper

class Summarizer:
    def __init__(self, id: str, videoAssets: str):
        self.id = id
        self.videoAssets = videoAssets
        self.videos_path = "./app/assets/videos"
        self.audios_path = "./app/assets/audios"
        self.summaries_path = "./app/assets/summaries"

    def download_video(self, videoId: str, url: str):
        obj = SmartDL(url, f"{self.videos_path}/{videoId}.mp4")
        obj.start()

        print(f"Downloaded: {obj.get_dest()}")
        
    def convert_video(self, videoId: str):
        stream = ffmpeg.input(f"{self.videos_path}/{videoId}.mp4")
        stream = ffmpeg.output(stream, f"{self.audios_path}/{videoId}.mp3")
        ffmpeg.overwrite_output(stream).run()

    def transcribe_audio(self, videoId: str):
        model = whisper.load_model("base")
        result = model.transcribe(f"{self.audios_path}/{videoId}.mp3")

        return result["text"]

    def summarize_text(self, text: str):
        docs = [Document(text)]

        summarizer = TransformersSummarizer(model_name_or_path="philschmid/bart-large-cnn-samsum")
        summary = summarizer.predict(documents=docs)

        return summary[0].meta["summary"]

    def save_summary(self, text: str):
        with open(f"{self.summaries_path}/{self.id}.txt", 'w') as f:
            f.write(text)

    def execute(self):
        transcripts = ""

        for video in self.videoAssets:
            self.download_video(video.id, video.url)
            self.convert_video(video.id)
            transcripts += self.transcribe_audio(video.id)

        summary = self.summarize_text(transcripts)

        self.save_summary(summary)

        print("summary: ", summary)

        return summary

