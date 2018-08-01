import sys
import threading
import multiprocessing
import os
import time
import math
from config import config_dict



class Segment:
    def __init__(self, pool_file, compare_file, train_file):
        self.pool_text = ""
        self.pool_file = pool_file

        self.train_file = train_file
        self.train_file_words = set() #存储训练文件里面已有的词语，用来过滤百科弱标注数据
        self.train_file_chars = set() #存储训练纹面已有的汉字，用来过滤百科弱标注数据

        self.compare_file = compare_file
        self.compare_posi_list = list()
        self.compare_posi_sentence = dict()
        self.compare_posi_key_words = dict()


    def load_conll_pool(self):
        print("Pool file:", self.pool_file, end="\t")
        print("Start loading pool file:", time.asctime( time.localtime(time.time()) ))
        self.pool_text += "&"
        with open(self.pool_file, "r", encoding="utf-8") as fo:
            line = fo.readline()
            while line:
                line_strip = line.strip()
                if line_strip:
                    self.pool_text += line_strip[0]
                else:
                    self.pool_text += "&"
                line = fo.readline()
        if not self.pool_text.endswith("&"):
            self.pool_text += "&"

        print("Finish loading pool file:", time.asctime(time.localtime(time.time())))
        print()

    def load_conll_train_words(self):
        list_words = []
        list_chars = []
        cur_word = ""
        print()
        print("Start loading train file!")
        with open(self.train_file, "r", encoding="utf-8") as fo:
            line = fo.readline()
            while line:
                line = line.strip()
                if line:
                    list_chars.append(line[0])
                    if line.endswith("s-seg"):
                        assert cur_word == ""
                    elif line.endswith("b-seg"):
                        assert cur_word == ""
                        cur_word += line[0]
                    elif line.endswith("m-seg"):
                        assert cur_word != ""
                        cur_word += line[0]
                    else:
                        cur_word += line[0]
                        list_words.append(cur_word)
                        cur_word = ""
                line = fo.readline()
        self.train_file_words = set(list_words)
        self.train_file_chars = set(list_chars)
        print("Finish loading train file and total {0} words and {1} chars in it!".format(len(self.train_file_words),len(self.train_file_chars)))
        print()


    def load_compare_file_posi(self):
        print("Compare file:", self.compare_file)
        print("Start loading compare file:", time.strftime("%m %d %Y %H:%M:%S", time.gmtime(time.time())))
        with open(self.compare_file, "r", encoding="utf-8") as fo:
            sentence = ""
            key_words_list = []
            cur_posi = fo.tell()
            line = fo.readline()
            while line:
                line_strip = line.strip()
                if line_strip:
                    if line_strip.startswith("Num same bichar:") or line_strip.startswith("Num same char:") or line_strip.startswith("SimilarToZX:") or line_strip.startswith("SimilarIndexInZX:") or line_strip.startswith("PercentInfo:"):
                        cur_posi = fo.tell()
                        line = fo.readline()

                        continue
                    elif line_strip.startswith("sentence:"):
                        sentence_posi = cur_posi
                        sentence = line_strip.lstrip("sentence:").strip()
                    else:
                        assert line_strip.startswith("key word:")
                        cur_word = line_strip.lstrip("key word:").strip()
                        if cur_word not in key_words_list and len(cur_word) > 1:
                            key_words_list.append(cur_word)
                else:
                    if sentence != "":
                        self.compare_posi_list.append(sentence_posi)
                        # self.compare_posi_sentence[sentence_posi] = sentence
                        # self.compare_posi_key_words[sentence_posi] = list(set(key_words_list))
                        sentence = ""
                        key_words_list = []
                cur_posi = fo.tell()
                line = fo.readline()


        if sentence != "":
            self.compare_posi_list.append(sentence_posi)
            # self.compare_posi_sentence[sentence_posi] = sentence
            # self.compare_posi_key_words[sentence_posi] = list(set(key_words_list))
            sentence = ""
            key_words_list = []

        print("Finish loading compare file:", time.strftime("%m %d %Y %H:%M:%S", time.gmtime(time.time())))
        print()

    def get_num_same_segment_with_multi_processs(self, num_processs, output_file):

        processs = list()
        tmp_output_file_list = list()

        sentences_in_one_process = math.ceil(len(self.compare_posi_list) / num_processs) #取上届
        groups = [self.compare_posi_list[i:i + sentences_in_one_process] for i in range(0, len(self.compare_posi_list), sentences_in_one_process)]

        for i in range(len(groups)):
            each_process = multiprocessing.Process(target=self.load_sentences_by_posis_and_caculate_similarity_and_write, args=(groups[i], "./random.tmp" + str(i),))
            tmp_output_file_list.append("./random.tmp"+ str(i))
            # print(tmp_output_file_list)
            processs.append(each_process)

        for each_process in processs:
            each_process.start()

        for each_process in processs:
            each_process.join()

        self.combine_tmp_file_and_delete_to_output(tmp_output_file_list, output_file)


    def combine_tmp_file_and_delete_to_output(self, list_file, output_file):
        with open( output_file, "w", encoding="utf-8") as fw:
            print("Start write file:", output_file)
            for each_file in list_file:
                print("Start copying file:", each_file)
                with open(each_file, "r", encoding="utf-8") as fo:
                    line = fo.readline()
                    while line:
                        fw.write(line)
                        line = fo.readline()

                os.remove(each_file)
                print("Finish copy file and delete ", each_file)
                print()

        print("Finish combining file!")
        print()



    def load_sentences_by_posis_and_caculate_similarity_and_write(self, list_groups, tmp_file):
        with open(tmp_file, "w", encoding="utf-8") as fw, open(self.compare_file, "r", encoding="utf-8") as fo:
            for each_posi in list_groups:
                # print(each_posi)
                char_in_pa_with_tag_list = list()
                fo.seek(each_posi)
                line = fo.readline()
                sentence = ""
                key_word_list = []
                while line.strip():
                    # print(line)
                    if line.startswith("sentence:"):
                        sentence = line.strip().lstrip("sentence:").strip()
                    elif line.startswith("key word:"):
                        key_word_list.append(line.strip().lstrip("key word:").strip())
                    line = fo.readline()

                num_same_bichar = 0
                key_word_to_write = []

                for one_key_word in key_word_list:
                    char_in_pa_with_tag_list.append(one_key_word[0])
                    char_in_pa_with_tag_list.append(one_key_word[-1])

                char_in_pa_with_tag_set = set(char_in_pa_with_tag_list)
                all_char_in_pa_set = set([char for char in sentence])

                if len(all_char_in_pa_set - char_in_pa_with_tag_set - self.train_file_chars) > 0:
                    continue #如果包含无标签的字，那么直接跳过

                for one_key_word in key_word_list:
                    if one_key_word not in self.train_file_words:
                        key_word_to_write.append(one_key_word)


                if num_same_bichar >= 0 and len(key_word_to_write) > 0:
                    fw.write("sentence:\t" + sentence + "\n")
                    for key_word in key_word_to_write:
                        fw.write("key word:\t" + key_word + "\n")
                    fw.write("Num same bichar:\t" + str(num_same_bichar) + "\n")
                    fw.write("\n")


    def extract_and_sort_bichar_frequency_more_than_zero(self, input_file,file_out):
        sentence_posi_info = dict()
        sentence_posi_bichar_frequency = dict()
        num_frequency_more_than_zero = 0
        print("Start loading char bichar file:", time.strftime("%m %d %Y %H:%M:%S", time.gmtime(time.time())))
        with open(input_file, "r", encoding="utf-8") as fo:
            info_list = list()
            posi = fo.tell()
            line = fo.readline()
            while line:
                line_strip = line.strip()
                if line_strip:
                    info_list.append(line_strip)
                    if line_strip.startswith("sentence:"):
                        assert len(info_list) == 1
                        sentence_posi = posi
                    elif line_strip.startswith("Num same bichar:"):
                        num_same_bichar = line_strip.lstrip("Num same bichar:").strip()
                else:
                    if info_list != []:
                        if int(num_same_bichar) > 0:
                            num_frequency_more_than_zero += 1
                            sentence_posi_info[sentence_posi] = info_list
                            sentence_posi_bichar_frequency[sentence_posi] = num_same_bichar
                            for one in info_list:
                                if one.startswith("Num same bichar:"):
                                    assert num_same_bichar == one.lstrip("Num same bichar:").strip()

                        info_list = []

                posi = fo.tell()
                line = fo.readline()

            if info_list != []:
                if int(num_same_bichar) > 0:
                    sentence_posi_info[sentence_posi] = info_list
                    sentence_posi_bichar_frequency[sentence_posi] = num_same_bichar
                    for one in info_list:
                        if one.startswith("Num same bichar:"):
                            assert num_same_bichar == one.lstrip("Num same bichar:").strip()

                info_list = []

        print("Finish loading char bichar file:", time.strftime("%m %d %Y %H:%M:%S", time.gmtime(time.time())))
        print()
        print("Start sort char bichar file by bichar frequency:", time.strftime("%m %d %Y %H:%M:%S", time.gmtime(time.time())))
        no_sort_tuple = zip(sentence_posi_bichar_frequency.values(), sentence_posi_bichar_frequency.keys())
        sort_tuple = sorted(no_sort_tuple, reverse=True)
        print("Finish sort char bichar file by bichar frequency:",time.strftime("%m %d %Y %H:%M:%S", time.gmtime(time.time())))
        print()
        print("Start save sort results:",time.strftime("%m %d %Y %H:%M:%S", time.gmtime(time.time())))
        with open(file_out, "w", encoding="utf-8") as fw:
            for each_tuple in sort_tuple:
                each_info_list = sentence_posi_info[each_tuple[-1]]
                for one in each_info_list:
                    fw.write(one + "\n")
                fw.write("\n")
        print("Finish save sort results:", time.strftime("%m %d %Y %H:%M:%S", time.gmtime(time.time())))
        print()

        print("Count of frequency more than zero:",num_frequency_more_than_zero)


    def remove_same_bichar_frequency(self, input_file, output_file):
        sentence_info_dict = dict()
        sentence_bichar_num_dict = dict()
        with open(input_file, "r", encoding="utf-8") as fo:
            sentence = ""
            key_word_list = list()
            info_list = list()
            num_bichar = 0

            line = fo.readline()
            while line:
                line_strip = line.strip()
                if line_strip:
                    info_list.append(line_strip)
                    if line_strip.startswith("sentence:"):
                        assert sentence == ""
                        sentence = line_strip.lstrip("sentence:").strip()
                    elif line_strip.startswith("key word:"):
                        key_word_list.append(line_strip.lstrip("key word:").strip())
                    elif line_strip.startswith("Num same bichar:"):
                        assert num_bichar == 0
                        num_bichar = int(line_strip.lstrip("Num same bichar:").strip())
                else:
                    if info_list != []:
                        assert sentence != "" and key_word_list != []
                        for one_key_word in key_word_list:
                            sentence = sentence.replace(one_key_word, " "+one_key_word+" ")
                        sentence_bichar_num_dict[sentence] = num_bichar
                        sentence_info_dict[sentence] = info_list
                    info_list = []
                    key_word_list = []
                    sentence = ""
                    num_bichar = 0

                line = fo.readline()

        no_sort_tuple = zip(sentence_bichar_num_dict.values(), sentence_bichar_num_dict.keys())
        sort_tuple = sorted(no_sort_tuple, reverse=True)

        with open(output_file, "w" ,encoding="utf-8") as fw:
            for one_tuple in sort_tuple:
                info_list = sentence_info_dict[one_tuple[-1]]
                for one in info_list:
                    fw.write(one + "\n")
                fw.write("\n")

        print("共计：",len(sort_tuple))


    def get_finst_n_sentence(self, input_file, output_file, n):
        cur_num = 0
        with open(input_file, "r", encoding="utf-8") as fo, open(output_file, "w", encoding="utf-8") as fw:
            info_list = []
            sentence = ""

            line = fo.readline()
            while line:
                line_strip = line.strip()
                if line_strip:
                    info_list.append(line_strip)
                    if line_strip.startswith("sentence:"):
                        assert sentence == ""
                        sentence = line_strip.lstrip("sentence:").strip()
                else:
                    if info_list != []:
                        if " " not in sentence and cur_num < n:
                            cur_num += 1
                            for one in info_list:
                                fw.write(one + "\n")
                            fw.write("\n")

                    info_list = []
                    sentence = ""
                line = fo.readline()
            if info_list != []:
                if " " not in sentence and cur_num < n:
                    cur_num += 1
                    for one in info_list:
                        fw.write(one + "\n")
                    fw.write("\n")



if __name__ == "__main__":
    file_pool = config_dict["file_pool"]
    file_compare = config_dict["file_compare"]
    file_train = config_dict["file_train"]
    file_compare_output = config_dict["file_compare_output"]
    file_more_zero = file_compare_output + ".morezero"
    file_remove = file_more_zero + ".remove"
    num_process = config_dict["num_process"]
    num_sample = 500000
    file_first_n = file_remove + ".first" + str(num_sample)

    test = Segment(file_pool, file_compare, file_train)
    test.load_conll_pool()
    test.load_compare_file_posi()
    test.load_conll_train_words()
    test.get_num_same_segment_with_multi_processs(num_process, file_compare_output)
    # test.extract_and_sort_bichar_frequency_more_than_zero(file_compare_output, file_more_zero)
    test.remove_same_bichar_frequency(file_compare_output, file_remove)
    test.get_finst_n_sentence(file_remove, file_first_n, num_sample)