import string

chinese_punction = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
english_punction = string.punctuation


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


if __name__ == "__main__":
    print(chinese_punction)
    print("，" in chinese_punction)
    print("," in english_punction)