import os
from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import nltk


nltk.download('punkt', quiet=True)

def extract_audio(video_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_path = video_path + '.wav'
        video_clip.audio.write_audiofile(audio_path, logger=None)
        return audio_path
    except Exception as e:
        raise Exception(f"Error extracting audio: {str(e)}")

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    transcribed_text = ""

    audio = AudioSegment.from_file(audio_path)
    duration_ms = len(audio)
    chunk_length_ms = 60 * 1000  # 1-minute chunks
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, duration_ms, chunk_length_ms)]

    for i, chunk in enumerate(chunks):
        chunk_filename = f"{audio_path}_chunk_{i}.wav"
        chunk.export(chunk_filename, format='wav')

        with sr.AudioFile(chunk_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                transcribed_text += text + " "
            except sr.UnknownValueError:
                transcribed_text += "[Unintelligible] "
            except sr.RequestError as e:
                transcribed_text += f"[Error: {e}] "

        # Remove the chunk file
        os.remove(chunk_filename)

    return transcribed_text

def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)

    summary_sentences = [str(sentence) for sentence in summary]
    return ' '.join(summary_sentences)

