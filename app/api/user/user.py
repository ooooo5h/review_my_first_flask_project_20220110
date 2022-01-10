from pymysql import connect
from pymysql.cursors import DictCursor
# 사용자 정보 관련된 기능들을 모아두는 모듈
# app.py에서 이 함수들을 끌어다 사용

# DB 연결 전담 변수
db = connect(
    host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com',
    port=3306,
    user='admin',
    passwd='Vmfhwprxm!123',
    db='test_phone_book',
    charset='utf8',
    cursorclass=DictCursor
)

cursor = db.cursor()


def user_test():
    
    # 추가 기능 작성  
    # DB에서 아이디/비밀번호를 조회해서, 로그인 확인 등
    
    return {
        'name' : '전은형',
        'birth_year' : 1991,
    }
 
# 로그인 테스트 기능   
def login_test(id, pw):
    # id, pw를 이용해서  -> SQL 쿼리 작성 -> 결과에 따라 다른 응답 리턴 
    
    sql = f"SELECT * FROM users WHERE email='{id}' AND password='{pw}'"
    cursor.execute(sql)
    
    query_result = cursor.fetchone()  # 검색결과 없으면, None 리턴. 검색결과 있으면, 사용자의 정보를 담은 dict 리턴
    
    # 쿼리 결과가 None이다 > 아이디 비번 맞는 사람이 없다 > 로그인 실패
    if query_result == None :
        return{
            'code' : 400,
            'message' : '아이디 또는 비밀번호가 잘못되었습니다.'
        }, 400
    else :
        # 검색 결과가 있다 > 아이디/비밀번호 모두 맞는 사람이 있다 > 로그인 성공
        # query_result의 실체가 있다 > None이 아니다 => 앱에서 사용 가능한 JSONObject로 보내보자
        
        print(query_result)
        
        user_dict = {
            'id' : query_result['id'],
            'email' : query_result['email'],
            'nickname' : query_result['nickname'],
        }
        
        
        return{
            'code' : 200,
            'message' : '로그인 성공',
            'data' : {
                'user' : user_dict,
            }
        }
    
 
# 회원가입 기능
# 1. 이메일이 이미 사용중이라면 400으로 에러처리
# 2. 닉네임도 사용중이라면 400으로 에러처리
# 둘 다 통과해야지 실제 INSERT INTO -> 결과를 200으로 내려주고, 가입된 사용자 정보도 내려줄꺼야
def sign_up(params):   
    
    # 이메일(params['email']이 이미 사용중인지, 같은 이메일이 DB에 있는가 조회하기 => SELECT문
    sql = f"SELECT * FROM users WHERE email = '{params['email']}'"
    
    cursor.execute(sql)
    email_check_result = cursor.fetchone()
    
    # ecr가 None이라면 사용가능한 이메일
    # ecr가 None이 아니라면 사용불가
    if email_check_result:
        return{
            'code' : 400,
            'message' : '이미 사용중인 이메일입니다.'
        }, 400
    
    # 닉네임이 사용중인가? 사용중이라면 CODE 400, MESSAGE 이미 사용중인 닉네임입니다.
    sql = f"SELECT * FROM users WHERE nickname = '{params['nick']}'"
    
    cursor.execute(sql)
    nickname_check_result = cursor.fetchone()
    
    if nickname_check_result:
        return {
            'code' : 400,
            'message' : '이미 사용중인 닉네임입니다.',
        }, 400
    
    
    sql = f"INSERT INTO users (email, password, nickname) VALUES ('{params['email']}', '{params['pw']}', '{params['nick']}');"
    
    print(f'완성된 쿼리 : {sql}')

    cursor.execute(sql)
    db.commit()
    
    return {
        'test' : '테스트'
    }