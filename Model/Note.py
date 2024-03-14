class Note:
    def __init__(self, id, title, note_body):
        self._id = id
        self._title = title
        self._note_body = note_body
        self._date = str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = title

    def get_note_body(self):
        return self._note_body

    def set_note_body(self, note_body):
        self._note_body = note_body

    def get_date(self):
        return self._date

    def set_date(self, date):
        self._date = date