from flask import flash, request
from website.models import Models
from website.excel import Excel

class CrawlingController:

    def select_data_crawling(self):
        instance_model = Models('SELECT * FROM tbl_data_crawling')
        data_crawling = instance_model.select()
        return data_crawling


    def import_crawlingExcel(self):
        excel_file = request.files['excel_file']

        if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
            instance_excel = Excel()
            tuples_excel = instance_excel.make_tuples_crawling(excel_file)

            instance_model = Models('REPLACE INTO tbl_data_crawling(created_at, name, label_1, answer_1, label_2, answer_2, label_3, answer_3, label_4, answer_4, label_5, answer_5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
            instance_model.query_sql_multiple(tuples_excel)
            return None

        flash('Format tidak sesuai! Pastikan file ber-ekstensi .xls atau .xlsx', 'error')
        return None