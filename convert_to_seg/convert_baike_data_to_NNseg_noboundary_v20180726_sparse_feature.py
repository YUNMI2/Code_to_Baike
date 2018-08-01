import sys
import punct

def convert_baike_conll_to_baike_pa(baike_conll, file_out):
    with open(baike_conll, "r", encoding="utf-8") as fo, open(file_out, "w", encoding="utf-8") as fw:
        line = fo.readline()
        sentence = ""
        cur_word = ""
        key_word_list = []
        while line:
            line = line.strip()
            if line:
                sentence += line[0]
                if line.endswith("b-seg/s-seg") or line.endswith("b-seg") or line.endswith("s-seg/b-seg"):
                    assert cur_word == ""
                    cur_word += line[0]
                elif line.endswith("a-seg") or line.endswith("m-seg"):
                    if cur_word != "":
                        cur_word += line[0]
                elif line.endswith("e-seg/s-seg") or line.endswith("e-seg") or line.endswith("s-seg/e-seg"):
                    assert cur_word != ""
                    cur_word += line[0]
                    key_word_list.append(cur_word)
                    cur_word = ""
            else:
                fw.write("sentence:\t" + sentence + "\n")
                for one_word in key_word_list:
                    fw.write("key word:\t" + one_word + "\n")
                fw.write("\n")
                sentence = ""
                key_word_list = []
            line = fo.readline()

def convert_baike_to_nolinkseg(baike_file_name):
    file_out = baike_file_name + ".nolinkseg.bichar.feats"
    with open(baike_file_name, "r", encoding="utf-8") as fo, open(file_out, "w", encoding="utf-8") as fw:
        sentence = ""
        key_word_list = list()
        line = fo.readline()
        while line:
            line = line.strip()
            if line:
                if line.startswith("sentence:"):
                    assert sentence == "" and len(line.lstrip("sentence:").strip().split()) == 1
                    sentence = line.lstrip("sentence:").strip()
                elif line.startswith("key word:"):
                    assert line.lstrip("key word:").strip() in sentence
                    sentence = sentence.replace(line.lstrip("key word:").strip(), " " + line.lstrip("key word:").strip() + " ")
                    key_word_list.append(line.lstrip("key word:").strip())
            else:
                sentence_seg_list = sentence.split()
                pre_char = "#START#"
                for one_seg in sentence_seg_list:
                    if one_seg not in key_word_list:
                        fw.write(one_seg + " [T1]" + one_seg + pre_char + " s-seg\n")
                        pre_char = one_seg[-1]
                    else:
                        if len(one_seg) == 2:
                            fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg\n")
                            fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[-2] + " e-seg\n")
                            pre_char = one_seg[-1]
                        else:
                            fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg/s-seg\n")
                            fw.write(one_seg[1:-1] + " [T1]" + one_seg[1:-1] + one_seg[0] + " a-seg\n")
                            fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[-2] + " e-seg/s-seg\n")
                            pre_char = one_seg[-1]
                fw.write("\n")
                key_word_list = list()
                sentence = ""
            line = fo.readline()



def convert_peking_to_nolinkseg(peking_file_name):
    file_out = peking_file_name + ".nolinkseg.bichar.feats"
    with open(peking_file_name, "r", encoding="utf-8") as fo, open(file_out, "w", encoding="utf-8") as fw:
        sentence = ""
        key_word_list = list()
        line = fo.readline()
        while line:
            line = line.strip()
            print(line)
            if line:
                if line.startswith("sentence:"):
                    assert sentence == "" and len(line.lstrip("sentence:").strip().split()) == 1
                    sentence = line.lstrip("sentence:").strip()
                elif line.startswith("key word:"):
                    assert line.lstrip("key word:").strip() in sentence
                    sentence = sentence.replace(line.lstrip("key word:").strip(), " " + line.lstrip("key word:").strip() + " ")
                    key_word_list.append(line.lstrip("key word:").strip())
            else:
                sentence_seg_list = sentence.split()
                pre_char = "#START#"

                for one_seg in sentence_seg_list:
                    if one_seg not in key_word_list:
                        fw.write(one_seg + " [T1]" + one_seg + pre_char + " s-seg\n")
                        pre_char = one_seg[-1]
                    else:
                        for i in range(len(one_seg)):
                            if i == 0:
                                tag = "b-seg"
                            elif i == len(one_seg) - 1:
                                tag = "s-seg"
                            else:
                                tag = "m-seg"
                            fw.write(one_seg[i] + " [T1]" + one_seg[i] + pre_char + " " + tag +"\n")
                            pre_char = one_seg[i]
                fw.write("\n")
                key_word_list = list()
                sentence = ""
            line = fo.readline()




