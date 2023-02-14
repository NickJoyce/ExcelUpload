import os

class File:
    def __init__(self, th, file_path, form_name, input_accept):
        self.th = th
        self.file_path = file_path
        self.form_name = form_name
        self.input_accept = input_accept
        self.file_name = self.get_file_name()


    def get_file_name(self):
        try:
            file_name = os.listdir(f"{self.file_path}")[0]
        except IndexError:
            file_name = "---файл не загружен---"
        return file_name