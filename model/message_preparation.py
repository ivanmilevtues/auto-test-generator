from history_scanner.CommitData import CommitData


class MessageBuilder:

    def __init__(self, commits_data: [CommitData], train=0.7):
        self.commits_data = commits_data
        self.train = train

    def create_prompt(self):
        data_for_training = self.commits_data[:int(len(self.commits_data) * self.train)]
        for data in data_for_training:
            yield data.construct_prompt()
