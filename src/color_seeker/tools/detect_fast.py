import time
import torch
from PIL import Image
from transformers import Owlv2Processor, Owlv2ForObjectDetection # Owlv2Processor: 사진과 글을 숫자로 바꾸고, 결과 숫자를 사각형으로 되돌림. | Owlv2ForObjectDetection: 모델 자체

name = "google/owlv2-base-patch16-ensemble"
processor = Owlv2Processor.from_pretrained(name)
model = Owlv2ForObjectDetection.from_pretrained(name).to("cuda") # .to("cuda"): 모델 숫자를 GPU 메모리로 옮김. pipeline의 devcie=0이 해주던 일

image = Image.open("/tmp/frame.png")
labels = [["red box", "blue box"]] # 대괄호가 두겹. 사진 여러 장을 한 번에 넣을 수 있게 만든 함수라, "사진 1장에 대한 글 목록"을 바깥 목록에 한 번 더 사용.
for _ in range(5):
    start = time.perf_counter()
    inputs = processor(text=labels, images=image, return_tensors="pt").to("cuda") # return_tensors="pt": 결과를 PyTorch 텐서(GPU에 올릴 수 있는 숫자표)로 달라는 뜻 | 입력에도 .to("cuda"): 모델이 GPU에 있으니 입력 숫자도 GPU로 옮겨야함. 둘 중 하나라도 빠지면 "다른 장치에 있다"는 에러가 남.
    with torch.no_grad(): # 학습할 때만 필요한 계산(기울기)을 끄는 블록. 여기서는 쓰기만 하니까 꺼서 빠르게 함.
        outputs = model(**inputs) # model(**inputs): inputs는 딕셔너리(pixel_values, input_ids 등). **는 딕셔너리의 칸을 이름=값 인자로 풀어서 넘김
    results = processor.post_process_grounded_object_detection(
        outputs, threshold=0.05, target_sizes=[(240, 320)], text_labels=labels)[0] # target_sizes=[(240, 320)]: 원래 사진 크기를(세로, 가로) 순서로 줌. frame.shape와 같은 순서. 이걸 줘야 box가 320x240칸 번호로 나옴. 끝의 [0]은 사진 1장의 결과만 꺼내는 것
    print(time.perf_counter() - start)
    # print(results)

target = "blue box"
best = None # (가장 좋은 점수의 box)
best_score = 0

for score, label, box in zip(results["scores"], results["text_labels"], results["boxes"]): # zip(a, b, c): 목록 3개를 같은 순번끼리 하나로 묶어서 꺼내줌. for name, (lower, upper) in self.color_ranges.items(): 처럼 한 번에 여러 이름으로 받음
    if label != target:
        continue # 건너뛰기(이번 차례 끝, 다시 for문으로 감)
    score = score.item()
    if score > best_score: # 점수 비교: score는 텐서라 score.item()으로 숫자로 바꿔서 비교하고 저장
        best_score = score
        best = box
if best is None:
    print("못찾음")
else:
    xmin, ymin, xmax, ymax = best.tolist()
    cx = (xmin + xmax) / 2
    print(target, best_score, cx)