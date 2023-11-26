from flask import request, json
from website.models import Models
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class PreprocessingController:
    def select_dataPreprocessing(self):
        instance_model = Models("SELECT * FROM tbl_data_clean")
        data_preprocessing = instance_model.select()
        return data_preprocessing

    def add_dataPreprocessing(self):
        aksi = request.form["aksi"]

        if aksi == "preprocessing":
            instance_model = Models("SELECT * FROM tbl_data_crawling")
            data_preprocess = instance_model.select()

            first_data = []
            last_data = []
            casefolding = []
            remove_non_char = []
            remove_stopword = []
            change_slangword = []
            change_stemming = []

            save_data = []

            instance_model = Models("SELECT * FROM tbl_slangword")
            slangwords = instance_model.select()

            instance_model = Models("SELECT * FROM tbl_stopword")
            stopwords = instance_model.select()

            instance_stemming = StemmerFactory()
            stemmer = instance_stemming.create_stemmer()

            print("-- Proses " + str(len(data_preprocess)) + " Data --")

            for index, data in enumerate(data_preprocess):
                list_answer = [
                    data["answer_1"],
                    data["answer_2"],
                    data["answer_3"],
                    data["answer_4"],
                    data["answer_5"],
                ]
                
                first_data.append(list_answer)

                clean_text = []
                for index, first in enumerate(first_data):
                    temp = []
                    temp_casefold = []
                    temp_remove_non_char = []
                    temp_slangword = []
                    temp_stopword = []
                    temp_stemming = []

                    for text in first:
                        result_text = text.lower()
                        temp_casefold.append(result_text)

                        result_text = re.sub(r"http\S+|@\S+|#\S+|\d+", "", text)  # Remove mentions, hashtags, links, and numbers
                        # result_text = re.sub(r"[^a-z ]", " ", result_text)  # Replace non-letter characters with spaces
                        result_text = result_text.strip()  # Remove trailing and leading spaces
                        result_text = re.sub("\s+", " ", result_text)  # Remove excessive spaces between words
                        temp_remove_non_char.append(result_text)
                        
                        # Change slangwords
                        for slang in slangwords:
                            if slang["slangword"] in result_text:
                                result_text = re.sub(
                                    r"\b{}\b".format(slang["slangword"]),
                                    slang["kata_asli"],
                                    result_text,
                                )
                        temp_slangword.append(result_text)
                        
                        # Remove stopwords
                        for stop in stopwords:
                            if stop["stopword"] in result_text:
                                result_text = re.sub(
                                    r"\b{}\b".format(stop["stopword"]), "", result_text
                                )
                        temp_stopword.append(result_text)
                        
                        # Stemming
                        result_text = stemmer.stem(result_text)
                        temp_stemming.append(result_text)
                        

                        temp.append(result_text)

                    casefolding.append(temp_casefold)
                    remove_non_char.append(temp_remove_non_char)
                    change_slangword.append(temp_slangword)
                    remove_stopword.append(temp_stopword)
                    change_stemming.append(temp_stemming)
                    clean_text.append(temp)
                    last_data = clean_text

                    if len(clean_text) != 0:
                        try:
                            save_data.append(
                                (
                                    data["id"],
                                    data["answer_1"],
                                    clean_text[index][0],
                                    data["label_1"],
                                    data["answer_2"],
                                    clean_text[index][1],
                                    data["label_2"],
                                    data["answer_3"],
                                    clean_text[index][2],
                                    data["label_3"],
                                    data["answer_4"],
                                    clean_text[index][3],
                                    data["label_4"],
                                    data["answer_5"],
                                    clean_text[index][4],
                                    data["label_5"],
                                    data["name"],
                                    data["created_at"],
                                )
                            )
                        except:
                            print(
                                "\nGagal Menyimpan Data (ID: " + str(data["id"]) + ")\n"
                            )
                    else:
                        print("\nGagal Menyimpan Data (ID: " + str(data["id"]) + ")\n")

                print("Data ke-" + str(index + 1))

            instance_model = Models(
                "REPLACE INTO tbl_data_clean(id, answer_1, clean_answer_1, sentiment_1, answer_2, clean_answer_2, sentiment_2, answer_3, clean_answer_3, sentiment_3, answer_4, clean_answer_4, sentiment_4, answer_5, clean_answer_5, sentiment_5, name, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            instance_model.query_sql_multiple(save_data)
            print("\n -- SELESAI -- ")

        return json.dumps(
            {
                "first_data": first_data,
                "casefolding": casefolding,
                "remove_non_char": remove_non_char,
                "change_slangword": change_slangword,
                "remove_stopword": remove_stopword,
                "change_stemming": change_stemming,
                "last_data": last_data,
            }
        )

    def count_dataCrawling(self):
        instance_model = Models("SELECT COUNT(id) as jumlah FROM tbl_data_crawling")
        data_crawling = instance_model.select()
        return data_crawling[0]["jumlah"]

    def delete_allDataPreprocess():
        instance_model = Models("DELETE FROM tbl_data_clean WHERE sentiment IS NULL")
        instance_model.query_delete_all()
        return None
