from flask import Flask, request
from flask.templating import render_template
from flask_cors import CORS

from .api import user_test, login_test, sign_up, add_contact_to_db

def create_app():
    # 플라스크 서버를 변수에 담자
    app = Flask(__name__)
    
    # 만든 서버를 CORS 설정 적용
    CORS(app)
    
    # 서버에 대한 세팅 진행
    
    @app.route("/")   # 만들고있는 서버의 / (아무것도 안붙인 주소)로 접속하면 보여줄 내용
    def home():
        # return 내용 : HTML등 웹 프론트엔드 태그
        return "<h1>Hello World!</h1>"  # Hello World 문장 리턴 => 이 내용을 사용자에게 보여주겠다.

    @app.route('/module_test')
    def module_test():
        return user_test()  # 다른 모듈의 함수의 실행결과를 내보내자 => 로직은 다른 모듈에서만 작성하면 됨
    
    
    @app.route('/login_test')
    def login_01():
        # 외부에서 보내준 파라미터들 확인
        params = request.args.to_dict()
        print(f'전달받은 파라미터 : {params}')
        
        # 아이디 : login_id 이름표를 뽑아서 사용
        # 비밀번호 : pw 이름표로 뽑아서 사용
        
        # 원하는 파라미터가 안들어왔다면? 잘못보냈다고 알려주는 코드를 추가하자
        # dict의 key값의 데이터가 실제 존재하나??
        if 'login_id' not in params.keys() or 'pw' not in params.keys():
            return {
               'code' : 400,
               'message' : 'login_id / pw 중 하나가 첨부되지 않았습니다.' 
            }
            
        id = params['login_id']
        pw = params['pw']
        
        return login_test(id, pw)
    
    
    # 회원가입 주소
    @app.route("/sign_up")
    def sign_up_url():
        # 받아낸 파라미터를 그냥 통째로 회원가입 함수에 전달하자
        return sign_up(request.args.to_dict())
    
    
    # 전화번호부 추가 등록
    @app.route("/add_contact")
    def add_contact_to_url():
        return add_contact_to_db(request.args.to_dict())
    
    # 이 서버를 사용하도록 결과로 내보내기
    return app