
class Card:
    def __init__(self,data):
        self.id=data['id']; self.name=data['name']
        self.tags=data.get('tags',[])
        self.time=data.get('time',0)
        self.memory=data.get('memory',0)
        self.correct=data.get('correct',0)
        self.description=data.get('description','')
    def __str__(self):
        return f"{self.name} (T{self.time:+} M{self.memory:+} C{self.correct:+})"
