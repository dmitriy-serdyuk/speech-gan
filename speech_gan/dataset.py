from os.path import join, isdir, isfile
from os import listdir


class VCTK(object):
    def __init__(self, path):
        self.path = path
        self.files = []
        txt_path = join(path, 'txt')
        wav_path = join(path, 'wav48')
        dirs = [f for f in listdir(txt_path) if isdir(join(txt_path, f))]
        for dir in dirs:
            self.files.extend((join(txt_path, dir, f), join(wav_path, dir, f))
                              for f in listdir(dir) if isfile(join(dir, f)))

    def __getitem__(self, item):
        return self.files[item]

    def __len__(self):
        return len(self.files)