def convert_baike_to_nolinkseg_with_bou(baike_file_name):
    file_out = baike_file_name + ".nolinksegbou.bichar.feats"
    with open(baike_file_name, "r", encoding="utf-8") as fo, open(file_out, "w", encoding="utf-8") as fw:
        sentence = ""
        key_word_list = list()
        line = fo.readline()
        while line:
            line = line.strip()
            if line:
                if line.startswith("sentence:"):
                    assert sentence == "" and len(line.lstrip("sentence:").strip().split()) == 1
                    sentence = line.lstrip("sentence:").strip()
                elif line.startswith("key word:"):
                    assert line.lstrip("key word:").strip() in sentence
                    sentence = sentence.replace(line.lstrip("key word:").strip(), " " + line.lstrip("key word:").strip() + " ")
                    key_word_list.append(line.lstrip("key word:").strip())
            else:
                sentence_seg_list = sentence.split()
                pre_char = "#START#"
                for one_seg in sentence_seg_list:
                    if one_seg not in key_word_list:
                        if len(one_seg) > 1:
                            fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg/s-seg\n")
                            if len(one_seg) > 2:
                                fw.write(one_seg[1:-1] + " [T1]" + one_seg[1:-1] + one_seg[0] + " a-seg\n")
                                fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[1:-1] + " e-seg/s-seg\n")
                            else:
                                fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[0] + " e-seg/s-seg\n")
                        else:
                            fw.write(one_seg + " [T1]" + one_seg + pre_char + " s-seg\n")
                        pre_char = one_seg[-1]
                    else:
                        if len(one_seg) == 2:
                            fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg\n")
                            fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[-2] + " e-seg\n")
                            pre_char = one_seg[-1]
                        else:
                            for i in range(len(one_seg)):
                                if i == 0:
                                    fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg/s-seg\n")
                                elif i == len(one_seg) -1:
                                    fw.write(one_seg[i] + " [T1]" + one_seg[i] + one_seg[i-1] + " e-seg/s-seg\n")
                                else:
                                    fw.write(one_seg[i] + " [T1]" + one_seg[i] + one_seg[i-1] + " a-seg\n")
                            pre_char = one_seg[-1]
                fw.write("\n")
                key_word_list = list()
                sentence = ""
            line = fo.readline()



def convert_baike_to_nolinkseg_with_bou_sparse_feature(baike_file_name):
    file_out = baike_file_name + ".nolinksegbou.bichar.feats"
    with open(baike_file_name, "r", encoding="utf-8") as fo, open(file_out, "w", encoding="utf-8") as fw:
        sentence = ""
        key_word_list = list()
        line = fo.readline()
        while line:
            line = line.strip()
            if line:
                if line.startswith("sentence:"):
                    assert sentence == "" and len(line.lstrip("sentence:").strip().split()) == 1
                    sentence = line.lstrip("sentence:").strip()
                elif line.startswith("key word:"):
                    assert line.lstrip("key word:").strip() in sentence
                    sentence = sentence.replace(line.lstrip("key word:").strip(), " " + line.lstrip("key word:").strip() + " ")
                    key_word_list.append(line.lstrip("key word:").strip())
            else:
                sentence_seg_list = sentence.split()
                pre_char = "#START#"
                for one_seg in sentence_seg_list:
                    if one_seg not in key_word_list:
                        if len(one_seg) > 1:
                            fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " [T2]" + get_type(one_seg[0]) + " [T3]" + get_type(one_seg[0]) + get_type(pre_char) + " b-seg/s-seg\n")
                            if len(one_seg) > 2:
                                fw.write(one_seg[1:-1] + " [T1]" + one_seg[1:-1] +  one_seg[0] + " a-seg\n")
                                fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[1:-1] + " e-seg/s-seg\n")
                            else:
                                fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[0] + " e-seg/s-seg\n")
                        else:
                            fw.write(one_seg + " [T1]" + one_seg + pre_char + " s-seg\n")
                        pre_char = one_seg[-1]
                    else:
                        if len(one_seg) == 2:
                            fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg\n")
                            fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[-2] + " e-seg\n")
                            pre_char = one_seg[-1]
                        else:
                            for i in range(len(one_seg)):
                                if i == 0:
                                    fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg/s-seg\n")
                                elif i == len(one_seg) -1:
                                    fw.write(one_seg[i] + " [T1]" + one_seg[i] + one_seg[i-1] + " e-seg/s-seg\n")
                                else:
                                    fw.write(one_seg[i] + " [T1]" + one_seg[i] + one_seg[i-1] + " a-seg\n")
                            pre_char = one_seg[-1]
                fw.write("\n")
                key_word_list = list()
                sentence = ""
            line = fo.readline()




