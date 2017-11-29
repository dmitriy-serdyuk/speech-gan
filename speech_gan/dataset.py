from os.path import join, isdir, isfile
from os import listdir
from scipy.io.wavfile import read


class VCTK(object):
    def __init__(self, path):
        self.path = path
        self.files = []
        txt_path = join(path, 'txt')
        wav_path = join(path, 'wav48')
        dirs = [f for f in listdir(txt_path) if isdir(join(txt_path, f))]
        for dir in dirs:
            self.files.extend((join(txt_path, dir, f), join(wav_path, dir, f[:-4] + '.wav'))
                              for f in listdir(join(txt_path, dir)) if isfile(join(txt_path, dir, f)))

    def __getitem__(self, item):
        return self.files[item]

    def __len__(self):
        return len(self.files)


class FramewiseVCTK(object):
    def __init__(self, dataset, window_size, hop_size):
        self.total_length = 0
        for text, wav in dataset:
            sample_rate, data = read(wav)
            window_size_frames = sample_rate // 1000 * window_size
            hop_size_frames = sample_rate // 1000 * hop_size
            self.total_length += (data.shape[0] - window_size_frames) // hop_size_frames

    def __getitem__(self, item):
        pass

    def __len__(self):
        return self.total_length
