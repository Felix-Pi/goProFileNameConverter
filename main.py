import argparse
import os.path
import shutil
import datetime

extensions = ['MP4', 'JPG', 'LRV']


def validate_path(path):
    """
    adds / to path if missing
    :param path:
    :return: path with /
    """
    path = str(path)

    if path[-1] != '/':
        path = path + '/'
    return path


def rename(path, file):
    """
    renames file to files creation_time.extension
    :param path: path to file
    :param file: filename
    :return: renamed filename
    """
    extension = file.split('.')[1]

    # read creation time and convert to datetime
    creation_time = os.path.getmtime(path + file)
    creation_time = datetime.datetime.fromtimestamp(creation_time)

    # format datetime
    # creation_time = creation_time.strftime("%Y-%m-%d_%H-%M-%S")
    creation_time = creation_time.strftime("%Y_%m_%d-%H_%M_%S")

    new_file = str(creation_time) + '.' + extension
    os.rename(path + file, path + new_file)

    return new_file


def read_dir(path):
    """
    reads files from dir
    :param path: path to directory
    :return: supported files and lrv files
    """
    print('readdir', path)
    entries = os.listdir(path)

    content_holder = []
    lrv_holder = []

    for entry in entries:
        tmp = entry.split('.')
        if len(tmp) == 2:
            extension = tmp[1]

            if extension in extensions:
                if extension == 'LRV':
                    lrv_holder.append(rename(path, entry))
                else:
                    content_holder.append(rename(path, entry))

    return content_holder, lrv_holder


def move_lrv_files(path, path_lrv, lrv_holder):
    """
    creates new directory and moves .lrv files to new directory
    :param path: path to lrv files
    :param path_lrv: path to new directory
    :param lrv_holder: array of lrv files that should be moved
    """
    if len(lrv_holder) > 0:
        os.mkdir(path + path_lrv)

        for entry in lrv_holder:
            shutil.move(path + entry, path + path_lrv + entry)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename gopro files to creation date')
    parser.add_argument('-p', '--path', default='/Users/felixpieschka/Pictures/GoPro/')
    parser.add_argument('-f', '--folder', required=True)
    parser.add_argument('-model', '--gopromodel', default='HERO9 BLACK 1')
    parser.add_argument('-lrv', '--lrvpath', default='_LRV/')
    args = parser.parse_args()

    # validate path
    path = validate_path(args.path) + validate_path(args.folder) + validate_path(args.gopromodel)
    if not os.path.exists(path):
        print(' \'{}\' does not exist'.format(str(path)))
        exit()
    lrvpath = validate_path(args.lrvpath)

    # read dir and rename files
    mp4, lrv = read_dir(path)

    # move lrv files to lrv dir
    move_lrv_files(path, lrvpath, lrv)

    print('Renamed {} mp4 and {} lrv files \nMoved {} lrv files to \'{}\''.format(len(mp4), len(lrv), len(lrv),
                                                                                  args.lrvpath))