def convert_baike_to_nolinkseg_with_bou_2_uncertain(baike_file_name):
    file_out = baike_file_name + ".2noqueding.nolinksegbou.bichar.feats"
    with open(baike_file_name, "r", encoding="utf-8") as fo, open(file_out, "w", encoding="utf-8") as fw:
        sentence = ""
        key_word_list = list()
        line = fo.readline()
        while line:
            line = line.strip()
            if line:
                if line.startswith("sentence:"):
                    assert sentence == "" and len(line.lstrip("sentence:").strip().split()) == 1
                    sentence = line.lstrip("sentence:").strip()
                elif line.startswith("key word:"):
                    assert line.lstrip("key word:").strip() in sentence
                    sentence = sentence.replace(line.lstrip("key word:").strip(), " " + line.lstrip("key word:").strip() + " ")
                    key_word_list.append(line.lstrip("key word:").strip())
            else:
                sentence_seg_list = sentence.split()
                pre_char = "#START#"
                for one_seg in sentence_seg_list:
                    if one_seg not in key_word_list:
                        if len(one_seg) > 1:
                            fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg/s-seg\n")
                            if len(one_seg) > 2:
                                fw.write(one_seg[1:-1] + " [T1]" + one_seg[1:-1] + one_seg[0] + " a-seg\n")
                                fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[1:-1] + " e-seg/s-seg\n")
                            else:
                                fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[0] + " e-seg/s-seg\n")
                        else:
                            fw.write(one_seg + " [T1]" + one_seg + pre_char + " s-seg\n")
                        pre_char = one_seg[-1]
                    else:
                        if len(one_seg) == 2:
                            fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg/s-seg\n")
                            fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[-2] + " e-seg/s-seg\n")
                            pre_char = one_seg[-1]
                        else:
                            for i in range(len(one_seg)):
                                if i == 0:
                                    fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg/s-seg\n")
                                elif i == len(one_seg) -1:
                                    fw.write(one_seg[i] + " [T1]" + one_seg[i] + one_seg[i-1] + " e-seg/s-seg\n")
                                else:
                                    fw.write(one_seg[i] + " [T1]" + one_seg[i] + one_seg[i-1] + " a-seg\n")
                            pre_char = one_seg[-1]
                fw.write("\n")
                key_word_list = list()
                sentence = ""
            line = fo.readline()




