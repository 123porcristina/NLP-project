"""This saves any list variable into a pickle file"""
import pickle


class SaveList:
    def __init__(self, dir_base, tokens, file_name):
        self.dir_base = dir_base
        self.tokens = tokens
        self.file_name = file_name

    def save_token_list(self):
        with open(self.dir_base + '/' + self.file_name, 'wb') as handle:
            pickle.dump(self.tokens, handle, protocol=pickle.HIGHEST_PROTOCOL)
