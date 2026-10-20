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
- my_vision 패키지 (OpenCV 연동, 영상은 `ros2 run image_tools cam2image --ros-args -p burger_mode:=true`로 /image에 발행)
  - image_info: /image 구독, 영상 크기와 인코딩 출력
  - image_viewer: cv_bridge로 OpenCV 이미지로 바꿔 창에 표시 (topic 파라미터로 볼 토픽 선택, 기본값 image)
  - gray_converter: /image 구독 → cv2.cvtColor로 흑백 변환 → /image_gray 발행
- 기초 다지기 문제 (drills/ 폴더, 빌드 없이 `python3 drills/파일.py`로 실행)
  - d01 빈 노드, d02 talker(타이머 + String Publisher), d03 listener(String Subscriber), d04 counter(self.count로 0, 1, 2... Int32 발행)
  - d05 judge(/number 구독, 짝수/홀수 판단), d06 doubler(/number 구독 → ×2 → /doubled 발행, Sub+Pub 한 노드)
  - d07 stopper(설계 문제: 토픽/양식을 ros2 topic list/info, ros2 interface show로 직접 찾음. x > 9면 멈춤), d08 arrive(self.logged_count 수첩으로 "도착" 로그를 딱 한 번)
  - d09 find_center(ROS 없이 마스크의 흰 칸 → cx, cy), d10 follow(/image Sub + /turtle1/cmd_vel Pub, 흰 덩어리 cx로 왼쪽 회전/직진/오른쪽 회전 세 구역)
    - d10의 콜백은 앞쪽 CV 세계(사진 → cx)와 뒤쪽 거북이 세계(cx → 명령, d07과 같은 틀)가 숫자 cx 하나로만 이어진다
    - cam2image는 1초에 약 30장 → 콜백도 30번, 매번 새 사진만 보고 새로 판단
    - cam2image 영상은 거북이와 상관없어서 거북이가 돌아도 cx가 안 바뀐다. 진짜 로봇은 카메라가 몸에 붙어 있어 내 움직임이 다시 입력을 바꾼다(피드백 고리) → Gazebo에서 다룰 예정
  - OpenCV가 바닥부터 비어 있다고 느껴 OpenCV 기초 사다리(c01~)로 다시 시작. 파일마다 "예상 먼저 적기 → 실행 → 확인"
    - c01 숫자 표/shape, c02 범위 칠하기, c03 BGR, c04 흑백, c05 마스크, c06 nonzero/cx 완료
    - c07 진짜 햄버거 사진 한 장(d10에 imwrite 한 줄로 drills/burger.png 저장): imread → shape → 점 재기 → 흰색 마스크 → cx → cx 자리에 빨간 세로선. 햄버거가 여러 개면 cx가 무리 사이 빈 곳을 가리킨다는 걸 발견
    - d10에 cx 선 그리기: 실시간 영상에서도 선이 햄버거 사이 빈 곳, cx가 가운데라 거북이는 직진해서 벽에 붙음. 코드가 아니라 구조의 한계(평균 → 가장 큰 덩어리 고르기로, 피드백 없음 → Gazebo로 해결)
    - d10의 한 줄 설명: 카메라로 흰색 물체를 찾고, 화면 어디 있는지(cx) 계산해서, 위치에 따라 거북이를 돌리거나 직진시킨다. 보기 → 판단 → 움직이기가 Physical AI의 기본 뼈대이고, 나중의 LLM 프로젝트("빨간 컵으로 가")에서 LLM과 로봇을 잇는 부분이 이것
  - OpenCV 구간 완료 → 다음은 URDF + RViz
  - 자주 하는 실수: `__init` 오타, 따옴표(문자열 vs 객체: spin('judge')), 봉투(msg)와 숫자(msg.data) 혼동, 한 번(__init__)/매번(콜백) 자리 바꿈, Publisher에 콜백 넣기
  - 게시판 이름(주소, URL 경로 /image)과 양식 이름(스키마, sensor_msgs/msg/Image)은 다르다. create_subscription(양식, '게시판 이름', ...). `ros2 topic list -t`의 왼쪽이 게시판, [ ] 안이 양식. 이름은 대소문자까지 같아야 하고, 틀리면 에러 없이 아무것도 안 온다
  - 보낼 때는 봉투에 넣고(Int32() → .data = → publish(봉투)), 받을 때는 봉투에서 꺼낸다(msg.data). 숫자만 publish하면 TypeError. 칸 이름은 `ros2 interface show <양식>`으로 확인 (Pose는 msg.x, Twist는 cmd.linear.x)
  - 토픽은 노드가 켜져 있어야 보인다 (중앙 서버 없음). ros2 topic 명령은 어느 폴더에서 쳐도 같다
  - publish는 배달만 맡기고 바로 다음 줄로 간다. 구독자가 없으면 버려지고, 늦게 켠 구독자는 지난 글을 못 받는다
