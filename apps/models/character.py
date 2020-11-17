from apps import db

class Character(db.Model):
    __tablename__ = 'characters'
    id                 = db.Column(db.Integer, primary_key=True)
    name               = db.Column(db.String(64), index=True)
    can_edit_auth      = db.Column(db.Boolean, default=False)
    can_edit_tree      = db.Column(db.Boolean, default=False)
    can_edit_article   = db.Column(db.Boolean, default=True)

    def check_can(self,can_str:str):
        if hasattr(self,can_str):
            return getattr(self,can_str)
        return False