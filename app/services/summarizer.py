import os
from haystack.nodes import TransformersSummarizer
from haystack import Document
from pySmartDL import SmartDL
import ffmpeg
import whisper
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class Summarizer:
    """Provides a service to summarize videos"""

    def __init__(self, content_id: str, video_assets: str):
        self.content_id = content_id
        self.video_assets = video_assets
        self.videos_path = self.get_path("../assets/videos")
        self.audios_path = self.get_path("../assets/audios")
        self.summaries_path = self.get_path("../assets/summaries")

    def get_path(self, path: str):
        """Get directory path"""
        dir_path = os.path.dirname(__file__)
        return os.path.join(dir_path, path)

    def download_video(self, video_id: str, url: str):
        """Download video"""
        ssl._create_default_https_context = ssl._create_unverified_context
        obj = SmartDL(url, f"{self.videos_path}/{video_id}.mp4", threads=10)
        obj.start()

    def convert_video(self, video_id: str):
        """Convert video to audio"""
        stream = ffmpeg.input(f"{self.videos_path}/{video_id}.mp4")
        stream = ffmpeg.output(stream, f"{self.audios_path}/{video_id}.mp3")
        ffmpeg.overwrite_output(stream).run()

    def transcribe_audio(self, video_id: str):
        """Transcribe audio"""
        model = whisper.load_model("base")
        result = model.transcribe(f"{self.audios_path}/{video_id}.mp3")

        return result["text"]

    def summarize_text(self, text: str):
        """Summarize text"""
        docs = [Document(text)]

        summarizer = TransformersSummarizer(model_name_or_path="philschmid/bart-large-cnn-samsum")
        summary = summarizer.predict(documents=docs)

        return summary[0].meta["summary"]

    def save_summary(self, text: str):
        """Save summary to file"""
        with open(f"{self.summaries_path}/{self.content_id}.txt", 'w', encoding="utf-8") as file:
            file.write(text)

    def execute(self):
        """Execute summarization process"""
        transcripts = ""
        summary_file = f"{self.summaries_path}/{self.content_id}.txt"

        if os.path.isfile(summary_file):
            with open(summary_file, "r", encoding="utf-8") as file:
                return file.read()

        for video in self.video_assets:
            if not os.path.isfile(f"{self.videos_path}/{video.id}.mp4"):
                self.download_video(video.id, video.url)

            if not os.path.isfile(f"{self.audios_path}/{video.id}.mp3"):
                self.convert_video(video.id)

            transcripts += self.transcribe_audio(video.id)

        summary = self.summarize_text(transcripts)

        self.save_summary(summary)

        return summary