- URDF + RViz (urdf_practice/ 폴더, 튜토리얼 파일은 /opt/ros/jazzy/share/urdf_tutorial/urdf/)
  - 실행: `ros2 launch urdf_tutorial display.launch.py model:=$HOME/ros2_ws/urdf_practice/파일.urdf` (내 파일은 절대 경로)
  - u01 link 하나(원통/상자/구 바꿔 보기), u02 link 둘 + fixed joint, u03 origin 실험 후 왼쪽 다리(left_leg)를 직접 추가 (joint y만 +0.22로, visual은 오른쪽과 똑같이)
  - 새 실습은 새 파일에 쓴다 (u01에 덮어쓸 뻔함. 아직 커밋 안 한 파일은 git으로 못 되돌린다). u01, u02에 아직 깨진 곳 있음(따옴표, 닫는 태그)
  - 다음: fixed → 움직이는 joint로 바꿔 슬라이더로 다리 흔들기, /joint_states
- 노드 파일 이름 정리: publisher_, 클래스 이름은 노드 이름을 대문자로 이어 쓴 것(ImageViewer, GrayConverter), main의 변수 이름은 노드 이름과 같게

## 개념 정리

### ROS2
- 노드: 한 가지 일을 맡은 프로그램 하나
- 토픽: 이름 붙은 게시판. 노드끼리 직접 연결되지 않고 게시판을 사이에 둔다
  - 요청/응답이 아니라 한쪽 방향이다 (메시지 큐와 같은 구조). 요청/응답은 서비스 (예: /spawn)
- 메시지: 게시판에 올리는 글의 양식 (Twist: 속도 명령, Pose: 위치와 방향)
- Publisher는 올리는 쪽(정보를 원래 가진 쪽), Subscriber는 읽는 쪽
  - 게시판의 성질이 아니라, 그 게시판에 대한 노드의 역할이다
  - 헷갈리면 추리하지 말고 확인: `ros2 topic info <토픽> -v`, 또는 코드의 create_publisher / create_subscription
  - 언제 무엇을 쓰나: 노드를 함수(입력 → 출력)로 본다. "이 일을 하려면 무엇을 알아야 하나?" → Subscribe, "결과로 무엇을 내보내나/움직이나?" → Publish (Kafka의 consumer/producer와 같음)
  - 입력이 없으면 타이머(circle_publisher), 입력/출력이 바깥 세상(카메라, 키보드, 화면)이면 그쪽 토픽이 없다(cam2image, image_viewer)
  - 새 노드는 코드보다 먼저 "알아야 할 것 / 내보내는 것" 두 칸을 채운다. 예: 빨간 물체 보고 돌기 = /image Sub + /turtle1/cmd_vel Pub (speed_changer와 같은 구조, 판단 부분만 OpenCV)
