import numpy as np
import time
from datetime import datetime, timedelta
from machine import machine_operate
from SQL import MySQL_query
from predict_model import Predict

class process_operate:

    def process_start(amount):
        std = 0.0025  # 표준편차   100만개 중에 12개 불량

        num = MySQL_query.key_for_count(1)  # 키 번호를 매기기 위한 값을 DB에서 가져옴 op10 키

        if num == []:  # 아무것도 없으면 -> 생산이 안됐음
            n = 10001  # 처음 10001 번 품목으로 키값을 찍어라. n은 P10001 <- 요 숫자
        else:  # 하나라도 있으면

            n = num[0]['product_key']  # ['product_key' : 'xxxx']  n은 키 값 -> str 형식
            bar_count = 0  # 키 파싱하기 위한
            for index in range(len(n)):

                if n[index] == '-':
                    bar_count = bar_count + 1

                    if bar_count == 3:
                        break

            n = int(n[index + 4:]) + 1  # 지금까지 만들어진 품목 번호 + 1을 시작값으로 만들겠다.

        total_test_data = []  # 예측할 test 데이터들을 뽑기 위한 모음

        stop_button = None  # 정지 버튼 True 되면 공정 스탑 하고 정지하거나 리셋

        ##### 전체적인 진행: body 생성 -> op10 실행 -> DB 저장 -> 저장한 데이터 가져오기 -> op10_data 변수 저장 -> 다음 공정 실행

        body_P0 = []  # 공정에 넣을 body 데이터 리스트 틀 -> Machine에 넣을 예정

        product_key_W1P0 = '-' + 'W1' + 'P' + str(n)  # 첫번째 제품 primary_key 생성 -> machine에서 시간 추가할 예정
        body_P0.append(product_key_W1P0)

        body_l_P0 = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l_P0 = round(body_l_P0, 5)  # 소수점 5째 자리까지 만들어줘
        body_P0.append(body_l_P0)  # 리스트에 담기

        body_w_P0 = np.random.normal(100, std)
        body_w_P0 = round(body_w_P0, 5)
        body_P0.append(body_w_P0)

        body_h_P0 = np.random.normal(50, std)
        body_h_P0 = round(body_h_P0, 5)
        body_P0.append(body_h_P0)

        op10_process_time_P0 = np.random.triangular(9, 10, 10)  # process_time 생성  (최소, 최대, 최빈)
        op10_process_time_P0 = round(op10_process_time_P0, 5)

        body_P0.append(op10_process_time_P0)

        body_P0.append(datetime.now() + timedelta(hours=9))  # 첫번째 제품은 현재시간부터 시작한다고 가정, 한국시간에 맞추기 위해 9시간 추가

        print('한개 생산 중')
        time.sleep(10)  # 10초 텀 실제 시간으로 텀을 주도록 만듬

        # op10 공정 실행 (W1P0)
        op10_data_P0 = machine_operate.op10(body_P0)
        product_key_W1P0 = op10_data_P0['product_key']

        ##### 여기에 웹페이지로 쏴주는 기능 추가 #####

        #################################### W1P0 생산 및 DB 저장 완료 #####################################

        # 다음 공정에 넣기 위한 데이터 가져와서 넣기
        op10_data_P0_from_DB = MySQL_query.get_quality_data_for_process(product_key_W1P0)

        op10_data_list_P0 = []  # P0 재공품 다음공정으로 넣어줄 데이터 저장할 리스트

        op10_l_P0 = op10_data_P0_from_DB[0]['product_size_l']  # 재공품 치수 데이터 가져오기
        op10_w_P0 = op10_data_P0_from_DB[0]['product_size_w']
        op10_h_P0 = op10_data_P0_from_DB[0]['product_size_h']


        op20_process_time_P0 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time 새로 생성
        op20_process_time_P0 = round(op20_process_time_P0, 5)

        op20_product_key_P0 = '-' + 'W2' + 'P' + str(n)  # 제품 키 생성

        op20_start_time_P0 = datetime.now() + timedelta(hours=9)

        op10_data_list_P0.append(op20_product_key_P0)  # 2번째 제품 키 - 인덱스 0번
        op10_data_list_P0.append(op10_l_P0)  # 1번 - 길이
        op10_data_list_P0.append(op10_w_P0)  # 2번 - 너비
        op10_data_list_P0.append(op10_h_P0)  # 3번 - 높이
        op10_data_list_P0.append(op20_process_time_P0)  # 4번 - 다음 공정 작업할 process_time
        op10_data_list_P0.append(op20_start_time_P0)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번 // # op20 넣기위한 리스트를 만들어주고 있음.



        body_P1 = []  # P1 제품에 대한 body 값 저장할 리스트

        product_key_W1P1 = '-' + 'W1' + 'P' + str(n+1)  # 첫번째 제품 primary_key 생성 -> machine에서 시간 추가할 예정
        body_P1.append(product_key_W1P1)

        body_l_P1 = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l_P1 = round(body_l_P1, 5)
        body_P1.append(body_l_P1)

        body_w_P1 = np.random.normal(100, std)
        body_w_P1 = round(body_w_P1, 5)
        body_P1.append(body_w_P1)

        body_h_P1 = np.random.normal(50, std)
        body_h_P1 = round(body_h_P1, 5)
        body_P1.append(body_h_P1)

        op10_process_time_P1 = np.random.triangular(9, 10, 10)  # process_time 생성
        op10_process_time_P1 = round(op10_process_time_P1, 5)


        body_P1.append(op10_process_time_P1)
        body_P1.append(datetime.now() + timedelta(hours=9))

        print('두개 생산 중')
        time.sleep(10)  # 10초 텀


        # op20 공정 실행 (W2P0)
        op20_data_P0 = machine_operate.op20(op10_data_list_P0)  # <- 앞공정 재공품 받아서 실행 //  리스트를 넣어줌
        product_key_W2P0 = op20_data_P0['product_key']

        #################################### W2P0 생산 및 DB 저장 완료 #####################################

        # op10 공정 실행 (W1P1)
        op10_data_P1 = machine_operate.op10(body_P1)
        product_key_W1P1 = op10_data_P1['product_key']

        #################################### W1P1 생산 및 DB 저장 완료 #####################################

        ##### 여기에다가 웹에다가 쏴주는 기능 추가 #####

        # 다음 공정에 넣기 위한 데이터 가져오기
        op20_data_P0_from_DB = MySQL_query.get_quality_data_for_process(product_key_W2P0)
        # 다음 공정에 넣기 위한 데이터 가져오기
        op10_data_P1_from_DB = MySQL_query.get_quality_data_for_process(product_key_W1P1)



        # op20 P0 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op20_data_list_P0 = []

        product_key_W3P0 = '-' + 'W3' + 'P' + str(n)  # 제품 키 생성
        op20_l_P0 = op20_data_P0_from_DB[0]['product_size_l']
        op20_w_P0 = op20_data_P0_from_DB[0]['product_size_w']
        op20_h_P0 = op20_data_P0_from_DB[0]['product_size_h']

        op20_timestamp_P0 = op20_data_P0_from_DB[0]['product_test_timestamp']  # op20 끝난시간

        op30_process_time_P0 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op30_process_time_P0 = round(op30_process_time_P0, 5)

        op30_start_time_P0 = datetime.now() + timedelta(hours=9)

        op20_data_list_P0.append(product_key_W3P0)
        op20_data_list_P0.append(op20_l_P0)
        op20_data_list_P0.append(op20_w_P0)
        op20_data_list_P0.append(op20_h_P0)
        op20_data_list_P0.append(op30_process_time_P0)
        op20_data_list_P0.append(op30_start_time_P0)


        # op10 P1 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op10_data_list_P1 = []

        product_key_W2P1 = '-' + 'W2' + 'P' + str(n+1)  # 제품 키 생성
        op10_l_P1 = op10_data_P1_from_DB[0]['product_size_l']
        op10_w_P1 = op10_data_P1_from_DB[0]['product_size_w']
        op10_h_P1 = op10_data_P1_from_DB[0]['product_size_h']

        op10_timestamp_P1 = op10_data_P1_from_DB[0]['product_test_timestamp']  # op20 끝난시간

        op20_process_time_P1 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op20_process_time_P1 = round(op20_process_time_P1, 5)

        op20_start_time_P1 = datetime.now() + timedelta(hours=9)

        op10_data_list_P1.append(product_key_W2P1)  # 재공품 데이터 -> 다음 공정에 투입 (P1제품)
        op10_data_list_P1.append(op10_l_P1)
        op10_data_list_P1.append(op10_w_P1)
        op10_data_list_P1.append(op10_h_P1)
        op10_data_list_P1.append(op20_process_time_P1)
        op10_data_list_P1.append(op20_start_time_P1)


        body_P2 = []  # P1 제품에 대한 body 값 저장할 리스트

        product_key_W1P2 = '-' + 'W1' + 'P' + str(n+2)  # 첫번째 제품 primary_key 생성 -> machine에서 시간 추가할 예정
        body_P2.append(product_key_W1P2)

        body_l_P2 = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l_P2 = round(body_l_P2, 5)
        body_P2.append(body_l_P2)

        body_w_P2 = np.random.normal(100, std)
        body_w_P2 = round(body_w_P2, 5)
        body_P2.append(body_w_P2)

        body_h_P2 = np.random.normal(50, std)
        body_h_P2 = round(body_h_P2, 5)
        body_P2.append(body_h_P2)

        op10_process_time_P2 = np.random.triangular(9, 10, 10)  # process_time 생성
        op10_process_time_P2 = round(op10_process_time_P2, 5)

        body_P2.append(op10_process_time_P2)
        body_P2.append(datetime.now() + timedelta(hours=9))  # 세번째 제품은 P1 끝난시간부터 시작



        # op30, 20, 10 시작

        print('세개 생산 중')
        time.sleep(10)

        # op30 공정 실행 (W3P0)
        op30_data_P0 = machine_operate.op30(op20_data_list_P0)  # <- 앞공정 재공품 받아서 실행

        pred_P0 = Predict.predict_quality(op10_data_P0, op20_data_P0, op30_data_P0)
        print("P0 예측값 : " + str(pred_P0))

        MySQL_query.insert_product_prediction(op30_data_P0, op20_data_P0, op10_data_P0, pred_P0)

        product_key_W3P0 = op30_data_P0['product_key']

        #################################### W3P0 생산 및 DB 저장 완료 #####################################

        # op20 공정 실행 (W2P1)
        op20_data_P1 = machine_operate.op20(op10_data_list_P1)  # <- 앞공정 재공품 받아서 실행
        product_key_W2P1 = op20_data_P1['product_key']

        #################################### W2P1 생산 및 DB 저장 완료 #####################################

        # op10 공정 실행 (W1P2)
        op10_data_P2 = machine_operate.op10(body_P2)
        product_key_W1P2 = op10_data_P2['product_key']

        #################################### W1P2 생산 및 DB 저장 완료 #####################################

        # 다음 공정에 넣기 위한 데이터 가져오기
        op30_data_P0_from_DB = MySQL_query.get_quality_data_for_process(product_key_W3P0)
        # 다음 공정에 넣기 위한 데이터 가져오기
        op20_data_P1_from_DB = MySQL_query.get_quality_data_for_process(product_key_W2P1)
        # 다음 공정에 넣기 위한 데이터 가져오기
        op10_data_P2_from_DB = MySQL_query.get_quality_data_for_process(product_key_W1P2)


        # op30 P0 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op30_data_list_P0 = []

        product_key_W4P0 = '-' + 'W4' + 'P' + str(n)  # 제품 키 생성
        op30_l_P0 = op30_data_P0_from_DB[0]['product_size_l']
        op30_w_P0 = op30_data_P0_from_DB[0]['product_size_w']
        op30_h_P0 = op30_data_P0_from_DB[0]['product_size_h']

        op30_timestamp_P0 = op30_data_P0_from_DB[0]['product_test_timestamp']  # op20 끝난시간

        op40_process_time_P0 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op40_process_time_P0 = round(op40_process_time_P0, 5)

        op40_start_time_P0 = datetime.now() + timedelta(hours=9)

        op30_data_list_P0.append(product_key_W4P0)
        op30_data_list_P0.append(op30_l_P0)
        op30_data_list_P0.append(op30_w_P0)
        op30_data_list_P0.append(op30_h_P0)
        op30_data_list_P0.append(op40_process_time_P0)
        op30_data_list_P0.append(op40_start_time_P0)

        # op20 P1 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op20_data_list_P1 = []

        product_key_W3P1 = '-' + 'W3' + 'P' + str(n+1)  # 제품 키 생성
        op20_l_P1 = op20_data_P1_from_DB[0]['product_size_l']
        op20_w_P1 = op20_data_P1_from_DB[0]['product_size_w']
        op20_h_P1 = op20_data_P1_from_DB[0]['product_size_h']

        op30_process_time_P1 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op30_process_time_P1 = round(op30_process_time_P1, 5)

        op30_start_time_P1 = datetime.now() + timedelta(hours=9)

        op20_data_list_P1.append(product_key_W3P1)
        op20_data_list_P1.append(op20_l_P1)
        op20_data_list_P1.append(op20_w_P1)
        op20_data_list_P1.append(op20_h_P1)
        op20_data_list_P1.append(op30_process_time_P1)
        op20_data_list_P1.append(op30_start_time_P1)


        # op10 P2 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op10_data_list_P2 = []

        product_key_W2P2 = '-' + 'W2' + 'P' + str(n+2)  # 제품 키 생성
        op10_l_P2 = op10_data_P2_from_DB[0]['product_size_l']
        op10_w_P2 = op10_data_P2_from_DB[0]['product_size_w']
        op10_h_P2 = op10_data_P2_from_DB[0]['product_size_h']

        op20_process_time_P2 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op20_process_time_P2 = round(op20_process_time_P2, 5)

        op20_start_time_P2 = datetime.now() + timedelta(hours=9)

        op10_data_list_P2.append(product_key_W2P2)
        op10_data_list_P2.append(op10_l_P2)
        op10_data_list_P2.append(op10_w_P2)
        op10_data_list_P2.append(op10_h_P2)
        op10_data_list_P2.append(op20_process_time_P2)
        op10_data_list_P2.append(op20_start_time_P2)


        body_P3 = []  # P3 제품에 대한 body 값 저장할 리스트

        product_key_W1P3 = '-' + 'W1' + 'P' + str(n+3)  # 첫번째 제품 primary_key 생성 -> machine에서 시간 추가할 예정
        body_P3.append(product_key_W1P3)

        body_l_P2 = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l_P2 = round(body_l_P2, 5)
        body_P3.append(body_l_P2)

        body_w_P2 = np.random.normal(100, std)
        body_w_P2 = round(body_w_P2, 5)
        body_P3.append(body_w_P2)

        body_h_P2 = np.random.normal(50, std)
        body_h_P2 = round(body_h_P2, 5)
        body_P3.append(body_h_P2)

        op10_process_time_P2 = np.random.triangular(9, 10, 10)  # process_time 생성
        op10_process_time_P2 = round(op10_process_time_P2, 5)

        body_P3.append(op10_process_time_P2)
        body_P3.append(datetime.now() + timedelta(hours=9))

        print('네개 생산 중')
        time.sleep(10)

        # op40 공정 실행 (W4P0)
        op40_data_P0 = machine_operate.op40(op30_data_list_P0)  # <- 앞공정 재공품 받아서 실행
        product_key_W4P0 = op40_data_P0['product_key']

        #################################### W4P0 생산 및 DB 저장 완료 #####################################

        # op30 공정 실행 (W3P1)
        op30_data_P1 = machine_operate.op30(op20_data_list_P1)  # <- 앞공정 재공품 받아서 실행

        pred_P1 = Predict.predict_quality(op10_data_P1, op20_data_P1, op30_data_P1)
        print("P1 예측값 : " + str(pred_P1))

        MySQL_query.insert_product_prediction(op30_data_P1, op20_data_P1, op10_data_P1, pred_P1)

        product_key_W3P1 = op30_data_P1['product_key']

        #################################### W3P1 생산 및 DB 저장 완료 #####################################

        # op20 공정 실행 (W2P2)
        op20_data_P2 = machine_operate.op20(op10_data_list_P2)
        product_key_W2P2 = op20_data_P2['product_key']

        #################################### W2P2 생산 및 DB 저장 완료 #####################################

        # op10 공정 실행 (W1P3)
        op10_data_P3 = machine_operate.op10(body_P3)
        product_key_W1P3 = op10_data_P3['product_key']
        total_test_data.append(op10_data_P3)

        #################################### W1P3 생산 및 DB 저장 완료 #####################################

        # 다음 공정에 넣기 위한 데이터 가져오기
        op40_data_P0_from_DB = MySQL_query.get_quality_data_for_process(product_key_W4P0)
        # 다음 공정에 넣기 위한 데이터 가져오기
        op30_data_P1_from_DB = MySQL_query.get_quality_data_for_process(product_key_W3P1)
        # 다음 공정에 넣기 위한 데이터 가져오기
        op20_data_P2_from_DB = MySQL_query.get_quality_data_for_process(product_key_W2P2)
        # 다음 공정에 넣기 위한 데이터 가져오기
        op10_data_P3_from_DB = MySQL_query.get_quality_data_for_process(product_key_W1P3)



        # op40 P0 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op40_data_list_P0 = []

        product_key_W5P0 = '-' + 'W5' + 'P' + str(n)  # 제품 키 생성
        op40_l_P0 = op40_data_P0_from_DB[0]['product_size_l']
        op40_w_P0 = op40_data_P0_from_DB[0]['product_size_w']
        op40_h_P0 = op40_data_P0_from_DB[0]['product_size_h']

        op40_timestamp_P0 = op40_data_P0_from_DB[0]['product_test_timestamp']  # op20 끝난시간

        op50_process_time_P0 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op50_process_time_P0 = round(op50_process_time_P0, 5)

        op50_start_time_P0 = datetime.now() + timedelta(hours=9)

        op40_data_list_P0.append(product_key_W5P0)
        op40_data_list_P0.append(op40_l_P0)
        op40_data_list_P0.append(op40_w_P0)
        op40_data_list_P0.append(op40_h_P0)
        op40_data_list_P0.append(op50_process_time_P0)
        op40_data_list_P0.append(op50_start_time_P0)

        # op30 P1 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op30_data_list_P1 = []

        product_key_W4P1 = '-' + 'W4' + 'P' + str(n+1)  # 제품 키 생성
        op30_l_P1 = op30_data_P1_from_DB[0]['product_size_l']
        op30_w_P1 = op30_data_P1_from_DB[0]['product_size_w']
        op30_h_P1 = op30_data_P1_from_DB[0]['product_size_h']

        op30_timestamp_P1 = op30_data_P1_from_DB[0]['product_test_timestamp']  # op30 끝난시간

        op40_process_time_P1 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op40_process_time_P1 = round(op40_process_time_P1, 5)

        op40_start_time_P1 = datetime.now() + timedelta(hours=9)

        op30_data_list_P1.append(product_key_W4P1)
        op30_data_list_P1.append(op30_l_P1)
        op30_data_list_P1.append(op30_w_P1)
        op30_data_list_P1.append(op30_h_P1)
        op30_data_list_P1.append(op40_process_time_P1)
        op30_data_list_P1.append(op40_start_time_P1)

        # op20 P2 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op20_data_list_P2 = []

        product_key_W3P2 = '-' + 'W3' + 'P' + str(n+2)  # 제품 키 생성
        op20_l_P2 = op20_data_P2_from_DB[0]['product_size_l']
        op20_w_P2 = op20_data_P2_from_DB[0]['product_size_w']
        op20_h_P2 = op20_data_P2_from_DB[0]['product_size_h']

        op30_process_time_P2 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op30_process_time_P2 = round(op30_process_time_P2, 5)

        op30_start_time_P2 = datetime.now() + timedelta(hours=9)

        op20_data_list_P2.append(product_key_W3P2)
        op20_data_list_P2.append(op20_l_P2)
        op20_data_list_P2.append(op20_w_P2)
        op20_data_list_P2.append(op20_h_P2)
        op20_data_list_P2.append(op30_process_time_P2)
        op20_data_list_P2.append(op30_start_time_P2)

        # op10 P1 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op10_data_list_P3 = []

        product_key_W2P3 = '-' + 'W2' + 'P' + str(n+3)  # 제품 키 생성
        op10_l_P3 = op10_data_P3_from_DB[0]['product_size_l']
        op10_w_P3 = op10_data_P3_from_DB[0]['product_size_w']
        op10_h_P3 = op10_data_P3_from_DB[0]['product_size_h']

        op20_process_time_P3 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op20_process_time_P3 = round(op20_process_time_P3, 5)

        op20_start_time_P3 = datetime.now() + timedelta(hours=9)

        op10_data_list_P3.append(product_key_W2P3)
        op10_data_list_P3.append(op10_l_P3)
        op10_data_list_P3.append(op10_w_P3)
        op10_data_list_P3.append(op10_h_P3)
        op10_data_list_P3.append(op20_process_time_P3)
        op10_data_list_P3.append(op20_start_time_P3)

        body_P4 = []  # P1 제품에 대한 body 값 저장할 리스트

        product_key_W1P4 = '-' + 'W1' + 'P' + str(n+4)  # 첫번째 제품 primary_key 생성 -> machine에서 시간 추가할 예정
        body_P4.append(product_key_W1P4)

        body_l_P3 = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l_P3 = round(body_l_P3, 5)
        body_P4.append(body_l_P3)

        body_w_P3 = np.random.normal(100, std)
        body_w_P3 = round(body_w_P3, 5)
        body_P4.append(body_w_P3)

        body_h_P3 = np.random.normal(50, std)
        body_h_P3 = round(body_h_P3, 5)
        body_P4.append(body_h_P3)

        op10_process_time_P3 = np.random.triangular(9, 10, 10)  # process_time 생성
        op10_process_time_P3 = round(op10_process_time_P3, 5)

        body_P4.append(op10_process_time_P3)
        body_P4.append(datetime.now() + timedelta(hours=9))  # 다섯 번째 제품은 P3 끝난시간부터 시작

        print('다섯개 생산 중')
        time.sleep(10)

        # op50 공정 실행 (W5P0)
        op50_data_P0 = machine_operate.op50(op40_data_list_P0)  # <- 앞공정 재공품 받아서 실행
        product_key_W5P0 = op50_data_P0['product_key']

        #################################### W5P0 생산 및 DB 저장 완료 #####################################

        # op40 공정 실행 (W4P1)
        op40_data_P1 = machine_operate.op40(op30_data_list_P1)  # <- 앞공정 재공품 받아서 실행
        product_key_W4P1 = op40_data_P1['product_key']

        #################################### W4P1 생산 및 DB 저장 완료 #####################################

        # op30 공정 실행 (W3P2)
        op30_data_P2 = machine_operate.op30(op20_data_list_P2)  # <- 앞공정 재공품 받아서 실행

        pred_P2 = Predict.predict_quality(op10_data_P2, op20_data_P2, op30_data_P2)
        print("P2 예측값 : " + str(pred_P2))

        MySQL_query.insert_product_prediction(op30_data_P2, op20_data_P2, op10_data_P2, pred_P2)

        product_key_W3P2 = op30_data_P2['product_key']

        #################################### W3P2 생산 및 DB 저장 완료 #####################################

        # op20 공정 실행 (W2P3)
        op20_data_P3 = machine_operate.op20(op10_data_list_P3)
        product_key_W2P3 = op20_data_P3['product_key']
        total_test_data.append(op20_data_P3)

        #################################### W2P3 생산 및 DB 저장 완료 #####################################

        # op10 공정 실행 (W1P4)
        op10_data_P4 = machine_operate.op10(body_P4)
        product_key_W1P4 = op10_data_P4['product_key']
        total_test_data.append(op10_data_P4)

        #################################### W1P4 생산 및 DB 저장 완료 #####################################


        # 여기서부터 6개씩 반복
        print('for문 진입')


        for i in range(n + 5, 100000):  # 6번째 제품부터 반복 시작

            op10_process_time = np.random.triangular(9, 10, 10)
            op10_process_time = round(op10_process_time, 5)

            op20_process_time = np.random.triangular(9, 10, 10)
            op20_process_time = round(op20_process_time, 5)

            op30_process_time = np.random.triangular(9, 10, 10)
            op30_process_time = round(op30_process_time, 5)

            op40_process_time = np.random.triangular(9, 10, 10)
            op40_process_time = round(op40_process_time, 5)

            op50_process_time = np.random.triangular(9, 10, 10)
            op50_process_time = round(op50_process_time, 5)

            op60_process_time = np.random.triangular(9, 10, 10)
            op60_process_time = round(op60_process_time, 5)


            if i == n + 5:  # 딱 처음 for 문 진입했을 때만 실행

                op50_data_P0_from_DB = MySQL_query.get_quality_data_for_process(product_key_W5P0)  # 전 공정에서 끝나고 결과 데이터

                op50_WIP = []  # op60에 넣기 위한 리스트

                product_key_W6P0 = '-' + 'W6' + 'P' + str(i - 5)  # key값 부여
                op50_l_P0 = op50_data_P0_from_DB[0]['product_size_l']  # 데이터 나눠서 변수에 저장
                op50_w_P0 = op50_data_P0_from_DB[0]['product_size_w']
                op50_h_P0 = op50_data_P0_from_DB[0]['product_size_h']
                op60_start_time = op50_data_P0_from_DB[0]['product_test_timestamp']

                op50_WIP.append(product_key_W6P0)  # 변수에 저장한거 하나씩 리스테에 저장
                op50_WIP.append(op50_l_P0)
                op50_WIP.append(op50_w_P0)
                op50_WIP.append(op50_h_P0)
                op50_WIP.append(op60_process_time)
                op50_WIP.append(op60_start_time)

                op40_data_P1_from_DB = MySQL_query.get_quality_data_for_process(product_key_W4P1)
                op40_WIP = []
                product_key_W5P1 = '-' + 'W5' + 'P' + str(i - 4)
                op40_l_P1 = op40_data_P1_from_DB[0]['product_size_l']
                op40_w_P1 = op40_data_P1_from_DB[0]['product_size_w']
                op40_h_P1 = op40_data_P1_from_DB[0]['product_size_h']
                op50_start_time = op40_data_P1_from_DB[0]['product_test_timestamp']

                op40_WIP.append(product_key_W5P1)
                op40_WIP.append(op40_l_P1)
                op40_WIP.append(op40_w_P1)
                op40_WIP.append(op40_h_P1)
                op40_WIP.append(op50_process_time)
                op40_WIP.append(op50_start_time)

                op30_data_P2_from_DB = MySQL_query.get_quality_data_for_process(product_key_W3P2)
                op30_WIP = []
                product_key_W4P2 = '-' + 'W4' + 'P' + str(i - 3)
                op30_l_P2 = op30_data_P2_from_DB[0]['product_size_l']
                op30_w_P2 = op30_data_P2_from_DB[0]['product_size_w']
                op30_h_P2 = op30_data_P2_from_DB[0]['product_size_h']
                op40_start_time = op30_data_P2_from_DB[0]['product_test_timestamp']

                op30_WIP.append(product_key_W4P2)
                op30_WIP.append(op30_l_P2)
                op30_WIP.append(op30_w_P2)
                op30_WIP.append(op30_h_P2)
                op30_WIP.append(op40_process_time)
                op30_WIP.append(op40_start_time)

                op20_data_P3_from_DB = MySQL_query.get_quality_data_for_process(product_key_W2P3)
                op20_WIP = []
                product_key_W3P3 = '-' + 'W3' + 'P' + str(i - 2)
                op20_l_P3 = op20_data_P3_from_DB[0]['product_size_l']
                op20_w_P3 = op20_data_P3_from_DB[0]['product_size_w']
                op20_h_P3 = op20_data_P3_from_DB[0]['product_size_h']
                op30_start_time = op20_data_P3_from_DB[0]['product_test_timestamp']

                op20_WIP.append(product_key_W3P3)
                op20_WIP.append(op20_l_P3)
                op20_WIP.append(op20_w_P3)
                op20_WIP.append(op20_h_P3)
                op20_WIP.append(op30_process_time)
                op20_WIP.append(op30_start_time)

                op10_data_P4_from_DB = MySQL_query.get_quality_data_for_process(product_key_W1P4)
                op10_WIP = []
                product_key_W2P4 = '-' + 'W2' + 'P' + str(i - 1)
                op10_l_P4 = op10_data_P4_from_DB[0]['product_size_l']
                op10_w_P4 = op10_data_P4_from_DB[0]['product_size_w']
                op10_h_P4 = op10_data_P4_from_DB[0]['product_size_h']
                op20_start_time = op10_data_P4_from_DB[0]['product_test_timestamp']

                op10_WIP.append(product_key_W2P4)
                op10_WIP.append(op10_l_P4)
                op10_WIP.append(op10_w_P4)
                op10_WIP.append(op10_h_P4)
                op10_WIP.append(op20_process_time)
                op10_WIP.append(op20_start_time)

                op10_time_stamp = datetime.now() + timedelta(hours=9)

            else:  # 한바퀴 돌고 난 다음
                op50_WIP = []
                product_key_W6 = '-' + 'W6' + 'P' + str(i - 5)

                op50_l = op50_data['op50_l']
                op50_w = op50_data['op50_w']
                op50_h = op50_data['op50_h']

                op50_WIP.append(product_key_W6)
                op50_WIP.append(op50_l)
                op50_WIP.append(op50_w)
                op50_WIP.append(op50_h)
                op50_WIP.append(op60_process_time)
                op50_WIP.append(datetime.now() + timedelta(hours=9))


                op40_WIP = []
                product_key_W5 = '-' + 'W5' + 'P' + str(i - 4)

                op40_l = op40_data['op40_l']
                op40_w = op40_data['op40_w']
                op40_h = op40_data['op40_h']

                op40_WIP.append(product_key_W5)
                op40_WIP.append(op40_l)
                op40_WIP.append(op40_w)
                op40_WIP.append(op40_h)
                op40_WIP.append(op50_process_time)
                op40_WIP.append(datetime.now() + timedelta(hours=9))


                op30_WIP = []
                product_key_W4 = '-' + 'W4' + 'P' + str(i - 3)

                op30_l = op30_data['op30_l']
                op30_w = op30_data['op30_w']
                op30_h = op30_data['op30_h']

                op30_WIP.append(product_key_W4)
                op30_WIP.append(op30_l)
                op30_WIP.append(op30_w)
                op30_WIP.append(op30_h)
                op30_WIP.append(op40_process_time)
                op30_WIP.append(datetime.now() + timedelta(hours=9))


                op20_WIP = []
                product_key_W3 = '-' + 'W3' + 'P' + str(i - 2)

                op20_l = op20_data['op20_l']
                op20_w = op20_data['op20_w']
                op20_h = op20_data['op20_h']


                op20_WIP.append(product_key_W3)
                op20_WIP.append(op20_l)
                op20_WIP.append(op20_w)
                op20_WIP.append(op20_h)
                op20_WIP.append(op30_process_time)
                op20_WIP.append(datetime.now() + timedelta(hours=9))


                op10_WIP = []
                product_key_W2 = '-' + 'W2' + 'P' + str(i - 1)

                op10_l = op10_data['op10_l']
                op10_w = op10_data['op10_w']
                op10_h = op10_data['op10_h']

                op10_WIP.append(product_key_W2)
                op10_WIP.append(op10_l)
                op10_WIP.append(op10_w)
                op10_WIP.append(op10_h)
                op10_WIP.append(op20_process_time)
                op10_WIP.append(datetime.now() + timedelta(hours=9))


            # 새 제품 생산
            body = []

            product_key_W1 = '-' + 'W1' + 'P' + str(i)

            body_l = np.random.normal(200, std)  # body 치수 데이터 생성
            body_l = round(body_l, 5)
            body_w = np.random.normal(100, std)  # body 치수 데이터 생성
            body_w = round(body_w, 5)
            body_h = np.random.normal(50, std)  # body 치수 데이터 생성
            body_h = round(body_h, 5)

            op10_time_stamp = datetime.now() + timedelta(hours=9)

            body.append(product_key_W1)
            body.append(body_l)
            body.append(body_w)
            body.append(body_h)
            body.append(op10_process_time)
            body.append(op10_time_stamp)  # 시작 시간

            time.sleep(10)   # 공정 실행

            # 공정들 6개 실행
            op60_data = machine_operate.op60(op50_WIP)
            op50_data = machine_operate.op50(op40_WIP)
            op40_data = machine_operate.op40(op30_WIP)
            op30_data = machine_operate.op30(op20_WIP)
            op20_data = machine_operate.op20(op10_WIP)
            op10_data = machine_operate.op10(body)

            total_test_data.append(op30_data)
            total_test_data.append(op20_data)
            total_test_data.append(op10_data)

            op10_data = total_test_data.pop(0)
            op20_data = total_test_data.pop(0)
            op30_data = total_test_data.pop(1)

            pred = Predict.predict_quality(op10_data, op20_data, op30_data)
            print('P' + str(i-2) + ' 품질 예측값: ' + str(pred))

            MySQL_query.insert_product_prediction(op30_data, op20_data, op10_data, pred)

            now_product = op60_data['product_key']

            print('6개 생산 완료! %s 제품이 생산되었습니다.' % (now_product))

        return "공정 실행 완료!"