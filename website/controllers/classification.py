from math import nan
from sklearn.calibration import LabelEncoder
from sklearn.metrics import confusion_matrix
from website.models import Models
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB
from flask import flash, json, request
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

        mdl = request.form["model"]
        print(mdl)

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
        if mdl == "mnb" :
            model = MultiNB()
        else :
            model = GaussianNB()

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
                list_label_prediksi.append("Tidak Puas")
            elif y_pred[i] == 1:
                list_label_prediksi.append("Cukup")
            elif y_pred[i] == 2:
                list_label_prediksi.append("Puas")

        # Mengambil hasil probabilitas prediksi label
        list_prob_prediksi = []

        if mdl == "mnb":
            predict_prob = model.predict_proba
        else:
            predict_prob = model.predict_proba(X_train)

        for i in range(len(predict_prob)):
            tuple_pred = (round(float(predict_prob[i][0]), 3), round(float(predict_prob[i][1]), 3), round(float(predict_prob[i][2]), 3))
            list_prob_prediksi.append(tuple_pred)

        conf = confusion_matrix(y_test, y_pred)
        print(conf)
        TTidakPuas, FTidakPuas1, FTidakPuas2, FCukup1, TCukup, FCukup2, FPuas1, FPuas2, TPuas = confusion_matrix(y_test, y_pred).ravel()

        akurasi = (TTidakPuas + TCukup + TPuas) / (TTidakPuas + FTidakPuas1 + FTidakPuas2 + TCukup + FCukup1 + FCukup2 + FPuas1 + FPuas2 + TPuas)

        if ((TTidakPuas + FCukup1 + FPuas1) != 0):
            presisi_negatif = TTidakPuas / (TTidakPuas + FCukup1 + FPuas1)
        else: 
            presisi_negatif = 0
        
        if ((TCukup + FTidakPuas1 + FPuas2)):
            presisi_netral = TCukup / (TCukup + FTidakPuas1 + FPuas2)
        else:
            presisi_netral = 0 

        if ((TPuas + FTidakPuas2 + FCukup2) != 0):
            presisi_positif = TPuas / (TPuas + FTidakPuas2 + FCukup2)
        else:
            presisi_positif = 0

        presisi = (presisi_negatif + presisi_netral + presisi_positif) / len(label)

        if ((TTidakPuas + FTidakPuas1 + FTidakPuas1) != 0):
            recall_negatif = TTidakPuas / (TTidakPuas + FTidakPuas1 + FTidakPuas1)
        else:
            recall_negatif = 0

        if ((TCukup + FCukup1 + FCukup2)):
            recall_netral = TCukup / (TCukup + FCukup1 + FCukup2)
        else:
            recall_netral = 0

        if ((TPuas + FPuas1 + FPuas2)):
            recall_positif = TPuas / (TPuas + FPuas1 + FPuas2) 
        else:
            recall_positif = 0

        recall = (recall_negatif + recall_netral + recall_positif) / len(label)

        data_dict = {
            "text_list" : list_text_testing,
            "label_list" : list_label_testing,
            "predict_label" : list_label_prediksi,
            "predict_prob" : list_prob_prediksi,
            "tneg" : int(TTidakPuas),
            "fneg1" : int(FTidakPuas1),
            "fneg2" : int(FTidakPuas2),
            "fnet1" : int(FCukup1),
            "tnet" : int(TCukup),
            "fnet2" : int(FCukup2),
            "fpos1" : int(FPuas1),
            "fpos2" : int(FPuas2),
            "tpos" : int(TPuas),
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