- 콜백: 구독한 게시판에 새 글이 올 때(타이머는 정한 시간마다) 실행되는 함수
  - 내 코드가 부르지 않고 spin이 부른다. msg도 spin이 넣어 준다
  - 실행 횟수는 올리는 쪽이 정한다 (turtlesim의 pose는 1초에 약 60번)
  - 정의: 내가 직접 부르지 않고 "그 일이 생기면 불러 줘"라고 맡겨 둔 함수. 웹의 `button.addEventListener('click', handleClick)`의 handleClick과 같다 (브라우저 = spin)
  - 쓰는 이유는 반복이 아니라 "언제 생길지 내가 모르는 일"에 반응하려고. 반복은 일이 계속 생기니까 따라오는 결과
  - 맡기는 곳은 두 곳뿐: create_subscription(글이 오면, 콜백은 (self, msg)), create_timer(시간이 되면, 콜백은 (self)). Publisher에는 콜백을 넣지 않는다 (우체통일 뿐)
  - 타이머 콜백의 msg는 받은 게 아니라 콜백 안에서 String()/Int32()로 직접 만든 것
- spin: 글을 기다리다가 콜백을 불러 주는 것. 글이 안 오면 에러 없이 조용히 기다린다
  - spin(counter)는 counter 안에 등록된 알람/구독 목록을 보면서, 다음 알람까지 잠들었다가 때가 되면(또는 글이 오면) 깨서 콜백을 부른다. Ctrl+C 전까지 끝나지 않는다
  - 직접 sleep으로 기다리면 그동안 글을 못 받는다. 그래서 타이머도 spin에게 맡긴다
- throttle_duration_sec: 콜백 안의 로그만 줄이는 옵션 (콜백 횟수는 그대로). 1초에 수십 번 불리는 콜백(pose, image)에만 쓴다. 1초에 1번인데 쓰면 로그가 건너뛰어진다
- 노드 틀 + 빈칸 채울 때 질문 3개: Q1 내보내는 게 있나 → Publisher, Q2 알아야 할 게 있나 → Subscriber, Q3 받는 것 없이 반복할 일이 있나 → 타이머. 기억할 값은 __init__에서 self.이름 = 처음값 (이름은 내가 짓는 것, 예약어 아님)
- 노드 파일의 틀: import / class(Node 상속) / __init__(한 번: Publisher, Subscriber 생성) / 콜백(매번) / main(init → 노드 생성 → spin → 정리)
- 패키지와 빌드: 고치는 곳은 src, 실행되는 곳은 install. 고치면 colcon build
  - 새 노드는 setup.py의 console_scripts에 `'이름 = 패키지.파일:main'` 등록
  - source는 패키지를 새로 만들었을 때만 다시 필요
- Twist 단위: linear.x는 m/s(turtlesim에서는 창 칸 기준), angular.z는 rad/s(1.0이면 1초에 약 57도). z축은 늘 위를 향하고, 위에서 볼 때 +는 반시계(왼쪽), -는 시계(오른쪽)
- launch: ros2 run 여러 개를 한 번에 실행
- tf: frame은 "누구 기준으로 재는가". /tf 토픽에 "world 기준으로 나는 여기"를 올리면(broadcaster) 다른 조합은 계산해 준다(listener, lookup_transform)
  - pose의 x, y는 창 기준(가로, 세로). 거북이 기준 tf의 x, y는 앞쪽, 왼쪽
- colcon: 여러 패키지를 모아서 빌드하는 도구. 반드시 ~/ros2_ws에서 실행 (src 안에서 하면 src/build 등이 잘못 생김)

### OpenCV / 영상
- cv_bridge는 포장 뜯기와 다시 포장하기: imgmsg_to_cv2(msg, 'bgr8')는 ROS → OpenCV, cv2_to_imgmsg(사진, 'mono8')는 OpenCV → ROS
  - 인코딩은 "이 방식으로 꺼내 달라"는 주문. mono8 메시지를 bgr8로 꺼내면 밝기 하나를 세 칸에 복사해 준다
