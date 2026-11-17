from transformers import pipeline
from PIL import Image # 사진 여는 라이브러리(OpenCV말고 모델이 이걸 받음)
import time

detector = pipeline("zero-shot-object-detection",
                     model="google/owlv2-base-patch16-ensemble", device=0) # device=0: 0번 GPU를 쓰라는 뜻(STT의 device="cuda"와 같음)

image = Image.open("/tmp/frame.png")
for _ in range(5):
    start = time.time()
    results = detector(image, candidate_labels=["red box", "blue box"], threshold=0.01) # candidate_labels: 찾을 물체를 글로 주는 자리. 여기가 나중에 LLM 답("red cup")이 들어갈 곳
    # for i in results:
        # print(i)
    print(time.time() - start)