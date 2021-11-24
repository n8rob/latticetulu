import os

os.chdir(os.getcwd())

import videocr 

movie_name = "uppadu"

def main():
  videocr.api.save_subtitles_to_file(
    video_path= "tulu_movie_video/" + movie_name +".mp4", 
    file_path="movie_subtitles/" + movie_name + "_subtitle.srt", 
    lang='eng', 
    time_start='0:00', 
    time_end='', 
    conf_threshold=65, 
    sim_threshold=90, 
    use_fullframe=False
  )
  print("Saved subtitles for:", movie_name)
  
  
if __name__=="__main__":
    main()