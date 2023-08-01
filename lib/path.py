import os


class Path:
    def __init__(self, directory, file_name, rewriter=None):
        self.directory = directory
        self.file_name = file_name
        self.rewriter = rewriter

    def __str__(self):
        full_path = self.original_path()

        if self.rewriter is not None:
            return self.rewriter.rewrite(full_path)

        return full_path

    def get_directory(self):
        if self.rewriter is not None:
            return self.rewriter.rewrite(self.directory)

        return self.directory

    def original_path(self):
        return os.path.join(self.directory, self.file_name)
