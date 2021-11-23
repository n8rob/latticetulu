To run subtitles_extractor.py: 

- Create mp3 file using movie name and place in tulu_movie_audo directory. 
  (https://yt5s.com/en15/youtube-to-mp3)
- Create mp4 file using movie name and place in tulu_movie_video directory. 
  (https://yt5s.com/en15/youtube-to-mp4)
- Replace variable movie_name on line 7 of subtitles_extractor.py with the same 
  movie name chosen for the mp3 and mp4 files. 
- Make sure Python is updated to at least version 3.8 

- Run the following commands from tulu_dataset_creation directory: 
$ pip3 install tesseract 
$ python3 subtitles_extractor.py
 