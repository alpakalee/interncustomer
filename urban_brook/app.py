from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

#구글 시트 인증정보 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/digital-yeti-429601-v5-01c3837c2955.json", scope)
gc = gspread.authorize(creds)

#플라스크 실행
app = Flask(__name__)

# 초기 고객 데이터
initial_data = [
    {'상담일자': '7/13', '행사일자': '7/20', '고객명': '○○○', '행사 종류': '결혼식', '전화번호': '010-1111-1111', '상담중/상담완료': '상담완료'},
    {'상담일자': '7/13', '행사일자': '7/21', '고객명': '●●●', '행사 종류': '돌잔치', '전화번호': '010-1111-1112', '상담중/상담완료': '상담중'},
    {'상담일자': '7/15', '행사일자': '7/22', '고객명': 'OOO', '행사 종류': '결혼식', '전화번호': '010-0000-0000', '상담중/상담완료': '상담중'},
    {'상담일자': '7/15', '행사일자': '7/23', '고객명': '□□s□', '행사 종류': '세미나', '전화번호': '010-1111-1113', '상담중/상담완료': '상담완료'},
    {'상담일자': '7/15', '행사일자': '7/23', '고객명': '□□d□', '행사 종류': '세미나', '전화번호': '010-1111-1113', '상담중/상담완료': '상담완료'},
    {'상담일자': '7/15', '행사일자': '7/23', '고객명': '□c□□', '행사 종류': '세미나', '전화번호': '010-1111-1113', '상담중/상담완료': '상담완료'},
    {'상담일자': '7/15', '행사일자': '7/23', '고객명': '□□v□', '행사 종류': '세미나', '전화번호': '010-1111-1113', '상담중/상담완료': '상담완료'},
    {'상담일자': '7/15', '행사일자': '7/23', '고객명': '□sq□□', '행사 종류': '세미나', '전화번호': '010-1111-1113', '상담중/상담완료': '상담완료'},
    {'상담일자': '7/15', '행사일자': '7/23', '고객명': '□□b□', '행사 종류': '세미나', '전화번호': '010-1111-1113', '상담중/상담완료': '상담완료'},
    {'상담일자': '7/15', '행사일자': '7/23', '고객명': '□□s□', '행사 종류': '세미나', '전화번호': '010-1111-1113', '상담중/상담완료': '상담완료'},
    {'상담일자': '7/15', '행사일자': '7/23', '고객명': '□□z□', '행사 종류': '세미나', '전화번호': '010-1111-1113', '상담중/상담완료': '상담완료'},
    {'상담일자': '7/15', '행사일자': '7/23', '고객명': '□□x□', '행사 종류': '세미나', '전화번호': '010-1111-1113', '상담중/상담완료': '상담완료'}
]

spreadsheet_url1= "https://docs.google.com/spreadsheets/d/1rSQ9kiJ59S6aYP-oXaFDVTe2cSlt48Xr8FgKz-gZIM4/edit?gid=1361594786#gid=1361594786"
spreadsheet_url2= "https://docs.google.com/spreadsheets/d/1OtWfY2pDtMweXd74ttAleVNloei8cyM99uGSmZISn1A/edit?gid=1258371576#gid=1258371576"
spreadsheet_url3= "https://docs.google.com/spreadsheets/d/1Ogb4zN56bskVjSdp7jk6tNVntbec2GS1DDBunQfVi2U/edit?gid=1609720562#gid=1609720562"

# 엑셀 파일 경로(고객관리 저장)
excel_file = 'customers.xlsx'

#엑셀이 없으면 생성
def create_initial_excel(file_path, data):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

#초기실행시 고객관리 데이터 불러오기
def load_customers_from_excel(file_path):
    if not os.path.exists(file_path):
        create_initial_excel(file_path, initial_data)
    df = pd.read_excel(file_path)
    customers = df.to_dict(orient='records')
    return customers

#고객관리 데이터 저장
def save_customers_to_excel(file_path, customers):
    df = pd.DataFrame(customers)
    df.to_excel(file_path, index=False)
    
# 고객 상세정보 데이터 가져오기
def get_customer_from_excel(file_path, index):
    df = pd.read_excel(file_path)
    customer = df.iloc[index].to_dict()
    return customer

