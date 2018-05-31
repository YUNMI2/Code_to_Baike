#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
class Stat:
    def __init__(self):
        self.char_frequency_dict = dict()
        self.num_keyword_list = list()
        self.posi_stat = dict()

    def IsToRemain(self,key_word_list,posi):
        num_key_word = 0
        for one in key_word_list: #删除地图的数据
            if "shadow出口©" in one or "NavInfo" in one or "道道通" in one:
                return []

        for one in key_word_list:
            if one.startswith("key word:"):
                num_key_word += 1
            if one.startswith("sentence:"):
                len_sentence = len(one.strip("sentence:").strip())

        assert (posi not in self.posi_stat)
        self.posi_stat[posi] = (2*num_key_word)/len_sentence
        #print(self.posi_stat)
        return key_word_list


    def readBaikeData(self,file_name):
        with open(file_name, "r",encoding="utf-8") as fo:
            fo.seek(0,os.SEEK_SET)
            posi = fo.tell()
            key_word_list = []
            line = fo.readline()
            while line:
                line = line.strip()
                if not line :
                    if key_word_list != []:
                        self.IsToRemain(key_word_list,posi)
                        posi = fo.tell()
                        key_word_list = []
                else:
                    key_word_list.append(line)
                line = fo.readline()
            if key_word_list != []:
                self.IsToRemain(key_word_list, posi)


    def extractBaikeData(self, file_name, max_Instance_num):
            sort_tuple = sorted(self.posi_stat.items(), key=lambda item: item[1], reverse=True)
            index_list = []
            all_instance_num = max_Instance_num
            if all_instance_num <= 0 or all_instance_num > len(sort_tuple):
                all_instance_num = len(sort_tuple)
            print("all_instance_num:",all_instance_num)
            for i in range(all_instance_num):
                index_list.append(sort_tuple[i][0])
            with open(file_name, "r", encoding="utf-8") as fo, open(file_name + ".moreinfo.sort.version_20180531", "w", encoding="utf-8") as fw_more:
                fo.seek(0,os.SEEK_SET)
                for posi in index_list:
                    fo.seek(posi,os.SEEK_SET)
                    line = fo.readline().strip()

                    while line:
                        fw_more.write(line + "\n")
                        line = fo.readline().strip()
                    fw_more.write("\n")


    def save_char_frequency_dict(self,file_name):

            if file_name == "":
                return
            else:
                import json
                self.char_frequency_dict = sorted(self.char_frequency_dict.items(), key=lambda x: x[1], reverse=True)
                with open(file_name, "w", encoding="utf-8", errors="ignore") as fw:
                    json.dump(self.char_frequency_dict, fw, indent=4, ensure_ascii=False)
                    fw.write('\n')
                    fw.flush()
                    os.fsync(fw)




if __name__ == "__main__":
    stat_test = Stat()
    file_name = sys.argv[1]
    stat_test.readBaikeData(file_name)
    stat_test.extractBaikeData(file_name,0)
