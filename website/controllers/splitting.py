from datetime import datetime
import math
import random
from flask import request
import pandas as pd
from website.models import Models


class SplittingController:

    def count_dataWithLabel(self):
        instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_1 IS NOT NULL AND sentiment_2 IS NOT NULL AND sentiment_3 IS NOT NULL AND sentiment_4 IS NOT NULL AND sentiment_5 IS NOT NULL')
        data_labeling = instance_model.select()
        return data_labeling[0]['jumlah']

    def count_dataQ1WithLabel(self):
        instance_model_p = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_1 = "puas"')
        data_puas = instance_model_p.select()
        instance_model_c = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_1 = "cukup"')
        data_cukup = instance_model_c.select()
        instance_model_tp = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_1 = "tidak puas"')
        data_tidak_puas = instance_model_tp.select()
        data = {
            "puas" : data_puas[0]['jumlah'],
            "cukup" : data_cukup[0]['jumlah'],
            "tidak_puas" : data_tidak_puas[0]['jumlah'],
        }

        return data
    
    def count_dataQ2WithLabel(self):
        instance_model_p = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_2 = "puas"')
        data_puas = instance_model_p.select()
        instance_model_c = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_2 = "cukup"')
        data_cukup = instance_model_c.select()
        instance_model_tp = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_2 = "tidak puas"')
        data_tidak_puas = instance_model_tp.select()
        data = {
            "puas" : data_puas[0]['jumlah'],
            "cukup" : data_cukup[0]['jumlah'],
            "tidak_puas" : data_tidak_puas[0]['jumlah'],
        }

        return data
    
    def count_dataQ3WithLabel(self):
        instance_model_p = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_3 = "puas"')
        data_puas = instance_model_p.select()
        instance_model_c = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_3 = "cukup"')
        data_cukup = instance_model_c.select()
        instance_model_tp = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_3 = "tidak puas"')
        data_tidak_puas = instance_model_tp.select()
        data = {
            "puas" : data_puas[0]['jumlah'],
            "cukup" : data_cukup[0]['jumlah'],
            "tidak_puas" : data_tidak_puas[0]['jumlah'],
        }

        return data
    
    def count_dataQ4WithLabel(self):
        instance_model_p = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_4 = "puas"')
        data_puas = instance_model_p.select()
        instance_model_c = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_4 = "cukup"')
        data_cukup = instance_model_c.select()
        instance_model_tp = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_4 = "tidak puas"')
        data_tidak_puas = instance_model_tp.select()
        data = {
            "puas" : data_puas[0]['jumlah'],
            "cukup" : data_cukup[0]['jumlah'],
            "tidak_puas" : data_tidak_puas[0]['jumlah'],
        }

        return data
    
    def count_dataQ5WithLabel(self):
        instance_model_p = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_5 = "puas"')
        data_puas = instance_model_p.select()
        instance_model_c = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_5 = "cukup"')
        data_cukup = instance_model_c.select()
        instance_model_tp = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_5 = "tidak puas"')
        data_tidak_puas = instance_model_tp.select()
        data = {
            "puas" : data_puas[0]['jumlah'],
            "cukup" : data_cukup[0]['jumlah'],
            "tidak_puas" : data_tidak_puas[0]['jumlah'],
        }

        return data

    def count_dataWithLabelPos(self):
        instance_model_sentiment_1 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_1 = "puas"')
        data_sentiment_1 = instance_model_sentiment_1.select()
        instance_model_sentiment_2 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_2 = "puas"')
        data_sentiment_2 = instance_model_sentiment_2.select()
        instance_model_sentiment_3 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_3 = "puas"')
        data_sentiment_3 = instance_model_sentiment_3.select()
        instance_model_sentiment_4 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_4 = "puas"')
        data_sentiment_4 = instance_model_sentiment_4.select()
        instance_model_sentiment_5 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_5 = "puas"')
        data_sentiment_5 = instance_model_sentiment_5.select()
        count = data_sentiment_1[0]['jumlah'] + data_sentiment_2[0]['jumlah'] + data_sentiment_3[0]['jumlah'] + data_sentiment_4[0]['jumlah'] + data_sentiment_5[0]['jumlah']
        return count
    
    def count_dataWithLabelNeg(self):
        instance_model_sentiment_1 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_1 = "tidak puas"')
        data_sentiment_1 = instance_model_sentiment_1.select()
        instance_model_sentiment_2 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_2 = "tidak puas"')
        data_sentiment_2 = instance_model_sentiment_2.select()
        instance_model_sentiment_3 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_3 = "tidak puas"')
        data_sentiment_3 = instance_model_sentiment_3.select()
        instance_model_sentiment_4 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_4 = "tidak puas"')
        data_sentiment_4 = instance_model_sentiment_4.select()
        instance_model_sentiment_5 = Models('SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_5 = "tidak puas"')
        data_sentiment_5 = instance_model_sentiment_5.select()
        count = data_sentiment_1[0]['jumlah'] + data_sentiment_2[0]['jumlah'] + data_sentiment_3[0]['jumlah'] + data_sentiment_4[0]['jumlah'] + data_sentiment_5[0]['jumlah']
        print(count)
        return count

    def select_dataTrainQ1(self):
        instance_model = Models('SELECT * FROM tbl_data_train_q1')
        data_train = instance_model.select()
        return data_train

    def select_dataTestQ1(self):
        instance_model = Models('SELECT * FROM tbl_data_test_q1')
        data_test = instance_model.select()
        return data_test
    
    def select_dataTrainQ2(self):
        instance_model = Models('SELECT * FROM tbl_data_train_q2')
        data_train = instance_model.select()
        return data_train

    def select_dataTestQ2(self):
        instance_model = Models('SELECT * FROM tbl_data_test_q2')
        data_test = instance_model.select()
        return data_test
    
    def select_dataTrainQ3(self):
        instance_model = Models('SELECT * FROM tbl_data_train_q3')
        data_train = instance_model.select()
        return data_train

    def select_dataTestQ3(self):
        instance_model = Models('SELECT * FROM tbl_data_test_q3')
        data_test = instance_model.select()
        return data_test
    
    def select_dataTrainQ4(self):
        instance_model = Models('SELECT * FROM tbl_data_train_q4')
        data_train = instance_model.select()
        return data_train

    def select_dataTestQ4(self):
        instance_model = Models('SELECT * FROM tbl_data_test_q4')
        data_test = instance_model.select()
        return data_test
    
    def select_dataTrainQ5(self):
        instance_model = Models('SELECT * FROM tbl_data_train_q5')
        data_train = instance_model.select()
        return data_train

    def select_dataTestQ5(self):
        instance_model = Models('SELECT * FROM tbl_data_test_q5')
        data_test = instance_model.select()
        return data_test

    def delete_allDataSplit(self):
        instance_model = Models('DELETE FROM tbl_data_train_q1')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_test_q1')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_train_q2')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_test_q2')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_train_q3')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_test_q3')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_train_q4')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_test_q4')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_train_q5')
        instance_model.query_delete_all()
        instance_model = Models('DELETE FROM tbl_data_test_q5')
        instance_model.query_delete_all()
        return None

    def add_dataSplit(self):
        rasio = request.form['rasio']

        if rasio == '1:9':
            rasio_train = 0.9

        elif rasio == '2:8':
            rasio_train = 0.8

        # Select data Q berlabel
        instance_model = Models('SELECT * FROM tbl_data_clean WHERE sentiment_1 IS NOT NULL AND sentiment_2 IS NOT NULL AND sentiment_3 IS NOT NULL AND sentiment_4 IS NOT NULL AND sentiment_5 IS NOT NULL')
        data_withLabel = instance_model.select()

        df = pd.DataFrame(data_withLabel)

        # Membagi data train dan test dengan Stratified Sampling (Rasio label pada data latih dan uji sesuai dengan rasio label sebelum split data)
        train_q1 = df.groupby('sentiment_1', group_keys=False).apply(lambda x: x.sample(frac=rasio_train))
        test_q1 = df.drop(train_q1.index)
        train_q2 = df.groupby('sentiment_2', group_keys=False).apply(lambda x: x.sample(frac=rasio_train))
        test_q2 = df.drop(train_q2.index)
        train_q3 = df.groupby('sentiment_3', group_keys=False).apply(lambda x: x.sample(frac=rasio_train))
        test_q3 = df.drop(train_q3.index)
        train_q4 = df.groupby('sentiment_4', group_keys=False).apply(lambda x: x.sample(frac=rasio_train))
        test_q4 = df.drop(train_q4.index)
        train_q5 = df.groupby('sentiment_5', group_keys=False).apply(lambda x: x.sample(frac=rasio_train))
        test_q5 = df.drop(train_q5.index)

        data_simpan_train_q1 = []
        data_simpan_train_q2 = []
        data_simpan_train_q3 = []
        data_simpan_train_q4 = []
        data_simpan_train_q5 = []
        data_simpan_test_q1 = []
        data_simpan_test_q2 = []
        data_simpan_test_q3 = []
        data_simpan_test_q4 = []
        data_simpan_test_q5 = []

        for index, data in train_q1.iterrows():
            train_tuples = (data['id'], data['answer_1'], data['clean_answer_1'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_1'])
            data_simpan_train_q1.append(train_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_train_q1(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_train_q1)
        
        for index, data in train_q2.iterrows():
            train_tuples = (data['id'], data['answer_2'], data['clean_answer_2'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_2'])
            data_simpan_train_q2.append(train_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_train_q2(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_train_q2)
        
        for index, data in train_q3.iterrows():
            train_tuples = (data['id'], data['answer_3'], data['clean_answer_3'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_3'])
            data_simpan_train_q3.append(train_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_train_q3(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_train_q3)

        for index, data in train_q4.iterrows():
            train_tuples = (data['id'], data['answer_4'], data['clean_answer_4'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_4'])
            data_simpan_train_q4.append(train_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_train_q4(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_train_q4)
        
        for index, data in train_q5.iterrows():
            train_tuples = (data['id'], data['answer_5'], data['clean_answer_5'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_5'])
            data_simpan_train_q5.append(train_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_train_q5(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_train_q5)

        for index, data in test_q1.iterrows():
            test_tuples = (data['id'], data['answer_1'], data['clean_answer_1'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_1'])
            data_simpan_test_q1.append(test_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_test_q1(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_test_q1)
        
        for index, data in test_q2.iterrows():
            test_tuples = (data['id'], data['answer_2'], data['clean_answer_2'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_2'])
            data_simpan_test_q2.append(test_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_test_q2(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_test_q2)
        
        for index, data in test_q3.iterrows():
            test_tuples = (data['id'], data['answer_3'], data['clean_answer_3'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_3'])
            data_simpan_test_q3.append(test_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_test_q3(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_test_q3)
        
        for index, data in test_q4.iterrows():
            test_tuples = (data['id'], data['answer_4'], data['clean_answer_4'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_4'])
            data_simpan_test_q4.append(test_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_test_q4(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_test_q4)
        
        for index, data in test_q5.iterrows():
            test_tuples = (data['id'], data['answer_5'], data['clean_answer_5'], data['name'], str(datetime.strftime(datetime.strptime(str(data['created_at']),'%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')), data['sentiment_5'])
            data_simpan_test_q5.append(test_tuples)

        instance_model = Models('INSERT IGNORE tbl_data_test_q5(id, text, clean_text, user, created_at, sentiment) VALUES (%s, %s, %s, %s, %s, %s)')
        instance_model.query_sql_multiple(data_simpan_test_q5)

        return 'true'