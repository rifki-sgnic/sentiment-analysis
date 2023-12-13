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
            list_count_sp = []
            list_count_p = []
            list_count_kp = []
            list_persentase_sp = []
            list_persentase_p = []
            list_persentase_kp = []

            for num in range(1, 6):

                instance_model = Models(f'SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_{num} = "Sangat Puas"')
                count_sp = instance_model.select()[0]['jumlah']

                instance_model = Models(f'SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_{num} = "Puas"')
                count_p = instance_model.select()[0]['jumlah']

                instance_model = Models(f'SELECT COUNT(id) as jumlah FROM tbl_data_clean WHERE sentiment_{num} = "Kurang Puas"')
                count_kp = instance_model.select()[0]['jumlah']

                jumlah_data = count_sp + count_p + count_kp
                persentase_sp = round((count_sp / jumlah_data) * 100, 2)
                persentase_p = round((count_p / jumlah_data) * 100, 2)
                persentase_kp = round((count_kp / jumlah_data) * 100, 2)

                list_count_sp.append(count_sp)
                list_count_p.append(count_p)
                list_count_kp.append(count_kp)
                list_persentase_sp.append(persentase_sp)
                list_persentase_p.append(persentase_p)
                list_persentase_kp.append(persentase_kp)

                list_countSentiment = [persentase_sp, persentase_p, persentase_kp]

                plt.subplots(figsize=(10, 10))
                plt.pie(list_countSentiment, labels=['Sangat Puas ('+ str(persentase_sp) +'%)', 'Puas ('+ str(persentase_p) +'%)', 'Kurang Puas ('+ str(persentase_p) +'%)'], colors=['#00c853', '#CACACA', '#ff1744'], startangle=90)
                plt.legend(title="Data Tipe Sentimen")
                plt.savefig(f'website/static/visualisasi/pie_sentimen_{num}.png')

                plt.cla()
                plt.clf()

            instance_model = Models("SELECT clean_answer_5 FROM tbl_data_clean WHERE clean_answer_5 IS NOT NULL AND sentiment_5 = 'Sangat Puas'")
            data_positif = instance_model.select()
                
            instance_model = Models("SELECT clean_answer_5 FROM tbl_data_clean WHERE clean_answer_5 IS NOT NULL AND sentiment_5 = 'Puas'")
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
            if os.path.exists('website/static/visualisasi/pie_sentimen.png'):
                os.remove('website/static/visualisasi/pie_sentimen.png')
            else:
                print('\nFile piechart tidak ditemukan')
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
            'jumlah_sp': list_count_sp,
            'jumlah_p': list_count_p,
            'jumlah_kp': list_count_kp,
            'persentase_sp': list_persentase_sp,
            'persentase_p': list_persentase_p,
            'persentase_kp': list_persentase_kp,
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