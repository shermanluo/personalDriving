import argparse
import os
import pdb
import sys

import cv2

import constants

def make_video_recursive(directory, new_video=False):
    if directory[-1] != '/':
        directory += '/'
    files = [directory + f for f in os.listdir(directory)]
    interaction_data_dirs = [f for f in files if os.path.isdir(f)]
    all_frame_dirs = []
    for interaction_data_dir in interaction_data_dirs:
        interaction_files = [interaction_data_dir + '/' + f for f in os.listdir(interaction_data_dir)]
        frame_dirs = [f for f in interaction_files if os.path.isdir(f)]
        for frame_dir in frame_dirs:
            frame_dir_videos = [f for f in os.listdir(frame_dir) if f[-4:] == '.mp4']
            if new_video or len(frame_dir_videos) == 0:
                all_frame_dirs.append(frame_dir)
    print('Frame directories:', all_frame_dirs, len(all_frame_dirs))
    for frame_dir in all_frame_dirs:
        make_video(frame_dir)

def make_video(frame_dir, video_name=None):
    if frame_dir[-1] != '/':
        frame_dir += '/'
    frames = sorted([frame for frame in os.listdir(frame_dir) if frame.endswith(".png")],
        key=lambda f: int(f.split('.png')[0]))
    frame = cv2.imread(os.path.join(frame_dir, frames[-1]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    if video_name is None:
        video_name = frame_dir.split('/')[-2] + '.mp4'
    print('video:', frame_dir + video_name)
    out = cv2.VideoWriter(frame_dir + video_name, fourcc, 10.0, (width, height))
    for frame in frames:
        out.write(cv2.imread(os.path.join(frame_dir, frame)))
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', 
        help="The frame directory if not using the recursive option. Otherwise, the directory of frame direcories.")
    parser.add_argument('-v', '--video_name', help="The name of the video.")
    parser.add_argument('-r', '--recursive', action='store_true', 
        help="If True, make videos for all of the directories inside of the given directory.")
    parser.add_argument('-n', '--new_video', action='store_true', 
        help="If True, make a new video to overwrite the existing one. Otherwise, don't create a new video if one already exists.")
    args = parser.parse_args(sys.argv[1:])
    if args.recursive:
        make_video_recursive(args.directory, args.new_video)
    else:
        make_video(args.directory, args.video_name)