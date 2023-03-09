from ..services.summarizer import Summarizer

def process_summary(content_id: str, video_assets: list):
    """Process summary job"""
    processor = Summarizer(content_id, video_assets)

    result = processor.execute()

    return result