# 고객 상세정보 데이터 저장
def save_customer_to_excel(file_path, index, customer):
    df = pd.read_excel(file_path)
    for key in customer:
        df.at[index, key] = customer[key]
    df.to_excel(file_path, index=False)
    
# 고객 관리 데이터 삭제
def delete_customer_from_excel(file_path, index):
    df = pd.read_excel(file_path)
    df.drop(index, inplace=True)
    df.to_excel(file_path, index=False)

# 구글 시트에서 데이터 가져오기
def get_google_sheet_data(spreadsheet_url, worksheet_name):
    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet(worksheet_name)
    data = worksheet.get_all_records()
    return data

# 고객명, 행사종류로 고객 데이터 찾기
def find_customer_data(sheet_data, customer_name, event_type):
    search_column = '예약자 성함'
    if event_type == "비즈니스":
        search_column = '예약자(담당자) 성함'
    
    for row in sheet_data:
        if row.get(search_column) == customer_name:
            return row
    return None

# 행사종류에 따른 구글 시트 링크
def get_sheet_details_by_event_type(event_type):
    if event_type == "돌/가족행사":
        return {
            "spreadsheet_url": spreadsheet_url1,
            "worksheet_name": "설문지 응답 시트1"
        }
    elif event_type == "웨딩":
        return {
            "spreadsheet_url": spreadsheet_url2,
            "worksheet_name": "설문지 응답 시트1"
        }
    elif event_type == "비즈니스":
        return {
            "spreadsheet_url": spreadsheet_url3,
            "worksheet_name": "설문지 응답 시트1"
        }
    else:
        return None
    
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
            print(f"유효하지 않은 날짜 형식: {date_str}, 오류: {ve}")
    return count

@app.route('/')
def index():
    customers = load_customers_from_excel(excel_file)
    count_1 = count_new_reservations(spreadsheet_url1)
    count_2 = count_new_reservations(spreadsheet_url2)
    count_3 = count_new_reservations(spreadsheet_url3)
    return render_template('index.html', customers=customers, count_1=count_1,count_2=count_2,count_3=count_3)


# 삭제 기능
@app.route('/delete/<int:index>', methods=['POST'])
def delete_customer(index):
    delete_customer_from_excel(excel_file, index)
    return redirect(url_for('index'))

@app.route('/detail/<int:index>', methods=['GET', 'POST'])
def detail(index):
    if request.method == 'POST':
        customer = get_customer_from_excel(excel_file, index)
        customer['상담내용'] = request.form['상담내용']
        customer['상담중/상담완료'] = request.form['상담중/상담완료']
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
        '상담일자': request.form['상담일자'],
        '행사일자': request.form['행사일자'],
        '고객명': request.form['고객명'],
        '행사 종류': request.form['행사종류'],
        '전화번호': request.form['전화번호'],
        '상담내용': request.form['상담내용'],
        '상담중/상담완료': request.form['상담중/상담완료']
    }
    customers = load_customers_from_excel(excel_file)
    customers.append(new_customer)
    save_customers_to_excel(excel_file, customers)
    return redirect(url_for('index'))

@app.route('/update_status/<int:index>/<status>', methods=['POST'])
def update_status(index, status):
    customer = get_customer_from_excel(excel_file, index)
    customer['상담일자'] = request.form['상담일자']
    customer['행사일자'] = request.form['행사일자']
    customer['고객명'] = request.form['고객명']
    customer['행사 종류'] = request.form['행사종류']
    customer['전화번호'] = request.form['전화번호']
    customer['상담내용'] = request.form['상담내용']
    customer['상담중/상담완료'] = status
    save_customer_to_excel(excel_file, index, customer)
    return '', 204  # No Content response to indicate successful update

@app.route('/response_form/<int:index>', methods=['GET'])
def response_form(index):
    customer = get_customer_from_excel(excel_file, index)
    event_type = customer['행사 종류']
    customer_name = customer['고객명']

    sheet_details = get_sheet_details_by_event_type(event_type)
    if not sheet_details:
        return "Invalid event type"

    sheet_data = get_google_sheet_data(sheet_details['spreadsheet_url'], sheet_details['worksheet_name'])
    customer_data = find_customer_data(sheet_data, customer_name, event_type)

    if not customer_data:
        return "Customer data not found in Google Sheets"

    return render_template('response_form.html', customer_data=customer_data)

if __name__ == '__main__':
    app.run(debug=True)
