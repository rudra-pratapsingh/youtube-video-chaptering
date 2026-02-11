# YouTube Transcript Analyzer

A Python-based tool that extracts YouTube video transcripts and performs advanced text analysis including topic modeling and automatic chapter generation.

## Features

- **Transcript Extraction**: Download transcripts from YouTube videos (supports Hindi language)
- **Automated Chapter Detection**: Automatically identifies logical chapter breaks using topic modeling
- **Text Analytics**: 
  - Word frequency analysis
  - Text length distribution
  - TF-IDF based topic extraction
- **Topic Modeling**: Uses Non-negative Matrix Factorization (NMF) for identifying distinct topics
- **Smart Chapter Naming**: Generates descriptive chapter names based on key phrases

## Prerequisites

- Python 3.7+
- YouTube Data API key
- Required Python packages (see Installation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-transcript-analyzer.git
cd youtube-transcript-analyzer
```

2. Install required packages:
```bash
pip install pandas numpy matplotlib scikit-learn google-api-python-client youtube-transcript-api python-dotenv
```

3. Set up your environment:
   - Create a `.env` file in the project root
   - Add your YouTube Data API key:
```
API_KEY=your_youtube_api_key_here
```

4. Create a `transcript_files` directory:
```bash
mkdir transcript_files
```

## Usage

### 1. Extract Video Transcript

Run the main application to download a transcript:

```bash
python app.py
```

When prompted, enter a YouTube video URL. The script will:
- Extract the video ID
- Fetch the video title
- Download the transcript (Hindi language)
- Save it as a CSV file in `transcript_files/`

### 2. Analyze Transcript

After downloading a transcript, analyze it using:

```bash
python dataset.py
```

This will generate:
- Statistical overview of the transcript
- Text length distribution histogram
- Top 20 most common words bar chart
- Identified topics using NMF
- Automatically generated chapter points with descriptive names

## Project Structure

```
youtube-transcript-analyzer/
│
├── app.py                    # Main transcript extraction script
├── dataset.py               # Transcript analysis and chapter generation
├── .env                     # Environment variables (API keys)
├── transcript_files/        # Directory for saved transcripts
│   └── {video_id}_transcript.csv
└── README.md               # Project documentation
```

## How It Works

### Transcript Extraction (`app.py`)

1. **URL Parsing**: Extracts video ID from YouTube URL
2. **Metadata Retrieval**: Fetches video title using YouTube Data API
3. **Transcript Download**: Downloads transcript using `youtube-transcript-api`
4. **CSV Storage**: Saves transcript with timestamps to CSV file

### Analysis & Chapter Detection (`dataset.py`)

1. **Data Loading**: Reads transcript CSV file
2. **Text Preprocessing**: Analyzes text lengths and word frequencies
3. **Topic Modeling**: 
   - Uses Count Vectorizer for text representation
   - Applies NMF (Non-negative Matrix Factorization) to identify 10 topics
   - Assigns dominant topic to each transcript segment
4. **Chapter Detection**:
   - Identifies topic transitions as potential chapter breaks
   - Consolidates breaks using 60-second threshold
   - Merges consecutive segments with same topic
5. **Chapter Naming**: Uses TF-IDF to extract key phrases for descriptive names

## Configuration

### Topic Modeling Parameters

In `dataset.py`, you can adjust:

- `n_topics`: Number of topics to identify (default: 10)
- `threshold`: Minimum seconds between chapters (default: 60)
- `max_df`, `min_df`: Document frequency thresholds for vectorization

### Language Support

Currently supports Hindi transcripts. To change language, modify:

```python
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
```

Replace `'hi'` with desired language code (e.g., `'en'` for English).

## Output Examples

### Transcript CSV Format
```csv
start,text
0.0,"नमस्ते दोस्तों"
2.5,"आज हम बात करेंगे"
...
```

### Chapter Output
```
00:00:00 - Chapter 1: introduction topic overview
00:02:30 - Chapter 2: main concept explanation
00:05:15 - Chapter 3: examples demonstration
...
```

## Limitations

- Only works with videos that have transcripts available
- Requires YouTube Data API quota
- Chapter detection accuracy depends on topic coherence
- Currently optimized for Hindi language transcripts

## Error Handling

The application handles:
- Invalid YouTube URLs
- Disabled transcripts
- Duplicate file prevention
- Missing API credentials

## Future Enhancements

- [ ] Multi-language support
- [ ] GUI interface
- [ ] Export chapters to video editing software formats
- [ ] Sentiment analysis of transcript segments
- [ ] Summary generation for each chapter
- [ ] Support for playlist processing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Your Name - Rudra Pratap Singh (https://github.com/rudra-pratapsingh)

## Support

For issues or questions, please open an issue on GitHub.