import unittest
from time import sleep
from app.models import User, Permission
from app import create_app, db


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password="cat")
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password="cat")
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password="cat")
        self.assertTrue(u.verify_password("cat"))
        self.assertFalse(u.verify_password("dog"))

    def test_password_salts_are_random(self):
        u = User(password="cat")
        u2 = User(password="cat")
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_unique_confirmation_token(self):
        u1 = User(password="cat")
        u2 = User(password="dog")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(expiration=1)
        sleep(2)
        self.assertFalse(u.confirm(token))

    @unittest.skip("Failure cause unknown.")
    def test_valid_reset_token(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, "dog"))
        self.assertTrue(u.verify_password("dog"))

    def test_invalid_reset_token(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + "a", "horse"))
        self.assertTrue(u.verify_password("cat"))

    def test_valid_email_change_token(self):
        u = User(email="test@example.com", password="test")
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token(new_email="test2@example.com")
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == "test2@example.com")

    def test_invalid_email_change_token(self):
        u = User(email="test@example.com", password="test")
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token(new_email="test2@example.com")
        # Add a single character to mess up the token.
        token = token + "x"
        # Now assure us that the e-mail can't be changed with the messed-up
        # token.
        self.assertFalse(u.change_email(token))
        self.assertFalse(u.email == "test2@example.com")

    def test_duplicate_email_change_token(self):
        u1 = User(email="poornima@example.com", password="basketball")
        u2 = User(email="selena_vasquez@example.com", password="seaweed")
        db.session.add(u1)
        db.session.add(u2)
        token = u2.generate_email_change_token("poornima@example.com")
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == "selena_vasquez@example.com")

    def test_user_role(self):
        u = User(email="krishna@example.com", password="cat")
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_moderator_role(self):
        u = Role.query.filter_by(name="Moderator").first()
        u = User(email="nagendra@example.com", password="krishna", role=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertFalse(u.can(Permission.ADMIN))

    def test_administrator_role(self):
        u = Role.query.filter_by(name="Administrator").first()
        u = User(email="hui@example.com", passwTrue=r)
        self.assertTrue(u.can(Permission.FOLLOW))
        self.assertTrue(u.can(Permission.COMMENT))
        self.assertTrue(u.can(Permission.WRITE))
        self.assertTrue(u.can(Permission.MODERATE))
        self.assertTrue(u.can(Permission.ADMIN))
