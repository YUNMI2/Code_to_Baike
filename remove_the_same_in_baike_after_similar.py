class Remove:
    def __init__(self):
        self.old_sentence = 0
        self.old_segment = 0
        self.old_char = 0
        self.new_sentence = 0
        self.new_segment = 0
        self.new_char = 0

    def read_file_posis(self, input_file, posi_list):
        posi_list.clear()

        with open(input_file, "r", encoding="utf-8") as fo:
            fo.seek(0)
            cur_posi = fo.tell()
            line = fo.readline()
            while line :
                if line.startswith("sentence:"):
                    posi_list.append(cur_posi)

                cur_posi = fo.tell()
                line = fo.readline()

    def read_Instance_by_posi(self, input_file, posi):
        with open(input_file, "r", encoding="utf-8") as fo:
            fo.seek(posi)
            one_Instance_list = []
            line = fo.readline()
            while line.strip():
                one_Instance_list.append(line.strip())
                line = fo.readline()
        return one_Instance_list

    def remove_the_same(self, input_file):
        output_file = input_file + ".remove_same.out_v20180605"
        posi_list = []
        self.read_file_posis(input_file, posi_list)
        with  open(output_file, "w", encoding="utf-8") as fw:
            i = 0
            j = i + 1

            before_Instance = self.read_Instance_by_posi(input_file, posi_list[i])
            self.old_sentence += 1

            for one in before_Instance:
                fw.write(one + "\n")
            fw.write("\n")
            self.new_sentence += 1

            while j < len(posi_list):
                next_Instance = self.read_Instance_by_posi(input_file, posi_list[j])
                self.old_sentence += 1
                if before_Instance != next_Instance:
                    before_Instance = next_Instance
                    self.new_sentence += 1

                    for one in before_Instance:
                        fw.write(one + "\n")
                    fw.write("\n")
                j += 1
        print ("old sentence num :", self.old_sentence)
        print("new sentence num :", self.new_sentence)




if __name__ == "__main__":
    test = Remove()
    test.remove_the_same("baike_data.size10to100.similar")