- shape: 컬러는 (세로, 가로, 3) 점 하나에 파랑/초록/빨강, 흑백은 (세로, 가로) 점 하나에 밝기 하나
- cv2.cvtColor(사진, cv2.COLOR_BGR2GRAY): 색 방식 바꾸기. 원래 사진은 그대로, 새 사진이 나온다
- 흑백 변환 이유: 윤곽선, QR/마커, 선 따라가기처럼 밝기 차이만 보는 처리가 많고 데이터가 1/3로 준다. 색이 중요한 일(빨간 공 찾기)에는 안 쓴다
- 받고 → 가공하고 → 올리는 노드의 틀: 가공 줄만 바꾸면 다른 처리(나중에는 AI 모델)가 된다
- OpenCV 다지기 (practice_opencv.py, ROS 없이 사진만 만져 보기)
  - 사진은 numpy 배열(숫자 격자). np.zeros((세로, 가로, 3), np.uint8)은 검은 사진
  - img[세로, 가로]로 점 하나, img[a:b, c:d]로 범위. 세로가 먼저, 0이 맨 위, 끝 숫자는 포함 안 됨
  - 가운데 놓기: 가운데 − 절반 : 가운데 + 절반. 나중에 칠한 것이 덮어쓴다
  - 색 순서는 BGR: 빨강은 [0, 0, 255]
  - 흑백 밝기 = 파랑×0.114 + 초록×0.587 + 빨강×0.299 (사람 눈 기준이라 초록이 가장 밝다). 그래서 흑백으로는 색 구분이 어렵다
  - cv2.inRange(사진, 아래한계, 위한계)로 마스크: 숫자 3개가 모두 범위 안이면 255, 아니면 0. shape는 흑백과 같다
