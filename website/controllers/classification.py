from math import nan
from sklearn.calibration import LabelEncoder
from sklearn.metrics import confusion_matrix
from website.models import Models
from sklearn.feature_extraction.text import CountVectorizer
from flask import flash, json
import pickle
import os
import numpy as np

from website.multinb import MultiNB

class ClassificationController:
    def createModel(self, num = ""):

        # instance_model = Models('SELECT COUNT(id) as jumlah FROM tbl_data_train WHERE clean_text IS NOT NULL AND sentiment IS NOT NULL')
        # sentiment_count = instance_model.select()

        # instance_model = Models("SELECT COUNT(id) as positif FROM tbl_data_train WHERE clean_text IS NOT NULL AND sentiment = 'positif'")
        # sentiment_positif = instance_model.select()

        # instance_model = Models("SELECT COUNT(id) as negatif FROM tbl_data_train WHERE clean_text IS NOT NULL AND sentiment = 'negatif'")
        # sentiment_negatif = instance_model.select()

        # Data Training
        list_text_training = []
        list_label_training = []

        instance_model = Models(f'SELECT clean_text, sentiment, user FROM tbl_data_train_q{num}')
        data_train = instance_model.select()

        for i in range(len(data_train)):
            list_text_training.append(data_train[i]['clean_text'])
            list_label_training.append(data_train[i]['sentiment'])

        # Data Testing
        list_text_testing = []
        list_label_testing = []

        instance_model = Models(f'SELECT clean_text, sentiment, user FROM tbl_data_test_q{num}')
        data_test = instance_model.select()
        for i in range(len(data_test)):
            list_text_testing.append(data_test[i]['clean_text'])
            list_label_testing.append(data_test[i]['sentiment'])

        # Vectorize X_train X_test
        vectorizer = CountVectorizer()
        X_train = vectorizer.fit_transform(list_text_training).toarray()
        X_test = vectorizer.transform(list_text_testing).toarray()
        vocab = vectorizer.get_feature_names_out()

        # Vectorize y_train y_test
        labelEncoder = LabelEncoder()
        y_train = labelEncoder.fit_transform(list_label_training).ravel()
        y_test = labelEncoder.transform(list_label_testing).ravel()

        label = labelEncoder.classes_

        # TRAIN MULTINOMIAL NAIVE BAYES
        model = MultiNB()
        model.fit(X_train, y_train)

        # SAVE MODEL as PKL
        filename = f'mnb_model{num}.pkl'
        path = 'website/static/model_data/'
        with open(os.path.join(path, filename), 'wb') as out_name:
            pickle.dump(model, out_name, pickle.HIGHEST_PROTOCOL)

        # EVALUATION
        y_pred = model.predict(X_test)

        # Mengambil hasil prediksi label
        list_label_prediksi = []

        for i in range(len(y_pred)):
            if y_pred[i] == 0:
                list_label_prediksi.append("Kurang Puas")
            elif y_pred[i] == 1:
                list_label_prediksi.append("Puas")
            elif y_pred[i] == 2:
                list_label_prediksi.append("Sangat Puas")

        # Mengambil hasil probabilitas prediksi label
        list_prob_prediksi = []

        predict_prob = model.predict_proba
        for i in range(len(predict_prob)):
            tuple_pred = (round(float(predict_prob[i][0]), 3), round(float(predict_prob[i][1]), 3), round(float(predict_prob[i][2]), 3))
            list_prob_prediksi.append(tuple_pred)
        conf = confusion_matrix(y_test, y_pred)
        print(conf)
        TKurangPuas, FKurangPuas1, FKurangPuas2, FPuas1, TPuas, FPuas2, FSangatPuas1, FSangatPuas2, TSangatPuas = confusion_matrix(y_test, y_pred).ravel()

        akurasi = (TKurangPuas + TPuas + TSangatPuas) / (TKurangPuas + FKurangPuas1 + FKurangPuas2 + TPuas + FPuas1 + FPuas2 + FSangatPuas1 + FSangatPuas2 + TSangatPuas)

        if ((TKurangPuas + FPuas1 + FSangatPuas1) != 0):
            presisi_negatif = TKurangPuas / (TKurangPuas + FPuas1 + FSangatPuas1)
        else: 
            presisi_negatif = 0
        
        if ((TPuas + FKurangPuas1 + FSangatPuas2)):
            presisi_netral = TPuas / (TPuas + FKurangPuas1 + FSangatPuas2)
        else:
            presisi_netral = 0 

        if ((TSangatPuas + FKurangPuas2 + FPuas2) != 0):
            presisi_positif = TSangatPuas / (TSangatPuas + FKurangPuas2 + FPuas2)
        else:
            presisi_positif = 0

        presisi = (presisi_negatif + presisi_netral + presisi_positif) / len(label)

        if ((TKurangPuas + FKurangPuas1 + FKurangPuas1) != 0):
            recall_negatif = TKurangPuas / (TKurangPuas + FKurangPuas1 + FKurangPuas1)
        else:
            recall_negatif = 0

        if ((TPuas + FPuas1 + FPuas2)):
            recall_netral = TPuas / (TPuas + FPuas1 + FPuas2)
        else:
            recall_netral = 0

        if ((TSangatPuas + FSangatPuas1 + FSangatPuas2)):
            recall_positif = TSangatPuas / (TSangatPuas + FSangatPuas1 + FSangatPuas2) 
        else:
            recall_positif = 0

        recall = (recall_negatif + recall_netral + recall_positif) / len(label)

        data_dict = {
            "text_list" : list_text_testing,
            "label_list" : list_label_testing,
            "predict_label" : list_label_prediksi,
            "predict_prob" : list_prob_prediksi,
            "tneg" : int(TKurangPuas),
            "fneg1" : int(FKurangPuas1),
            "fneg2" : int(FKurangPuas2),
            "fnet1" : int(FPuas1),
            "tnet" : int(TPuas),
            "fnet2" : int(FPuas2),
            "fpos1" : int(FSangatPuas1),
            "fpos2" : int(FSangatPuas2),
            "tpos" : int(TSangatPuas),
            "jumlah_kelas": int(len(label)),
            "presisi_negatif" : round(float(presisi_negatif), 2),
            "presisi_netral" : round(float(presisi_netral), 2),
            "presisi_positif" : round(float(presisi_positif), 2),
            "recall_negatif" : round(float(recall_negatif), 2),
            "recall_netral" : round(float(recall_netral), 2),
            "recall_positif" : round(float(recall_positif), 2),
            "akurasi" : round(float(akurasi), 2),
            "presisi" : round(float(presisi), 2),
            "recall" : round(float(recall), 2)
        }

        # Menyimpan hasil evaluasi dalam bentuk json
        with open(os.path.join(path, f'hasil_evaluasi_model{num}.json'), 'w') as outfile:
            json.dump(data_dict, outfile, indent=2)

        flash('Berhasil melakukan klasifikasi data.', 'success')

        return 'true'

    def getEvaluation(self):
        path = 'website/static/model_data/'
        data = {}
        for num in range(1, 6):
            filename = f'hasil_evaluasi_model{num}.json'

            try:
                data[f"eval_{num}"] = json.load(open(path+filename))
            except:
                data = {}

        return data


    def deleteEvalutaion(self):
        filepath = 'website/static/model_data/hasil_evaluasi_model.json'

        if os.path.exists(filepath):
            os.remove(filepath)
            flash('Berhasil menghapus data.', 'success')

        return None