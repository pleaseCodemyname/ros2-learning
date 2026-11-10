# 명령 해석 정확도 측정 (Gazebo/로봇 없이, Ollama만 켜져 있으면 됨)
# 실행: cd ~/ros2_ws && python3 src/color_seeker/tools/eval_commands.py
# 프롬프트나 STOP_WORDS를 고칠 때마다 다시 돌려서 정확도가 떨어지지 않았는지 확인한다
# 주의: 프롬프트의 예시 문장을 여기 넣지 않는다(외운 것인지 이해한 것인지 구분이 안 됨)

import os
import sys
import time

# src/color_seeker를 import 경로에 넣어서 color_seeker.commander의 interpret를 그대로 쓴다(로봇이 쓰는 것과 같은 함수)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from color_seeker.commander import interpret

# (문장, 기대하는 답)
CASES = [
    # 색 이름 그대로
    ("빨간색 상자로 가", "red"),
    ("파란 상자 찾아 줘", "blue"),
    ("초록색으로 가", "green"),
    # 색을 다른 말로
    ("바다색 상자로 가", "blue"),
    ("풀색 박스", "green"),
    ("빨개 보이는 거", "red"),
    ("딸기 색 상자", "red"),
    ("잔디 같은 색으로 가", "green"),
    # 부정(가지 말라는 색 무시)
    ("초록색으로 가지 말고 빨간색 상자로 가 줘", "red"),
    ("빨간 거 말고 파란 거", "blue"),
    ("파랑은 아니고 초록", "green"),
    # 정지
    ("이제 그만해", "stop"),
    ("잠깐 멈춰봐", "stop"),
    ("잠깐 서 봐", "stop"),
    ("거기서 정지", "stop"),
    ("일단 기다려", "stop"),
    # 없는 색 / 색이 아닌 말
    ("노란 상자로 가", "unknown"),
    ("보라색 찾아", "unknown"),
    ("안녕", "unknown"),
    ("오늘 날씨 어때", "unknown"),
]


def main():
    correct = 0
    times = []
    print(f"{'결과':<4} {'기대':<8} {'답':<8} {'시간':>6}  문장")
    for sentence, expected in CASES:
        start = time.time()
        answer = interpret(sentence)
        elapsed = time.time() - start
        times.append(elapsed)
        ok = answer == expected
        correct += ok
        print(f"{'O' if ok else 'X':<4} {expected:<8} {str(answer):<8} {elapsed:>5.2f}s  {sentence}")
    print(f"\n정확도: {correct}/{len(CASES)} ({correct / len(CASES) * 100:.0f}%)")
    print(f"평균 시간: {sum(times) / len(times):.2f}s (정지 단어는 LLM을 안 거쳐 0초)")


if __name__ == "__main__":
    main()
