from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from big_block_create import Video, Loop
import datetime

db_params = {
    'user': '',
    'password': '',  # enter your DB password
    'host': 'localhost',  # 'localhost' or IP address
    'port': '5432',  # '5432'
    'database': 'test', #tensionTerminator
}

import os
import glob
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from big_block_create import Base, db_params, Users, Loop, Video  # Import necessary classes

def add_loop_and_videos_from_directory(timestamp, location, session_length, human_labeled, user_id, 
                                       video_directory, device, tool=None, bodyside=None):
    """
    Create and add a new loop and videos from a directory to the database.

    :param timestamp: Timestamp for the loop.
    :param location: Location of the loop.
    :param session_length: Duration of the loop.
    :param human_labeled: Boolean indicating if the loop is human-labeled.
    :param user_id: ID of the associated user.
    :param video_directory: Directory containing video files.
    :param device: Device used for the videos.
    :param tool: (Optional) Tool used in the loop.
    :param bodyside: (Optional) Bodyside information for the loop.
    """
    # Validate the directory
    if not os.path.isdir(video_directory):
        raise ValueError(f"The provided path '{video_directory}' is not a valid directory.")

    # Find video files in the directory
    video_files = glob.glob(os.path.join(video_directory, '*.mp4'))
    if not video_files:
        raise ValueError("No MP4 video files found in the provided directory.")

    # Database connection
    engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@"
                           f"{db_params['host']}:{db_params['port']}/{db_params['database']}")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Creating and adding Loop
    new_loop = Loop(timestamp=timestamp, location=location, session_length=session_length, 
                    human_labeled=human_labeled, user_id=user_id)
    session.add(new_loop)
    session.commit()

    loop_id = new_loop.id  # Capture the ID of the newly created loop

    if tool:
        new_loop.tools.append(tool)
        session.commit()

    if bodyside:
        new_loop.bodysides.append(bodyside)
        session.commit()

    # Creating and adding Videos
    for file_path in video_files:
        new_video = Video(file_path=file_path, device=device, loop_id=loop_id)
        session.add(new_video)
    session.commit()

    session.close()
    print(f"Loop and videos from {video_directory} added to the database.")

if __name__ == "__main__":
    # Example usage
    add_loop_and_videos_from_directory(timestamp=datetime.now(), location="Test Location", session_length=60, 
                                       human_labeled=True, user_id=1, video_directory="path/to/video_directory", 
                                       device="leftCam")
