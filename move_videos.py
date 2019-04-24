import argparse
import os
import os.path as osp
import sys

from shutil import copyfile

def move_videos_up(root_dir):
    subdir_paths = [osp.normpath(osp.join(root_dir, d)) for d in os.listdir(root_dir)]
    subdir_paths = [s for s in subdir_paths if osp.isdir(s)]
    subdir_names = [osp.basename(s) for s in subdir_paths]
    for subdir_name, subdir_path in zip(subdir_names, subdir_paths):
        frame_dirs = [osp.join(subdir_path, f) for f in os.listdir(subdir_path) if f[:6] == 'frames']
        frame_dirs = [f for f in frame_dirs if osp.isdir(f)]
        frame_dir_names = [osp.basename(f) for f in frame_dirs]
        for frame_dir_name, frame_dir_path in zip(frame_dir_names, frame_dirs):
            video = [v for v in os.listdir(frame_dir_path) if v[-4:] == '.mp4']
            # if not len(video) == 1:
            #     print frame_dir_path
            assert len(video) <= 1
            if len(video) == 1:
                video = video[0]
                video_path = osp.join(frame_dir_path, video)
                new_video_name = '{0}_{1}'.format(subdir_name, video)
                new_video_path = osp.join(subdir_path, new_video_name)
                print 'moving video at {0} to {1}'.format(video_path, new_video_path)
                copyfile(video_path, new_video_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    # Settings of this interaction
    parser.add_argument('root_dir')
    args = parser.parse_args(sys.argv[1:])
    move_videos_up(args.root_dir)