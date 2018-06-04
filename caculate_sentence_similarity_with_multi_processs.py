import sys
import threading
import multiprocessing
import math

class Similarity:
    def __init__(self):
        self.pool_sentence_num = 0
        self.pool_char_num = 0
        self.pool_list = list()
        self.pool_char_bichar_list = list() #存放pool的每句话的char_bichar
        self.posi_similarity_dict = dict()
        self.posi_poolIndex_dict = dict()
        self.input_char_num = 0
        self.input_sentence_num = 0
        self.input_index_list = list()

    def load_conll_pool_file(self,pool_file_name):
        with open(pool_file_name, "r", encoding="utf-8") as fo:
            char_list = []
            line = fo.readline()
            while line:
                line = line.strip()
                if line:
                    char_list.append(line[0])
                    self.pool_char_num += 1
                else:
                    if char_list != []:
                        sentence = "".join(char_list)
                        sentence_char_bichar_list = list()
                        self.pool_list.append(sentence)
                        self.get_char_and_bichar(sentence, sentence_char_bichar_list)
                        self.pool_char_bichar_list.append(sentence_char_bichar_list)
                        self.pool_sentence_num += 1
                    char_list.clear()
                line = fo.readline()
        print("pool_instance_num:",self.pool_sentence_num)
        print("pool_char_num:", self.pool_char_num)


    def load_input_and_caculate_similarity(self, input_file):
        if self.pool_list == []:
            print("Empty pool!")
            exit()
        with open(input_file, "r", encoding="utf-8") as fo:
            fo.seek(0,0)
            posi = fo.tell()
            line = fo.readline()
            while line:
                line = line.strip()
                if line.startswith("sentence:"):
                    assert posi not in self.posi_similarity_dict and posi not in self.posi_poolIndex_dict
                    self.input_sentence_num += 1
                    sentence = line.lstrip("sentence:").strip()
                    self.input_char_num += len(sentence)
                    self.posi_similarity_dict[posi], self.posi_poolIndex_dict[posi] = self.similarity_degree(sentence)

                posi = fo.tell()
                line = fo.readline()
        print("input_instance_num:", self.input_sentence_num)
        print("input_char_num:", self.input_char_num)

    def load_input_posi(self,input_file):#这边读取sentence的位置，附加统计句子数和字数
        with open(input_file, "r", encoding="utf-8") as fo:
            fo.seek(0,0)
            posi = fo.tell()
            line = fo.readline()
            while line:
                if line.startswith("sentence:"):#只存sentence的posi
                    self.input_index_list.append(posi)
                    self.input_sentence_num += 1
                    sentence = line.lstrip("sentence:").strip()
                    self.input_char_num += len(sentence)

                posi = fo.tell()
                line = fo.readline()
        print("input_instance_num:", self.input_sentence_num)
        print("input_char_num:", self.input_char_num)

    def load_sentences_by_posis_and_caculate_similarity_and_write(self, input_file, posi_list, output_file):
        if self.pool_list == []:
            print("Empty pool!")
            exit()
        with open(input_file, "r", encoding="utf-8") as fo, open(output_file, "w", encoding="utf-8") as fw:
            for posi in posi_list:
                fo.seek(posi,0)
                line = fo.readline()
                assert line.startswith("sentence:")
                sentence = line.lstrip("sentence:").strip()
                posi_similarity, posi_poolIndex = self.similarity_degree(sentence)
                fw.write(str(posi) + "\t" + str(posi_similarity) + "\t" + str(posi_poolIndex) + "\n")





    def caculate_similarity_with_multi_processs_and_threads(self, input_file, num_processs):
        one_posi_group = []
        groups = []
        processs = []
        output_file_list = []
        tasks_in_one_process = math.ceil(self.input_sentence_num / num_processs)


        for i in range(self.input_sentence_num):
            one_posi_group.append(self.input_index_list[i])
            if i % tasks_in_one_process == tasks_in_one_process - 1:
                if one_posi_group != []:
                    groups.append(one_posi_group)
                one_posi_group = []

        if one_posi_group != []:
            groups.append(one_posi_group)


        for i in range(len(groups)):
            each_process = multiprocessing.Process(target=self.load_sentences_by_posis_and_caculate_similarity_and_write, args=(input_file, groups[i], input_file + ".out" + str(i),))
            output_file_list.append(input_file + ".out" + str(i))
            processs.append(each_process)

        for each_process in processs:
            each_process.start()

        for each_process in processs:
            each_process.join()

        for one_out in output_file_list:
            with open(one_out , "r", encoding="utf-8") as fo:
                line = fo.readline()
                while line:
                    if line.strip():
                        [posi,posi_similarity,posi_poolIndex] = line.strip().split()
                        self.posi_poolIndex_dict[int(posi)] = posi_poolIndex
                        self.posi_similarity_dict[int(posi)] = posi_similarity
                    line = fo.readline()




    def get_char_and_bichar(self,sentence, char_bichar_list):
        char_bichar_list.clear()
        for i in range(len(sentence)):
            assert sentence[i] != " "
            char_bichar_list.append(sentence[i])
            if i == 0:
                char_bichar_list.append("#START#" + sentence[i])
            elif i == len(sentence) - 1:
                char_bichar_list.append(sentence[i-1] + sentence[i])
                char_bichar_list.append(sentence[i] + "#END#")
            else:
                char_bichar_list.append(sentence[i-1] + sentence[i])


    def similarity_degree(self,sentence_to_caculate):
        assert self.pool_sentence_num > 0

        input_sentence_char_bichar_list = list()
        one_sentence_in_pool_char_bichar_list = list()

        similarity_index_degree_dict = dict()

        self.get_char_and_bichar(sentence_to_caculate, input_sentence_char_bichar_list)
        input_sentence_num = len(input_sentence_char_bichar_list)

        for i in range(self.pool_sentence_num):
            assert i not in similarity_index_degree_dict
            one_sentence_in_pool_char_bichar_list = self.pool_char_bichar_list[i]
            same_char_bichar = [one for one in input_sentence_char_bichar_list if one in one_sentence_in_pool_char_bichar_list ]
            samll_all_num = min(input_sentence_num, len(one_sentence_in_pool_char_bichar_list))
            similarity_index_degree_dict[i] = len(same_char_bichar) / samll_all_num

        no_sort_tuple = zip(similarity_index_degree_dict.values(), similarity_index_degree_dict.keys())
        sort_tuple = sorted(no_sort_tuple, reverse=True)
        return sort_tuple[0]


    def save_sort_results(self,file_name_input, file_name_out):
        sort_tuple = sorted(zip(self.posi_similarity_dict.values(), self.posi_similarity_dict.keys()),reverse=True)
        with open(file_name_out, "w", encoding="utf-8") as fw, open(file_name_input, "r", encoding="utf-8") as fo:
            for simi_posi in sort_tuple:
                fo.seek(simi_posi[1],0)
                line = fo.readline()
                assert line.startswith("sentence:")
                while line.strip():
                    assert line.startswith("key word:") or line.startswith("sentence:")
                    fw.write(line)
                    line = fo.readline()
                fw.write("\n")



if __name__ == "__main__":
    test = Similarity()
    file_pool = sys.argv[1]
    file_input = sys.argv[2]
    file_out = sys.argv[3]
    # test.load_conll_pool_file("./zhuxian/dev.zhuxian.bichar.feats")
    # # test.load_input_and_caculate_similarity("./zhuxian/dev.simi_test.feats")
    # test.load_input_posi("./zhuxian/dev.simi_test.feats")
    # test.caculate_similarity_with_multi_processs_and_threads("./zhuxian/dev.simi_test.feats", 2)
    # test.save_sort_results("./zhuxian/dev.simi_test.feats", "./zhuxian/similar_to_dev_v5.feats")
    test.load_conll_pool_file(file_pool)
    # test.load_input_and_caculate_similarity("./zhuxian/dev.simi_test.feats")
    test.load_input_posi(file_input)
    test.caculate_similarity_with_multi_processs_and_threads(file_input, 20)
    test.save_sort_results(file_input, file_out)
    # test.load_conll_pool_file(file_input)
    # test.load_input_and_caculate_similarity(file_input)
    # test.save_sort_results(file_input, file_out)








