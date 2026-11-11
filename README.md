# ROS2 Learning

ROS2 (Jazzy) 학습 및 실습 기록입니다.

## 프로젝트: [color_seeker](src/color_seeker/README.md)

**말로 시키면 그 색 물체를 찾아가는 로봇** (ROS 2 Jazzy + Gazebo Harmonic + 로컬 LLM)

"빨간색으로 갔다가 파란색으로 가" → 로컬 LLM(Ollama)이 `["red", "blue"]`로 해석 → 액션 goal → 카메라로 색을 찾아 차례로 이동. 정지 명령 우선 처리, goal 취소/교체, 명령 해석 평가 24문장 92%.

→ [자세히 보기](src/color_seeker/README.md)

## 환경
- Ubuntu 24.04 (WSL2)
- ROS2 Jazzy

## 진행 내용
- turtlesim을 활용한 Node/Topic 개념 실습
- 커스텀 launch 파일 작성 (`my_first_launch`)
- turtlesim_node와 turtle_teleop_key를 동시 실행
- Python으로 Publisher/Subscriber 노드 직접 작성 (my_turtle_control)
- pose를 구독해 벽을 피하는 제어 노드 (wall_avoider)
- 직접 만든 노드를 launch 파일로 묶어 실행
