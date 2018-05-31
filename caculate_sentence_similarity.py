import sys

class Similarity:
    def __init__(self):
        self.pool_sentence_num = 0
        self.pool_char_num = 0
        self.input_char_num = 0
        self.input_sentence_num = 0
        self.pool_list = list()
        self.posi_similarity_dict = dict()
        self.posi_poolIndex_dict = dict()

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
                        self.pool_list.append("".join(char_list))
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
                    # print(self.posi_similarity_dict)
                    # print(self.posi_poolIndex_dict)


                posi = fo.tell()
                line = fo.readline()
        print("input_instance_num:", self.input_sentence_num)
        print("input_char_num:", self.input_char_num)

    def get_char_and_bichar(self,sentence, char_bichar_list):
        char_bichar_list.clear()
        for i in range(len(sentence)):
            assert sentence[i] != " "
            char_bichar_list.append(sentence[i])
            if i == 0:
                char_bichar_list.append("#START#" + sentence[i])
            elif i == len(sentence) - 1:
                char_bichar_list.append(sentence[i-1] + sentence[i])
                char_bichar_list.append(sentence[i] + "##END")
            else:
                char_bichar_list.append(sentence[i-1] + sentence[i])


    def similarity_degree(self,sentence_to_caculate):
        assert self.pool_sentence_num > 0

        input_sentence_char_bichar_list = list()
        one_sentence_in_pool_char_bichar_list = list()

        similarity_index_degree_dict = dict()

        self.get_char_and_bichar(sentence_to_caculate, input_sentence_char_bichar_list)
        input_sentence_num = len(input_sentence_char_bichar_list)

        for i in range(len(self.pool_list)):
            assert i not in similarity_index_degree_dict
            self.get_char_and_bichar(self.pool_list[i], one_sentence_in_pool_char_bichar_list)
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
    # test.load_input_and_caculate_similarity("./zhuxian/dev.simi_test.feats")
    # test.save_sort_results("./zhuxian/dev.simi_test.feats", "./zhuxian/similar_to_dev.feats")
    test.load_conll_pool_file(file_input)
    test.load_input_and_caculate_similarity(file_input)
    test.save_sort_results(file_input, file_out)








