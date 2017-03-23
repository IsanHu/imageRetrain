# Filename: bqss_text_reader.py
# coding:utf-8


class BQSSTextsReader:
    def __init__(self):
        self.texts = []

    def decode_config_file(self, file_path):
        with open(file_path, 'r') as f:
            for line in f.readlines():
                line_str = line.strip()
                if len(line_str) > 0:
                    self.texts.append(line_str)

if __name__ == '__main__':
    reader = BQSSTextsReader()
    reader.decode_config_file("uploads/maintain2.txt")
    for i in range(0, len(reader.texts)):
        print reader.texts[i]