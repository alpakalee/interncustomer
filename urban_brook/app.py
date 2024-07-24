from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 구글 시트 인증정보 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("digital-yeti-429601-v5-01c3837c2955.json", scope)
gc = gspread.authorize(creds)

# 플라스크 실행
app = Flask(__name__)

# 초기 고객 데이터
initial_data = [
    {'상담일': '새로생성됨', '행사종류': '새로생성됨', '구분': '새로생성됨', '행사날짜': '새로생성됨', '예상인원': '새로생성됨','시간': '새로생성됨', '예약자': '새로생성됨',  '연락처': '엑셀파일을 열어 변경하세요', '계약미완료/계약완료': '새로생성됨', '문자발송': '새로생성됨', '상담내용': '새로생성됨'}
]

#돌/가족잔치, 웨딩, 비즈니스, 기타 순
spreadsheet_url1= "https://docs.google.com/spreadsheets/d/1rSQ9kiJ59S6aYP-oXaFDVTe2cSlt48Xr8FgKz-gZIM4/edit?gid=1361594786#gid=1361594786"
spreadsheet_url2= "https://docs.google.com/spreadsheets/d/1OtWfY2pDtMweXd74ttAleVNloei8cyM99uGSmZISn1A/edit?gid=1258371576#gid=1258371576"
spreadsheet_url3= "https://docs.google.com/spreadsheets/d/1Ogb4zN56bskVjSdp7jk6tNVntbec2GS1DDBunQfVi2U/edit?gid=1609720562#gid=1609720562"
spreadsheet_url4= "https://docs.google.com/spreadsheets/d/1b-5orqX9nHSNMkmbW8qgHO4QK3fcdFHi8ieSojJX0jQ/edit?gid=926356915#gid=926356915"

# 엑셀 파일 경로(고객관리 저장)
excel_file = 'urban_brook_CRM.xlsx'

# 엑셀이 없으면 생성
def create_initial_excel(file_path, data):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

# 초기 실행시 고객관리 데이터 불러오기
def load_customers_from_excel(file_path):
    if not os.path.exists(file_path):
        create_initial_excel(file_path, initial_data)
    df = pd.read_excel(file_path, dtype=str)
    customers = df.to_dict(orient='records')
    return customers

# 고객관리 데이터 저장
def save_customers_to_excel(file_path, customers):
    df = pd.DataFrame(customers)
    df.to_excel(file_path, index=False)

# 고객 상세정보 데이터 가져오기
def get_customer_from_excel(file_path, index):
    df = pd.read_excel(file_path, dtype=str)
    customer = df.iloc[index].to_dict()
    return customer

# 고객 상세정보 데이터 저장
def save_customer_to_excel(file_path, index, customer):
    df = pd.read_excel(file_path, dtype=str)
    for key in customer:
        df.at[index, key] = customer[key]
    df.to_excel(file_path, index=False)

# 행사종류에 따른 구글 시트 데이터
def get_sheet_data_by_event_type(event_type):
    if event_type == "돌/가족행사":
        spreadsheet_url = spreadsheet_url1
    elif event_type == "웨딩":
        spreadsheet_url = spreadsheet_url2
    elif event_type == "비즈니스":
        spreadsheet_url = spreadsheet_url3
    elif event_type == "기타":
        spreadsheet_url = spreadsheet_url4
    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet("설문지 응답 시트1")
    data = worksheet.get_all_records()
    return data

# 새 예약 수 계산
def count_new_reservations(sheet_url):
    today = datetime.today().date()
    doc = gc.open_by_url(sheet_url)
    worksheet = doc.worksheet("설문지 응답 시트1")
    sheet_dates = worksheet.col_values(1)
    count = 0
    for date_str in sheet_dates:
        try:
            if date_str == "타임스탬프":
                continue
            date_only_str = date_str.split()[0] + " " + date_str.split()[1] + " " + date_str.split()[2]
            date_obj = datetime.strptime(date_only_str, '%Y. %m. %d').date()

            date_diff = abs((today - date_obj).days)
            # 날짜 비교
            if date_diff <= 1:
                count += 1
        except ValueError as ve:
            pass
    return count

# 비동기적으로 예약 수를 가져오는 API
@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    count_1_1 = count_new_reservations(spreadsheet_url1)
    count_2_2 = count_new_reservations(spreadsheet_url2)
    count_3_3 = count_new_reservations(spreadsheet_url3)
    count_4_4 = count_new_reservations(spreadsheet_url4)
    return jsonify({
        'count_1': count_1_1,
        'count_2': count_2_2,
        'count_3': count_3_3,
        'count_4': count_4_4
    })

@app.route('/')
def index():
    customers = load_customers_from_excel(excel_file)
    return render_template('index.html', customers=customers)

@app.route('/detail/<int:index>', methods=['GET', 'POST'])
def detail(index):
    if request.method == 'POST':
        customer = get_customer_from_excel(excel_file, index)
        save_customer_to_excel(excel_file, index, customer)
        return redirect(url_for('detail', index=index))
    customer = get_customer_from_excel(excel_file, index)
    return render_template('detail.html', customer=customer, index=index)

@app.route('/add_customer')
def add_customer():
    return render_template('add_customer.html')

@app.route('/create_customer', methods=['POST'])
def create_customer():
    new_customer = {
        '상담일': request.form['상담일'],
        '행사종류': request.form['행사종류'],
        '구분': request.form['구분'],
        '행사날짜': request.form['행사날짜'],
        '예상인원': request.form['예상인원'],
        '시간': request.form['시간'],
        '예약자': request.form['예약자'],
        '연락처': request.form['연락처'],
        '계약미완료/계약완료': request.form['계약미완료/계약완료'],
        '문자발송': request.form['문자발송'],
        '상담내용': request.form['상담내용']
    }
    customers = load_customers_from_excel(excel_file)
    customers.append(new_customer)
    save_customers_to_excel(excel_file, customers)
    return redirect(url_for('index'))

@app.route('/update_status/<int:index>/<status>', methods=['POST'])
def update_status(index, status):
    customer = get_customer_from_excel(excel_file, index)
    customer['상담일'] = request.form['상담일']
    customer['행사종류'] = request.form['행사종류']
    customer['구분'] = request.form['구분']
    customer['행사날짜'] = request.form['행사날짜']
    customer['예상인원'] = request.form['예상인원']
    customer['시간'] = request.form['시간']
    customer['예약자'] = request.form['예약자']
    customer['연락처'] = request.form['연락처']
    customer['계약미완료/계약완료'] = status
    customer['문자발송'] = request.form['문자발송']
    customer['상담내용'] = request.form['상담내용']
    save_customer_to_excel(excel_file, index, customer)
    return '', 204  # No Content response to indicate successful update

@app.route('/response_form/<int:index>', methods=['GET'])
def response_form(index):
    customer = get_customer_from_excel(excel_file, index)
    event_type = customer['행사종류']
    customer_name = customer['예약자']
    sheet_data = get_sheet_data_by_event_type(event_type)
    
    customer_data_list = [row for row in sheet_data if row.get('예약자 성함' if event_type != "비즈니스" else '예약자(담당자) 성함') == customer_name]
    
    if not customer_data_list:
        return jsonify({'error': f"{event_type}의 구글 시트에서 예약자 명을 찾지 못했습니다.\n다시 한 번 확인해주세요."}), 404

    return jsonify({'customer_data_list': customer_data_list})

@app.route('/show_response_form')
def show_response_form():
    return render_template('response_form.html')

if __name__ == '__main__':
    app.run(debug=True)
