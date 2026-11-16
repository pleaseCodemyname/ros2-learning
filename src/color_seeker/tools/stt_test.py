from faster_whisper import WhisperModel 
import time
import subprocess
import signal

model = WhisperModel("large-v3-turbo", device="cuda", compute_type="int8_float16") # 모델 만들기(한 번)
input("Enter를 누르고 말하세요")
proc = subprocess.Popen(["parecord", "--channels=1", "--rate=16000", "/tmp/cmd.wav"]) # 녹음 시작: parecord를 프로그램으로 켜기 (/tmp/cmd.wav로 저장)
input("다 말했으면 Enter")
proc.send_signal(signal.SIGINT) # 녹음 끝: parecord에 Ctrl + C 신호 보내기 -> 끝날 때까지 기다리기
proc.wait() # parecord가 파일을 다 쓰고 꺼질 때까지 기다림. 이게 없으면 파일이 덜 써진 상태로 transcribe할 수 있음
for _ in range(2):
    start = time.time()
    segments, info = model.transcribe("/tmp/cmd.wav", language="ko")    
    for i in segments:
        print(i.text)
    print(time.time() - start)
