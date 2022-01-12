from pymysql import connect
from pymysql.cursors import DictCursor

# 연락처에 관련된 로직을 담당하는 파일
# db연결/ cursor 변수
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


def add_contact_to_db(params):
    
    # 사전검사 추가 : user_id 파라미터의 값이 실제 사용자 id가 맞는지?
    sql = f"SELECT * FROM users WHERE id = {params['user_id']}"
    
    cursor.execute(sql)
    user_result = cursor.fetchone()
    
    if user_result == None:
        return{
            'code' : 400,
            'message' : '해당 사용자 id 없음'
        }, 400
    
    sql = f"INSERT INTO contacts (user_id, name, phone_num, memo) VALUES ({params['user_id']}, '{params['name']}', '{params['phone']}', '{params['memo']}'"
    
    print('SQL : ', sql)
    
    return {
        'code' : 200,
        'message' : '임시 성공 응답',
    }