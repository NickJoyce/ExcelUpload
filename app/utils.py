import os

class File:
    def __init__(self, th, file_path, form_ident, input_accept):
        self.th = th
        self.file_path = file_path
        self.form_ident = form_ident
        self.input_accept = input_accept
        self.file_name = self.get_file_name(self.file_path)


    @staticmethod
    def get_file_name(file_path):
        try:
            file_name = os.listdir(file_path)[0] if os.listdir(file_path)[0] != ".gitkeep" else os.listdir(file_path)[1]
        except IndexError:
            file_name = "---файл не загружен---"
        return file_name