def convert_peking_to_nolinkseg_with_bou(peking_file_name):
    file_out = peking_file_name + ".nolinksegbou.bichar.feats"
    with open(peking_file_name, "r", encoding="utf-8") as fo, open(file_out, "w", encoding="utf-8") as fw:
        sentence = ""
        key_word_list = list()
        line = fo.readline()
        while line:
            line = line.strip()
            # print(line)
            if line:
                if line.startswith("sentence:"):
                    assert sentence == "" and len(line.lstrip("sentence:").strip().split()) == 1
                    sentence = line.lstrip("sentence:").strip()
                elif line.startswith("key word:"):
                    assert line.lstrip("key word:").strip() in sentence
                    sentence = sentence.replace(line.lstrip("key word:").strip(), " " + line.lstrip("key word:").strip() + " ")
                    key_word_list.append(line.lstrip("key word:").strip())
            else:
                sentence_seg_list = sentence.split()
                pre_char = "#START#"

                for one_seg in sentence_seg_list:
                    if one_seg not in key_word_list:
                        if len(one_seg) == 1:
                            fw.write(one_seg + " [T1]" + one_seg + pre_char + " s-seg\n")
                            pre_char = one_seg
                        else:
                            fw.write(one_seg[0] + " [T1]" + one_seg[0] + pre_char + " b-seg/s-seg\n")
                            if len(one_seg) > 2:
                                fw.write(one_seg[1:-1] + " [T1]" + one_seg[1:-1] + one_seg[0] + " a-seg\n")
                                fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[1:-1] + " e-seg/s-seg\n")
                            else:
                                fw.write(one_seg[-1] + " [T1]" + one_seg[-1] + one_seg[0] + " e-seg/s-seg\n")
                            pre_char = one_seg[-1]
                    else:
                        for i in range(len(one_seg)):
                            if i == 0:
                                tag = "b-seg"
                            elif i == len(one_seg) - 1:
                                tag = "s-seg"
                            else:
                                tag = "m-seg"
                            fw.write(one_seg[i] + " [T1]" + one_seg[i] + pre_char + " " + tag +"\n")
                            pre_char = one_seg[i]
                fw.write("\n")
                key_word_list = list()
                sentence = ""
            line = fo.readline()


if __name__ == "__main__":
    # convert_baike_conll_to_baike_pa("./bichar_yuan/baike.com.dev.notrainwords.seg.fre.morezero.removealpha.nobou.bichar.feats","./bichar_yuan/bichar_xin/baike.com.dev.pa")
    # convert_baike_conll_to_baike_pa("./bichar_yuan/baike.com.test.notrainwords.nomoretrainchars.morezero.remove.2queding.nobou.bichar.feats","./bichar_yuan/bichar_xin/baike.com.test.pa")
    # convert_baike_conll_to_baike_pa("./bichar_yuan/baike.fin.test.notrainwords.nomoretrainchars.morezero.remove.2queding.nobou.bichar.feats","./bichar_yuan/bichar_xin/baike.fin.test.pa")
    # convert_baike_conll_to_baike_pa("./bichar_yuan/baike.lit.test.notrainwords.nomoretrainchars.morezero.remove.2queding.nobou.bichar.feats","./bichar_yuan/bichar_xin/baike.lit.test.pa")
    # convert_baike_conll_to_baike_pa("./bichar_yuan/baike.med.test.notrainwords.nomoretrainchars.morezero.remove.2queding.nobou.bichar.feats","./bichar_yuan/bichar_xin/baike.med.test.pa")
    # convert_baike_conll_to_baike_pa("./bichar_yuan/baike.zxd.seg.fre.morezero.remove.2queding.nobou.bichar.feats","./bichar_yuan/bichar_xin/baike.ZXD.pa")
    # convert_baike_conll_to_baike_pa("./bichar_yuan/peking_xinhua.conll","./bichar_yuan/bichar_xin/peking.pa")
    # convert_baike_to_nolinkseg_with_bou("./bichar_yuan/bichar_xin/baike.com.dev.pa")
    # convert_baike_to_nolinkseg_with_bou("./bichar_yuan/bichar_xin/baike.com.test.pa")
    # convert_baike_to_nolinkseg_with_bou("./bichar_yuan/bichar_xin/baike.fin.test.pa")
    convert_baike_to_nolinkseg_with_bou_2_uncertain("./bichar_yuan/bichar_xin/baike.lit.test.pa")
    # convert_baike_to_nolinkseg_with_bou("./bichar_yuan/bichar_xin/baike.med.test.pa")
    # convert_baike_to_nolinkseg_with_bou("./bichar_yuan/bichar_xin/baike.ZXD.pa")
    # convert_peking_to_nolinkseg_with_bou("./bichar_yuan/bichar_xin/peking.pa")