- OpenCV 기초 사다리 (drills/c01~c06)
  - 만들기 vs 고르기: np.zeros((크기), np.uint8)는 새 표 만들기(소괄호 두 겹, 크기 숫자), img[a:b, c:d]는 있는 표에서 범위 고르기(대괄호, 콜론). np.array([값들])는 준 값을 그대로 담기(lower, upper)
  - 모양과 숫자 종류는 따로 정한다: (줄, 칸)이면 흑백, (줄, 칸, 3)이면 컬러. np.uint8은 둘 다 항상 붙인다(0~255 정수, 1바이트). 빠지면 소수(0., CV_64F)가 돼서 cvtColor 등이 에러
  - 대괄호 겹 수 = shape 숫자 개수 (JSON 중첩 배열과 같음)
  - 세로/가로라는 말은 "선 모양"과 "방향"이 섞여서 헷갈린다 → img[위에서 몇 번째, 왼쪽에서 몇 번째]로 읽는다. 범위의 개수는 끝 − 시작
  - 색은 외우지 않는다. 기억할 것은 B, G, R 순서 / 0은 꺼짐, 255는 다 켬 / 세 개가 같으면 회색. 빛은 섞으면 밝아진다([0,255,255] = 노랑, 다 켜면 흰색). 실제 값은 print(frame[y, x])로 재서 정한다
  - 흑백은 색을 밝기 하나로 뭉갠다(파랑 29, 빨강 76, 초록 150). 빨강과 어두운 회색이 같은 값이 될 수 있어서 색 찾기는 컬러 사진에 inRange
  - 마스크: lower/upper는 기준표(놀이기구 키 제한), 마스크는 칸마다 찍은 O/X 도장(255/0). 기준 숫자는 마스크에 들어가지 않는다. shape는 흑백과 같다. 칸의 색은 그대로인데 기준이 바뀌면 결과가 바뀐다(lower를 낮추면 너그러워져 O가 늘어남). 흰색은 R이 커도 upper의 B, G에서 탈락
  - 마스크는 그냥 흑백 표라 np.zeros로 직접 만들 수도 있다. inRange는 만드는 방법 중 하나
  - np.nonzero(mask)는 책 읽듯 훑어 흰 칸 위치를 찾고, (줄, 칸) 짝을 앞 숫자끼리(ys), 뒤 숫자끼리(xs) 나눠 준다. cx = xs.mean()으로 숫자 하나를 만들어야 if로 판단할 수 있다. cy는 위아래 판단이 필요할 때만
  - 평균은 멀리 떨어진 외톨이 칸 하나에 끌려간다(덩어리가 없는 곳이 cx가 될 수 있음). 실제 사진의 잡티 문제
  - lower/upper는 색 조건(SQL의 WHERE)일 뿐 위치를 정하지 않는다. inRange가 모든 칸을 검사하고, 위치는 마지막에 nonzero가 알아낸다
  - shape의 숫자는 길이(cm)가 아니라 칸(픽셀) 개수. numpy는 위아래가 먼저(240, 320), 모니터 사양은 좌우가 먼저(320 × 240). 옆으로 넓은 사진이면 큰 숫자가 좌우
  - cv2.imwrite('이름', 사진)는 파일로 저장(같은 이름이면 덮어씀), img = cv2.imread('이름')은 파일에서 불러오기(결과를 받아야 함). 사진이 파일에 있으면 ROS 노드가 필요 없다
  - 코드는 위에서 아래로 실행된다: waitKey(0) 아래의 print는 창을 닫아야 나오고, imshow 뒤에 그린 선은 안 보이고, inRange 뒤에 img에 그린 선은 mask에 없다. 보여 주고 기다리는 건 항상 마지막
  - 결과(cx 등)를 사진 위에 그려서 눈으로 확인하는 게 비전의 기본 디버깅(console.log와 같음). 소수인 cx는 int(cx)로 칸 번호로 바꾼다
  - lower를 낮추면 흰 칸이 늘어난다(240: 3602, 200: 4635, 50: 7693). 햄버거는 속이 찬 흰색이 아니라 흰 테두리 그림이라 기준에 따라 크게 변한다. 정답은 없고 모양이 잘 나오는 값을 고른다
  - 색 고르기는 데모용 도구. 나중엔 AI 모델이 물체 위치를 주고, 노드 틀(사진 → 위치 → cx → 판단 → 명령)은 그대로다
  - waitKey(0)은 창에서 키를 눌러야 끝난다. X로 닫으면 안 꺼짐. 끌 때는 Ctrl+C (Ctrl+Z는 일시정지일 뿐, 그땐 pkill -9 -f 파일이름)

### URDF / RViz
- URDF: 로봇 몸의 설계도(XML). DB 스키마처럼 "무엇이 어떻게 생겼나"만 적는다. RViz는 보여 주기만 하는 3D 화면(물리 없음, 물리는 Gazebo)
- link = 부품 하나(visual → geometry 안에 모양 하나만: cylinder length/radius, box size="앞뒤 좌우 위아래", sphere radius). 숫자 단위는 미터
- joint = 부품 연결. parent(누구에게 붙나), child(누가 붙나). tf와 같은 것. type="fixed"는 용접이라 슬라이더가 없다
- child에 쓴 이름은 link의 name과 한 글자까지 같아야 한다 (토픽 이름처럼)
- 방향: 🔴x 앞, 🟢y 왼쪽, 🔵z 위 (빨초파 = xyz). 내가 로봇 가운데 서 있으면 빨강 = 코, 초록 = 왼손, 파랑 = 머리 위. 마이너스는 반대쪽(y -0.22 = 오른쪽)
- origin 두 종류
  - joint 안의 origin xyz: 부모 가운데 기준으로 관절(엉덩이)을 어디에 둘까. 없으면 부모 한가운데(0,0,0)
  - link visual 안의 origin: 관절 기준으로 모양을 어떻게 놓을까. rpy는 x, y, z축을 꼬치처럼 꽂고 돌리기(1.57 rad = 90°), xyz는 옮기기
  - 튜토리얼 다리의 xyz 0 0 -0.3은 상자 길이 0.6의 절반만큼 내려서 윗끝이 관절에 매달리게 한 것. 나중에 관절이 움직이면 그 점을 중심으로 돈다
  - 왼쪽/오른쪽 다리는 joint 위치만 다르고 visual은 똑같다
