from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_user_name(self, name):
        return self.session.query(User).filter(User.name == name).one_or_none()

    def get_user_by_email(self, email):
        user = self.session.query(User).filter(User.email == email).one_or_none()
        return user

    def create(self, id):
        ent = User(**id)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, rid):
        user = self.get_one(rid)
        self.session.delete(user)
        self.session.commit()

    def update(self, id):
        user = self.get_one(id.get("id"))
        for k, v in id.items():
            setattr(user, k, v)

        self.session.add(user)
        self.session.commit()
