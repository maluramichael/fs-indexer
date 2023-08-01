class Rewrite:
    def __init__(self, starting_path, rewrite_path):
        self.starting_path = starting_path
        self.rewrite_path = rewrite_path

    def rewrite(self, path):
        return path.replace(self.starting_path, self.rewrite_path)
