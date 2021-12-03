# 2W_ ECG

import scipy.signal as ssig
import math

class ECG_data:
    
    def __init__(self,name):
        self.name=name
    
    def load_data(self): # 파일 읽기 
        f=open(self.name,'r')
        lines=f.readlines()
        ecg_data,time_data=[],[]
        for i in lines:
            time_data.append(float(i.split(" ")[2]))
            ecg_data.append(float(i.split(" ")[-1]))
        f.close()
        return time_data,ecg_data
    
    def FFT(self, data, fs): # FFT 함수 
        import numpy as np
        length=len(data)
        k=np.arange(length)
        T=length/fs
        freq=k/T
        freq=freq[range(int(length/2))]
        ECG_fft=np.fft.fft(data)
        ECG_fft=abs(ECG_fft[range(int(length/2))])
        return freq,ECG_fft
    
    def low_Freq_response(self,data,fs): # Lowpass_filter + freq_response
        b,a=ssig.butter(10,50,btype='low', fs=fs)
        w,h=ssig.freqz(b,a,fs)
        w_hz=w*fs/(2*math.pi)
        low_ecg=ssig.filtfilt(b,a,data)
        return w_hz, abs(h), low_ecg
            
    def high_Freq_response(self,data,fs): # Highpass_filter + freq_response
        b,a= ssig.butter(6,1,btype='high',fs=fs)
        w,h=ssig.freqz(b,a,fs)
        w_hz=w*fs/(2*math.pi)
        high_ecg=ssig.filtfilt(b,a,data)
        return w_hz, abs(h), high_ecg
    
    def show_result(self): # 그래프로 확인하기 
        import matplotlib.pyplot as plt
        plt.figure(figsize=(13,15))
        time,ecg_data=ECG_data.load_data(self)
        fs=int(1/(time[1]-time[0]))
        plt.subplot(5,2,1); plt.title("original ECG data"); plt.xlabel('time(s)'); plt.plot(time,ecg_data,'black')
        freq,ecg_fft=ECG_data.FFT(self,ecg_data,fs)
        low_w_hz,low_gain,low_ecg=ECG_data.low_Freq_response(self,ecg_data,fs)
        plt.subplot(5,2,2); plt.title("Frequency component"); plt.xlabel('frequency(Hz)'); plt.plot(freq,ecg_fft,'black')
        plt.subplot(5,1,2); plt.title("Frequency Response"); plt.xlabel('frequency(Hz)'); plt.plot(low_w_hz,low_gain,'black')
        plt.subplot(5,2,5); plt.title("Lowpass filtering ECG data"); plt.xlabel('time(s)'); plt.plot(time,low_ecg,'black')
        freq,low_ecg_fft=ECG_data.FFT(self,low_ecg,fs)
        plt.subplot(5,2,6); plt.title("Frequency component"); plt.xlabel('frequency(Hz)'); plt.plot(freq,low_ecg_fft,'black')
        high_w_hz,high_gain,high_ecg=ECG_data.high_Freq_response(self,low_ecg,fs)
        plt.subplot(5,1,4); plt.title("Frequency Response"); plt.xlabel('frequency(Hz)'); plt.plot(high_w_hz,high_gain,'black');plt.xlim([0,3])
        plt.subplot(5,2,9); plt.title("highpass filtering ECG data"); plt.xlabel('time(s)'); plt.plot(time,high_ecg,'black')
        freq,high_ecg_fft=ECG_data.FFT(self,high_ecg,fs)
        plt.subplot(5,2,10); plt.title("Frequency component"); plt.xlabel('frequency(Hz)'); plt.plot(freq,high_ecg_fft,'black')
        plt.tight_layout()
        plt.show()
        
if __name__ == "__main__":
    ECG_data('ECG_data.txt').show_result() # 파일명 입력 