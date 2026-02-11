import re
import os
import csv
import pandas as pd
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled  
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

def get_video_url(url):
  #extract the video id from the url
  video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
  return video_id_match.group(1) if video_id_match else None  

def get_video_title(video_id):
  #build the youtube service
  youtube = build('youtube', 'v3', developerKey = api_key)

  #fetch video details
  request = youtube.videos().list(
    part='snippet',
    id=video_id
  )  

  response = request.execute()

  #extract the title
  title = response['items'][0]['snippet']['title'] if response['items'] else 'Unknown Title'
  return title

def get_video_transcript(video_id):
  #fetch the transcript
  try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
    return transcript
  except TranscriptsDisabled:
      print(f"Transcripts are disabled for video: {video_id}")
      return []
  except Exception as e:
    print(f"An error occured: {e}")
    return[]

def save_to_csv(title, transcript, filename):
  #save the title and transcript to a csv file
  transcript_data = [{'start': entry['start'], 'text': entry['text']} for entry in transcript]

  df = pd.DataFrame(transcript_data)
  df.to_csv(f'transcript_files/{filename}', index = False)     

  #save the title seperately 
  with open(f'transcript_files/{filename}', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Title: ', title])

def main():
  url = input('Enter the Youtube video link: ')
  video_id = get_video_url(url)

  if not video_id:
    print("Invalid Youtube url")
    return

  title = get_video_title(video_id)
  transcript = get_video_transcript(video_id)

  if not transcript:
    print("No transcript available for this video.")
    return

  filename = f"{video_id}_transcript.csv"
  if os.path.exists(f'transcript_files/{filename}'):
    print(f'{filename} already exists in the dir')
    return None
  else:
    save_to_csv(title, transcript, filename)
    print(f'Transcript saved to {filename}')  

if __name__ == '__main__':
  main()