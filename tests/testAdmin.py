from tools.admin import *
import unittest


class TestAdmin(unittest.TestCase):


    def test_main(self):
        user = 1234
        admin_id = 1111
        admin = Admin()
        self.assertFalse(admin.is_admin(user))
        self.assertTrue(admin.is_admin(admin_id))
        admin.add(admin_id, user)
        self.assertTrue(admin.is_admin(user))
        admin.remove(admin_id, user)
        self.assertFalse(admin.is_admin(user))

        try:
            admin.add(user, user)
            self.fail("Missing NotAdminException")
        except NotAdminException:
            pass

