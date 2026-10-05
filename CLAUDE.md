저는 ROS2를 새로 배우고 있는 백엔드/풀스택 개발자입니다. 아래 맥락 참고해서 도와주세요.

## 환경
- Windows PC (RTX5060Ti 16GB, i5-14400F, RAM 32GB)
- WSL2 + Ubuntu 24.04 설치 완료
- ROS2 Jazzy 설치 완료 (Isaac Sim 호환을 위해 Humble 대신 Jazzy 선택)
- 작업 폴더: ~/ros2_ws
- VS Code + WSL 연동 완료
- GitHub 저장소 연동 완료 (https://github.com/pleaseCodemyname/ros2-learning)

## 지금까지 한 것
- turtlesim으로 Node/Topic/Publisher-Subscriber 개념 실습
- rqt_graph로 노드 통신 구조 시각화
- 커스텀 launch 파일 작성 (my_first_launch 패키지, turtlesim_node + teleop 동시 실행)
- colcon build, roslaunch 실행까지 전체 워크플로우 경험
- wikidocs 책(ROS2 로봇 만들기, https://wikidocs.net/265253)을 참고 자료로 사용 중 (단, 책은 Humble 기준이라 명령어의 'humble'을 'jazzy'로 바꿔서 적용해야 함)

## 다음 목표
- tf(좌표계) 개념 학습
- 직접 Python으로 간단한 Publisher/Subscriber 노드 작성
- 이후 OpenCV 연동, URDF+RViz, Gazebo 시뮬레이션까지 단계적으로 진행 예정
- 최종적으로 "자연어 명령 → 로봇 동작" 같은 LLM 연동 미니 프로젝트까지 만들어서 포트폴리오로 쓸 계획 (Physical AI 분야 취업 목표)

## 참고 사항
- 배경: STT/LLM 파이프라인(GPT-4o 연동 등) 실무 경험 있음 (AnesNote 프로젝트)
- 이 경험을 ROS2+AI 결합 프로젝트에 활용하고 싶어함
