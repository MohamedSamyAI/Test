import streamlit as st
import openai
from langchain_community.document_loaders import YoutubeLoader
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser

# Configure your OpenAI API key:
# For Streamlit Cloud, place your API key in the secrets (e.g., st.secrets["OPENAI_API_KEY"])
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your_openai_api_key_here"

def get_transcript_captions(url, language=["en"]):
    """
    Try to get the transcript using YoutubeLoader (which uses YouTube's captions).
    """
    try:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=False, language=language)
        docs = loader.load()
        if docs and docs[0].page_content.strip():
            return docs[0].page_content
        else:
            return None
    except Exception as e:
        st.error(f"Error using captions loader: {e}")
        return None

def get_transcript_audio(url, save_dir="docs/youtube/"):
    """
    If captions aren't available, fall back to extracting audio and transcribing it.
    This method uses YoutubeAudioLoader and OpenAIWhisperParser.
    """
    try:
        loader = GenericLoader(
            YoutubeAudioLoader([url], save_dir),
            OpenAIWhisperParser(api_key=openai.api_key)
        )
        docs = loader.load()
        if docs and docs[0].page_content.strip():
            return docs[0].page_content
        else:
            return None
    except Exception as e:
        st.error(f"Error during audio transcription: {e}")
        return None

def main():
    st.title("YouTube Transcript Extractor")
    
    video_url = st.text_input("Enter YouTube Video URL:")
    
    if st.button("Extract Transcript") and video_url:
        st.info("Extracting transcript, please wait...")
        transcript = get_transcript_captions(video_url)
        
        if transcript:
            st.success("Transcript found using YouTube captions!")
            st.text_area("Transcript", transcript, height=500)
        else:
            st.warning("No captions found. Falling back to audio transcription...")
            transcript_audio = get_transcript_audio(video_url)
            if transcript_audio:
                st.success("Transcript extracted from audio!")
                st.text_area("Transcript", transcript_audio, height=500)
            else:
                st.error("Failed to extract transcript via both methods.")

if __name__ == "__main__":
    main()
