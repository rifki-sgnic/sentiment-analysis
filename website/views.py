import json
from urllib import response
from flask import Blueprint, jsonify, render_template, request, flash, redirect, url_for
from website.controllers.crawling import CrawlingController

from website.controllers.dashboard import DashboardController
from website.controllers.kamus import KamusController
from website.controllers.labeling import LabelingController
from website.controllers.classification import ClassificationController
from website.controllers.preprocessing import PreprocessingController
from website.controllers.splitting import SplittingController
from website.controllers.visualization import VisualizationController

views = Blueprint('views', __name__)

# DASHBOARD

controller_dashboard = DashboardController()
@views.route('/', methods=['GET'])
def dashboard():
    data = controller_dashboard.getData()
    return render_template("dashboard.html", data=data)

# KAMUS
controller_kamus = KamusController()
@views.route('/kamus', methods=['GET'])
def kamus():
    return render_template("kamus.html")

## Slangword
@views.route('/kamus/list-slangword', methods=['GET'])
def list_slangword():
    slangword = controller_kamus.select_dataSlangword()
    return { 'data' : slangword }

@views.route('/kamus/slangword/tambah', methods=['POST'])
def tambah_slangword():
    controller_kamus.add_dataSlangword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/slangword/import', methods=['POST'])
def import_data_slangword():
    controller_kamus.import_dataSlangword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/slangword/ubah', methods=['POST'])
def ubah_slangword():
    controller_kamus.update_dataSlangword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/slangword/hapus', methods=['POST'])
def hapus_slangword():
    controller_kamus.delete_dataSlangword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/slangword/hapus-all', methods=['POST'])
def hapus_all_slangword():
    controller_kamus.delete_allDataSlangword()
    return redirect(url_for('views.kamus'))

# Stopword
@views.route('/kamus/list-stopword', methods=['GET'])
def list_stopword():
    stopword = controller_kamus.select_dataStopword()
    return { 'data' : stopword }

@views.route('/kamus/stopword/tambah', methods=['POST'])
def tambah_stopword():
    controller_kamus.add_dataStopword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/stopword/import', methods=['POST'])
def import_data_stopword():
    controller_kamus.import_dataStopword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/stopword/ubah', methods=['POST'])
def ubah_stopword():
    controller_kamus.update_dataStopword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/stopword/hapus', methods=['POST'])
def hapus_stopword():
    controller_kamus.delete_dataStopword()
    return redirect(url_for('views.kamus'))

@views.route('/kamus/stopword/hapus-all', methods=['POST'])
def hapus_all_stopword():
    controller_kamus.delete_allDataStopword()
    return redirect(url_for('views.kamus'))


# CRAWLING
controller_crawling = CrawlingController()

@views.route('/crawling', methods=['GET'])
def crawling():
    data_crawling = controller_crawling.select_data_crawling()
    return render_template("crawling.html", data=data_crawling)

@views.route('/import-crawling', methods=['POST'])
def import_crawling():
    controller_crawling.import_crawlingExcel()
    return redirect(url_for('views.crawling'))


# PREPROCESSING
controller_preprocessing = PreprocessingController()

@views.route('/preprocessing', methods=['GET','POST'])
def preprocessing():
    if request.method == 'GET':
        count_data_crawling = controller_preprocessing.count_dataCrawling()
        return render_template("preprocessing.html", count_data_crawling=count_data_crawling)

    if request.method == 'POST':
        response = controller_preprocessing.add_dataPreprocessing()
        return response

@views.route('/list-data-preprocessing', methods=['GET'])
def list_data_preprocessing():
    data_preprocessing = controller_preprocessing.select_dataPreprocessing()
    return { 'data' : data_preprocessing }

# LABELING
controller_labeling = LabelingController()

@views.route('/labeling', methods=['GET','POST'])
def labeling():
    if request.method == 'GET':
        count_data_with_label = controller_labeling.count_dataWithLabel()
        return render_template("labeling.html", count_data_with_label=count_data_with_label)
    
    if request.method == 'POST':
        response = controller_labeling.add_dataLabeling()
        return response

@views.route('/list-data-with-label', methods=['GET'])
def list_data_with_label():
    data_with_label = controller_labeling.select_dataWithLabel()
    return { 'data' : data_with_label }

@views.route('/list-data-no-label', methods=['GET'])
def list_data_no_label():
    data_no_label = controller_labeling.select_dataNoLabel()
    return { 'data' : data_no_label }

@views.route('/labeling/hapus-all', methods=['POST'])
def hapus_all_label():
    controller_labeling.delete_dataLabeling()
    return redirect(url_for('views.labeling'))


# SPLITTING DATA
controller_splitting = SplittingController()

