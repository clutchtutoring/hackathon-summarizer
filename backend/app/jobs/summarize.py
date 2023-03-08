from ..services.summarizer import Summarizer

def process_summary(id: str, videoAssets: list):
    processor = Summarizer(id, videoAssets)

    result = processor.execute()

    return result
