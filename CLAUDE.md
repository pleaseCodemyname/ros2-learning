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
- my_turtle_control 패키지에 Python 노드 직접 작성
  - circle_publisher: 타이머로 /turtle1/cmd_vel에 Twist 발행 (원 그리기)
  - pose_subscriber: /turtle1/pose 구독, 로그 출력
  - wall_avoider: pose 구독 + cmd_vel 발행, theta(cos/sin)로 벽을 향할 때만 회전
  - turtle_tf_broadcaster: pose를 받아 world -> turtleN tf 발행 (turtlename 파라미터)
  - turtle_follower: tf listener로 turtle2 기준 turtle1 위치를 읽어 turtle2를 이동
- launch 파일 2개 작성 (turtle_control_launch.py, turtle_follow_launch.py: name/parameters/ExecuteProcess 사용)
- tf 학습: turtle_tf2_py 데모, tf2_echo, view_frames, broadcaster/listener 직접 구현
- 파라미터(declare_parameter, --ros-args -p), 서비스 호출(ros2 service call /spawn) 사용
- VS Code를 WSL 모드로 연결, ~/.bashrc에 워크스페이스 source 추가
- 개념 다지기 (8개 수업): 노드 → 토픽 → 메시지 → Publisher/Subscriber → 콜백과 spin → 노드 파일의 틀 → 패키지/빌드/launch → tf
  - 설명보다 직접 확인하는 방식으로 진행 (print 넣기, ros2 topic info -v, tf2_echo, 일부러 에러 내 보기)
- Python 기초 짚기 (practice.py): 함수와 인자, 함수를 값으로 넘기기(콜백), 클래스/생성자/self, 상속과 super()
- 빈 파일에서 노드 직접 작성
  - assignment (노드 이름 half_turtle): pose 구독, 거북이가 창의 왼쪽/오른쪽 절반 중 어디에 있는지 로그 출력
  - speed_changer: pose 구독 + cmd_vel 발행, 왼쪽 절반이면 빠르게, 오른쪽 절반이면 천천히 직진

## 개념 정리

### ROS2
- 노드: 한 가지 일을 맡은 프로그램 하나
- 토픽: 이름 붙은 게시판. 노드끼리 직접 연결되지 않고 게시판을 사이에 둔다
  - 요청/응답이 아니라 한쪽 방향이다 (메시지 큐와 같은 구조). 요청/응답은 서비스 (예: /spawn)
- 메시지: 게시판에 올리는 글의 양식 (Twist: 속도 명령, Pose: 위치와 방향)
- Publisher는 올리는 쪽(정보를 원래 가진 쪽), Subscriber는 읽는 쪽
  - 게시판의 성질이 아니라, 그 게시판에 대한 노드의 역할이다
  - 헷갈리면 추리하지 말고 확인: `ros2 topic info <토픽> -v`, 또는 코드의 create_publisher / create_subscription
- 콜백: 구독한 게시판에 새 글이 올 때(타이머는 정한 시간마다) 실행되는 함수
  - 내 코드가 부르지 않고 spin이 부른다. msg도 spin이 넣어 준다
  - 실행 횟수는 올리는 쪽이 정한다 (turtlesim의 pose는 1초에 약 60번)
- spin: 글을 기다리다가 콜백을 불러 주는 것. 글이 안 오면 에러 없이 조용히 기다린다
- 노드 파일의 틀: import / class(Node 상속) / __init__(한 번: Publisher, Subscriber 생성) / 콜백(매번) / main(init → 노드 생성 → spin → 정리)
- 패키지와 빌드: 고치는 곳은 src, 실행되는 곳은 install. 고치면 colcon build
  - 새 노드는 setup.py의 console_scripts에 `'이름 = 패키지.파일:main'` 등록
  - source는 패키지를 새로 만들었을 때만 다시 필요
- launch: ros2 run 여러 개를 한 번에 실행
- tf: frame은 "누구 기준으로 재는가". /tf 토픽에 "world 기준으로 나는 여기"를 올리면(broadcaster) 다른 조합은 계산해 준다(listener, lookup_transform)
  - pose의 x, y는 창 기준(가로, 세로). 거북이 기준 tf의 x, y는 앞쪽, 왼쪽

### Python
- def는 만들기, 이름()은 실행. 괄호 없이 쓰면 함수 그 자체 (콜백을 넘길 때)
- 부른 쪽 괄호 안의 값이 받는 쪽 이름에 담긴다. 이름이 아니라 값이 넘어간다
- class는 설계도, 클래스()는 하나 만들기 (이때 __init__이 한 번 실행됨)
- self는 만들어진 그것 자신. self.x에 넣은 것은 함수가 끝나도 남아서 다른 메서드에서 쓸 수 있다
  - 함수 안에서만 쓰고 버릴 값(cmd, msg 등)에는 self를 붙이지 않는다
- 상속: class X(Node)로 기능을 물려받고, super().__init__('이름')으로 부모의 준비를 실행한다

### 에러 읽는 법
- 맨 마지막 줄(무엇이 문제인지)과, 아래에서부터 처음 만나는 내 파일의 줄 번호(어디서 났는지)만 본다
- `missing ... argument` / `takes N ... but M were given`: 괄호 안에 넘긴 값의 개수가 안 맞음
- `has no attribute`: self.에 넣어 둔 적이 없거나, 함수 뒤에 괄호가 빠짐
- 고쳤는데 그대로면 빌드했는지부터 확인

## 다음 목표
- OpenCV 연동, URDF+RViz, Gazebo 시뮬레이션까지 단계적으로 진행 예정
- 최종적으로 "자연어 명령 → 로봇 동작" 같은 LLM 연동 미니 프로젝트까지 만들어서 포트폴리오로 쓸 계획 (Physical AI 분야 취업 목표)

## 참고 사항
- 배경: STT/LLM 파이프라인(GPT-4o 연동 등) 실무 경험 있음 (AnesNote 프로젝트)
- 이 경험을 ROS2+AI 결합 프로젝트에 활용하고 싶어함
