from scipy import fft
from scipy.io import wavfile
import numpy as np

sample_rate, test = wavfile.read("/Users/he/work/bigdata/media/机器学习与数据挖掘/02-回归算法/资料/genres/blues/converted/blues.00000.au.wav")
print(sample_rate, test)
testdata_fft_features = abs(fft(test))[:1000]
sad = '/Users/he/work/bigdata/media/机器学习与数据挖掘/02-回归算法/资料/genres/blues/blues.00000.fft'
np.savetxt(sad, testdata_fft_features, fmt='%10.5f')
