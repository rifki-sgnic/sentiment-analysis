import json

from flask import flash
from website.models import Models
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import operator
import os


class VisualizationController:
    def createVisualisasi(self):
        try:
            list_count_p = []
            list_count_c = []
            list_count_tp = []
            list_persentase_p = []
            list_persentase_c = []
            list_persentase_tp = []

            for num in range(1, 6):

                instance_model = Models(f'SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_{num} = "Puas"')
                count_p = instance_model.select()[0]['jumlah']

                instance_model = Models(f'SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_{num} = "Cukup"')
                count_c = instance_model.select()[0]['jumlah']

                instance_model = Models(f'SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_{num} = "Tidak Puas"')
                count_tp = instance_model.select()[0]['jumlah']

                jumlah_data = count_p + count_c + count_tp
                persentase_p = round((count_p / jumlah_data) * 100, 2)
                persentase_c = round((count_c / jumlah_data) * 100, 2)
                persentase_tp = round((count_tp / jumlah_data) * 100, 2)

                list_count_p.append(count_p)
                list_count_c.append(count_c)
                list_count_tp.append(count_tp)
                list_persentase_p.append(persentase_p)
                list_persentase_c.append(persentase_c)
                list_persentase_tp.append(persentase_tp)

                list_countSentiment = [persentase_p, persentase_c, persentase_tp]
                list_label = ["Puas", "Cukup Puas", "Tidak Puas"]

                plt.subplots(figsize=(10, 10))
                # plt.pie(list_countSentiment, labels=['Puas ('+ str(persentase_p) +'%)', 'Cukup ('+ str(persentase_c) +'%)', 'Tidak Puas ('+ str(persentase_tp) +'%)'], colors=['#00c853', '#CACACA', '#ff1744'], startangle=90)
                plt.bar(list_label, list_countSentiment, color=['#00c853', '#CACACA', '#ff1744'])
                plt.legend(title="Data Tipe Sentimen")
                plt.savefig(f'website/static/visualisasi/bar_sentimen_{num}.png')

                plt.cla()
                plt.clf()

            instance_model = Models("SELECT clean_answer_5 FROM tbl_data_clean WHERE clean_answer_5 IS NOT NULL AND sentiment_5 = 'Puas'")
            data_positif = instance_model.select()
                
            instance_model = Models("SELECT clean_answer_5 FROM tbl_data_clean WHERE clean_answer_5 IS NOT NULL AND sentiment_5 = 'Tidak Puas'")
            data_negatif = instance_model.select()

            string_positif = ""
            for data in data_positif:
                string_positif += str(data['clean_answer_5']) + " "
                
            string_negatif = ""
            for data in data_negatif:
                string_negatif += str(data['clean_answer_5']) + " "

            wordcloud = WordCloud(width=800, height=400, background_color='black', collocations=False).generate(string_positif)
            wordcloud.to_file('website/static/visualisasi/wordcloud_positif.png')

            wordcloud = WordCloud(width=800, height=400, background_color='black', collocations=False).generate(string_negatif)
            wordcloud.to_file('website/static/visualisasi/wordcloud_negatif.png')

        except:
            if os.path.exists('website/static/visualisasi/histogram_dist_waktu.png'):
                os.remove('website/static/visualisasi/histogram_dist_waktu.png')
            else:
                print('\nFile histogram tidak ditemukan')
            if os.path.exists('website/static/visualisasi/bar_sentimen.png'):
                os.remove('website/static/visualisasi/bar_sentimen.png')
            else:
                print('\nFile bar chart tidak ditemukan')
            return {'error': 'Terjadi Kesalahan'}

        counts = {}
        for word in string_positif.split():
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        frekuensi_pos = dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True))
        
        for word in string_negatif.split():
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        frekuensi_neg = dict(sorted(counts.items(), key=operator.itemgetter(1), reverse=True))

        data = {
            'jumlah_tweets': jumlah_data,
            'jumlah_p': list_count_p,
            'jumlah_c': list_count_c,
            'jumlah_tp': list_count_tp,
            'persentase_p': list_persentase_p,
            'persentase_c': list_persentase_c,
            'persentase_tp': list_persentase_tp,
            'frekuensi_pos': list(frekuensi_pos.items())[:15],
            'frekuensi_neg': list(frekuensi_neg.items())[:15],
        }

        # Menyimpan hasil visualisasi dalam bentuk json
        with open(os.path.join('website/static/visualisasi/', 'hasil_visualisasi.json'), 'w') as outfile:
            json.dump(data, outfile, indent=2)

        return 'true'

    def getVisualisasi(self):
        filepath = 'website/static/visualisasi/hasil_visualisasi.json'

        try:
            data = json.load(open(filepath))
        except:
            data = None
        
        return data


    def deleteVisualisasi(self):
        filepath = 'website/static/visualisasi/hasil_visualisasi.json'

        if os.path.exists(filepath):
            os.remove(filepath)
            flash('Berhasil menghapus data.', 'success')

        return None