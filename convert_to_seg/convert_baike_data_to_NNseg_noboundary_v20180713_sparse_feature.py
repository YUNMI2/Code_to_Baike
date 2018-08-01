import sys
from punct import chinese_punction
from punct import english_punction


def get_type(char):
    if char == "#START#":
        return "#START#"
    for i in range(len(char)):
        if char[i].isdigit():
            return "NU"
        elif char[i].encode("utf-8").isalpha():
            return "EN"
        elif char[i] in chinese_punction or char[i] in english_punction:
            return "PU"
        else:
            return char

def to_conll(senten, indexs_tuple_list):
    conll_list = []
    start_indexs = []
    end_indexs = []
    margin_left_indexs = []
    margin_right_indexs = []
    for one_tuple in indexs_tuple_list:
        for i in range(2):
            assert one_tuple[i] not in start_indexs and one_tuple[i] not in end_indexs
        start_indexs.append(one_tuple[0])
        margin_left_indexs.append(one_tuple[0] - 1)
        end_indexs.append(one_tuple[1])
        margin_right_indexs.append(one_tuple[1] + 1)

    for i in range(len(senten)):
        assert senten[i] != " "
        cur_char = senten[i]
        pre_char = senten[i-1] if i > 0 else "#START#"
        if i in start_indexs:
            if i+1 in end_indexs:
                cur_tag = "b-seg"
            else:
                cur_tag = "b-seg/s-seg"
        elif i in end_indexs:
            if i-1 in start_indexs:
                cur_tag = "e-seg"
            else:
                cur_tag = "e-seg/s-seg"
        elif i in margin_left_indexs and i not in margin_right_indexs:
            cur_tag = "a-seg"
        elif i in margin_right_indexs and i not in margin_left_indexs:
            cur_tag = "a-seg"
        elif i in margin_right_indexs and i in margin_left_indexs:
            cur_tag = "s-seg"
        else:
            cur_tag = "a-seg"
        isSame  = isSame = "[T4]same" if cur_char == pre_char else "[T4]diff"
        new_line = cur_char + " " + "[T1]" + cur_char + pre_char + " [T2]" +  get_type(cur_char) + " [T3]" + get_type(cur_char) + get_type(pre_char) + " " + isSame + " " + cur_tag

        conll_list.append(new_line)
    return conll_list




def extract_feat(sen_word_list):
    sentence = ""
    indexs_tuple_list = list()
    conll_list = list()
    key_words = list()

    for one in sen_word_list:
        if one.startswith("sentence:"):
            assert (sentence == "")
            sentence = one.lstrip("sentence:").strip()
        elif one.startswith("key word:"):
            assert ( one.lstrip("key word:").strip() in sentence)
            if one.lstrip("key word:").strip() not in key_words:
                key_words.append(one.lstrip("key word:").strip())

    for one_word in key_words:
        assert len(one_word) > 1
        start_index = sentence.index(one_word)
        indexs_tuple_list.append((start_index, start_index + len(one_word) - 1 ))

    conll_list = to_conll(sentence, indexs_tuple_list)
    return conll_list



def extract_list(sentence_and_key_word_list):
    new_list = []
    sentence = ""

    for i in range(len(sentence_and_key_word_list)):
        if "sentence:" in sentence_and_key_word_list[i]:
            sentence = sentence_and_key_word_list[i][10:]
            if sentence.count("…") >= 2:
                return []
            if len(sentence.strip().split()) > 1:
                return []
            if len(sentence_and_key_word_list[i][10:])  == 1:
                return []
            else:
                new_list.append(sentence_and_key_word_list[i])
        elif "key word:" in sentence_and_key_word_list[i]:
            if len(sentence_and_key_word_list[i][10:]) > 1 :
                if sentence.count(sentence_and_key_word_list[i][10:]) > 1:
                    return []
                new_list.append(sentence_and_key_word_list[i])
    return new_list


def main():
    file_baike = sys.argv[1]
    file_baike_out = file_baike + ".2queding.nobou.sparse.bichar.feats"

    all_num = 500000

    with open(file_baike, "r", encoding="utf-8") as fo,open(file_baike_out, "w", encoding="utf-8") as fw:
        sentence_and_key_word_list = []
        line = fo.readline()
        total_num = 0
        while line:
            line_strip = line.strip()

            if line_strip:
                sentence_and_key_word_list.append(line_strip)
            else:
                if sentence_and_key_word_list != []:
                    new_list = extract_list(sentence_and_key_word_list)
                    if new_list != [] and total_num <= all_num:
                        total_num += 1
                        conll_list = extract_feat(new_list)
                        for one in conll_list:
                            fw.write(one + "\n")
                        fw.write("\n")
                    elif total_num > all_num:
                        break
                    sentence_and_key_word_list.clear()
            line = fo.readline()


if __name__ == "__main__":
    main()