@views.route('/split', methods=['GET', 'POST'])
def split():
    if request.method == 'GET':
        count_data_with_label = controller_splitting.count_dataWithLabel()
        count_data_with_label_pos = controller_splitting.count_dataWithLabelPos()
        count_data_with_label_neg = controller_splitting.count_dataWithLabelNeg()

        count_data_q1_label = controller_splitting.count_dataQ1WithLabel()
        count_data_q2_label = controller_splitting.count_dataQ2WithLabel()
        count_data_q3_label = controller_splitting.count_dataQ3WithLabel()
        count_data_q4_label = controller_splitting.count_dataQ4WithLabel()
        count_data_q5_label = controller_splitting.count_dataQ5WithLabel()

        if count_data_with_label_pos != 0:
            percentage_pos = round((count_data_with_label_pos / count_data_with_label) * 100)
        else:
            percentage_pos = 0

        if count_data_with_label_neg != 0:
            percentage_neg = round((count_data_with_label_neg / count_data_with_label) * 100)
        else:
            percentage_neg = 0

        return render_template("splitting.html", count_data_with_label=count_data_with_label, 
        count_data_with_label_pos=count_data_with_label_pos, 
        count_data_with_label_neg=count_data_with_label_neg,
        count_data_q1_label=count_data_q1_label,
        count_data_q2_label=count_data_q2_label,
        count_data_q3_label=count_data_q3_label,
        count_data_q4_label=count_data_q4_label,
        count_data_q5_label=count_data_q5_label,
        percentage_pos=percentage_pos,
        percentage_neg=percentage_neg)
    
    if request.method == 'POST':
        response = controller_splitting.add_dataSplit()
        return response

@views.route('/split/list-data-train-q1', methods=['GET'])
def list_data_train_q1():
    data_train = controller_splitting.select_dataTrainQ1()
    return { 'data' : data_train }

@views.route('/split/list-data-test-q1', methods=['GET'])
def list_data_test_q1():
    data_test = controller_splitting.select_dataTestQ1()
    return { 'data' : data_test }

@views.route('/split/list-data-train-q2', methods=['GET'])
def list_data_train_q2():
    data_train = controller_splitting.select_dataTrainQ2()
    return { 'data' : data_train }

@views.route('/split/list-data-test-q2', methods=['GET'])
def list_data_test_q2():
    data_test = controller_splitting.select_dataTestQ2()
    return { 'data' : data_test }

@views.route('/split/list-data-train-q3', methods=['GET'])
def list_data_train_q3():
    data_train = controller_splitting.select_dataTrainQ3()
    return { 'data' : data_train }

@views.route('/split/list-data-test-q3', methods=['GET'])
def list_data_test_q3():
    data_test = controller_splitting.select_dataTestQ3()
    return { 'data' : data_test }

@views.route('/split/list-data-train-q4', methods=['GET'])
def list_data_train_q4():
    data_train = controller_splitting.select_dataTrainQ4()
    return { 'data' : data_train }

@views.route('/split/list-data-test-q4', methods=['GET'])
def list_data_test_q4():
    data_test = controller_splitting.select_dataTestQ4()
    return { 'data' : data_test }

@views.route('/split/list-data-train-q5', methods=['GET'])
def list_data_train_q5():
    data_train = controller_splitting.select_dataTrainQ5()
    return { 'data' : data_train }

@views.route('/split/list-data-test-q5', methods=['GET'])
def list_data_test_q5():
    data_test = controller_splitting.select_dataTestQ5()
    return { 'data' : data_test }

@views.route('/split/hapus', methods=['POST'])
def hapus_dataSplit():
    controller_splitting.delete_allDataSplit()
    return redirect(url_for('views.split'))

# CLASSIFICATION
controller_classification = ClassificationController()
@views.route('/classification', methods=['GET','POST'])
def classification():
    if request.method == 'GET':
        data_eval = controller_classification.getEvaluation()
        return render_template("classification.html", data_eval=data_eval)

    if request.method == 'POST':
        for num in range(1, 6):
            controller_classification.createModel(num)
        return controller_classification.createModel(1)

@views.route('/classification/hapus-data', methods=['POST'])
def hapus_evaluation():
    controller_classification.deleteEvalutaion()
    return redirect(url_for('views.classification'))

# VISUALISASI
controller_visualisasi = VisualizationController()
@views.route('/visualization', methods=['GET', 'POST'])
def visualization():
    if request.method == 'GET':
        data = controller_visualisasi.getVisualisasi()
        return render_template('visualization.html', data=data)
    
    if request.method == 'POST':
        response = controller_visualisasi.createVisualisasi()
        return response

@views.route('/visualization/hapus-data', methods=['POST'])
def hapus_visualization():
    controller_visualisasi.deleteVisualisasi()
    return redirect(url_for('views.visualization'))