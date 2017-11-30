import numpy
from bisect import bisect
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
    def __init__(self, dataset, window_size=40, hop_size=5, window_type='hanning'):
        self.vctk_dataset = dataset
        self.window_size = window_size
        self.hop_size = hop_size
        self.window_type = window_type

        self.total_length = 0
        # Cumulative index
        self.cumsize = []
        for text, wav in dataset:
            sample_rate, data = read(wav)
            window_size_frames = sample_rate // 1000 * window_size
            hop_size_frames = sample_rate // 1000 * hop_size
            length = (data.shape[0] - window_size_frames) // hop_size_frames
            self.total_length += length
            self.cumsize.append(self.total_length)

    def __getitem__(self, item):
        vctk_ind = bisect(self.cumsize, item)
        txt, wav = self.vctk_dataset[vctk_ind]
        sample_rate, data = read(wav)
        window_size_frames = sample_rate // 1000 * self.window_size
        hop_size_frames = sample_rate // 1000 * self.hop_size
        data_ind = item - self.cumsize[vctk_ind]
        output = data[data_ind * hop_size_frames: data_ind * hop_size_frames + window_size_frames]
        if self.window_type == 'hanning':
            return output * numpy.hanning(output.shape[0])
        elif self.window_type == 'none':
            return output
        else:
            raise ValueError

    def __len__(self):
        return self.total_length
