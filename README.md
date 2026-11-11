# ROS2 Learning

ROS2 (Jazzy) 학습 및 실습 기록입니다.

## 프로젝트: [color_seeker](src/color_seeker/README.md)

**말로 시키면 그 색 물체를 찾아가는 로봇** (ROS 2 Jazzy + Gazebo Harmonic + 로컬 LLM)

"빨간색으로 갔다가 파란색으로 가" → 로컬 LLM(Ollama)이 `["red", "blue"]`로 해석 → 액션 goal → 카메라로 색을 찾아 차례로 이동. 정지 명령 우선 처리, goal 취소/교체, 명령 해석 평가 24문장 92%.

→ [자세히 보기](src/color_seeker/README.md)

## 환경
- Windows + WSL2 (Ubuntu 24.04), RTX 5060 Ti 16GB
- ROS 2 Jazzy, Gazebo Harmonic (gz sim 8)
- Python, OpenCV, Ollama (llama3.1:8b)

## 학습 과정

빈 파일에서 직접 타이핑하고, 실행 전에 결과를 먼저 예상한 뒤 `ros2 topic info -v`, `tf2_echo`, 로그로 확인하는 방식으로 진행했습니다.

| 단계 | 내용 | 위치 |
|---|---|---|
| 1. 기본 통신 | turtlesim으로 노드·토픽·Publisher/Subscriber, rqt_graph, launch | `src/my_first_launch`, `src/my_turtle_control` |
| 2. 노드 직접 작성 | 원 그리기, pose 구독, 벽 피하기, tf broadcaster/listener로 거북이 따라가기 | `src/my_turtle_control` |
| 3. 기초 문제 | 빈 노드 → talker/listener → 구독+발행 한 노드 → 조건 판단 → 영상 cx로 거북이 조종 | `drills/d01~d10` |
| 4. OpenCV | numpy 배열로서의 사진, BGR, 흑백, `inRange` 마스크, `nonzero`와 cx | `drills/c01~c07`, `src/my_vision` |
| 5. 서비스·액션 | `/spawn` 서비스 client, `rotate_absolute` 액션 client(feedback, 취소) | `drills/s02, s04`, `basics/b06~b08` |
| 6. URDF + RViz | link/joint, origin, fixed/continuous/revolute, `/joint_states`를 직접 발행해 걷기·바퀴 돌리기 | `urdf_practice/u01~u07` |
| 7. 패키지·파라미터·launch | `ros2 pkg create`, setup.py 등록, `declare_parameter`, 노드 여러 개를 launch로 | `src/step_pkg`, `src/step2_pkg` |
| 8. tf | static transform, `tf2_echo`로 좌표 변환 예상 → 확인, RPY, URDF joint = tf | `src/my_turtle_control` (turtle_tf_broadcaster, turtle_follower) |
| 9. Gazebo | inertial/collision, 캐스터, diff-drive 플러그인, ros_gz_bridge, 카메라 센서, 빨간 상자 따라가기(카메라 피드백 고리) | `gazebo_practice/g02~g04` |
| 10. 재현 | 완성한 것을 빈 화면에서 다시 만들기(talker/listener, 패키지+launch, URDF 부품, follow 노드) | `review/`, `src/review_pkg` |
| 11. 프로젝트 | 위 내용을 묶어 자연어 명령 → LLM → 액션 → 카메라 주행 | `src/color_seeker` |