- RViz 보는 법: 눈대중 말고 Add → Axes(Length 1) 화살표로 판정. Alpha를 낮춰 속을 본다. 노란 점은 카메라가 보는 중심
  - 화면의 "위"와 로봇의 "위"는 다르다. Views의 Pitch가 1.57 근처면 하늘에서 내려다보는 중(원통이 동그라미, 파랑이 점으로 보임). Pitch 0.3이면 옆에서 본다
- launch는 켤 때 URDF를 한 번만 읽는다(서버가 부팅 때 config 읽는 것과 같음). 순서: 고치기 → 저장 → 터미널에서 Ctrl+C → 다시 실행
- joint_state_publisher_gui: 움직이는 joint의 슬라이더 창. Randomize는 아무 값, Center는 전부 0. /joint_states로 발행
- XML 주석 `<!-- -->`: 겹칠 수 없고, 안에 `--` 못 쓰고, 태그 안에 못 넣는다. 한 줄씩 따로 쓴다. 혼자 닫는 태그는 `/>`

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
- `is not defined`: 이름 앞의 `무엇.`(cv2., self.bridge. 등)이 빠짐
- `required to be an integer`: 정해진 이름(cv2.COLOR_BGR2GRAY)을 따옴표로 감싸 문자열로 넘김
- `setting an array element with a sequence`: 칸 하나에 목록(숫자 여러 개)을 넣음. 넣는 숫자 개수 ≠ 칸에 들어가는 숫자 개수 → 원래 의도(흑백/컬러) 쪽에 맞춘다
- `too many indices ... 1-dimensional`: 표가 생각보다 작게 만들어짐 (np.zeros 대신 np.array를 씀 등)
- `Cannot interpret '300' as a data type`: np.zeros의 크기 숫자를 소괄호로 안 묶음
- `missing required argument 'mat'`: imshow에 창 이름이 빠짐. imshow('창 이름', 사진). 창 이름이 같으면 덮어쓴다
- `Unsupported depth ... CV_64F` / inRange `Sizes of input arguments do not match`: 사진이 uint8이 아니거나, 사진(흑백)과 lower/upper(숫자 3개)의 개수가 안 맞음. 에러 난 줄이 아니라 사진 만드는 줄이 원인일 수 있다
- 창이 안 뜨고 로그도 없으면: 보내는 노드(cam2image)가 켜져 있는지부터. spin은 글이 안 오면 조용히 기다린다
- 고쳤는데 그대로면 빌드했는지부터 확인 (URDF는 launch를 다시 켰는지)
- URDF `mismatched tag` / `not well-formed (invalid token)`: 태그를 안 닫았거나(`/>` 빠짐) 주석이 겹침. 줄/칸 번호를 본다
- URDF `Joint [이름] is missing a parent and/or child link`: 그 joint의 parent/child 줄에 오타(`linke=` 등). XML은 모르는 속성을 조용히 무시한다. 처음 나온 Error 줄을 읽는다

## 다음 목표
- OpenCV 연동, URDF+RViz, Gazebo 시뮬레이션까지 단계적으로 진행 예정
- 최종적으로 "자연어 명령 → 로봇 동작" 같은 LLM 연동 미니 프로젝트까지 만들어서 포트폴리오로 쓸 계획 (Physical AI 분야 취업 목표)

## 참고 사항
- 배경: STT/LLM 파이프라인(GPT-4o 연동 등) 실무 경험 있음 (AnesNote 프로젝트)
- 이 경험을 ROS2+AI 결합 프로젝트에 활용하고 싶어함
