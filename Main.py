class Padam:
    def __init__(self):
        self.form, self.pratyaya = '', ''

    def __str__(self):
        return f'Padam({self.form})'


class Subanta(Padam):
    def __init__(self, pratipadikam, vibhakti, vacanam):
        super().__init__()
        self.pratipadikam, self.vibhakti, self.vacanam = pratipadikam, vibhakti, vacanam
        self.pratyaya_lis = []

class Tiganta(Padam):
    pass