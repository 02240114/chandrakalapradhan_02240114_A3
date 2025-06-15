import unittest
from chandrakalapradhan_02240114_A3_PA import BankAccount, InvalidAmountError, InsufficientFundsError

# test_chandrakalapradhan_02240114_A3_PA.py


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.acc1 = BankAccount("12345", "Alice", "1234", 1000)
        self.acc2 = BankAccount("54321", "Bob", "5678", 500)

    def test_deposit_valid(self):
        self.acc1.deposit(200)
        self.assertEqual(self.acc1.balance, 1200)
        self.assertIn("Deposited Nu.200", self.acc1.get_transactions()[-1])

    def test_deposit_invalid(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.deposit(0)
        with self.assertRaises(InvalidAmountError):
            self.acc1.deposit(-50)

    def test_withdraw_valid(self):
        self.acc1.withdraw(300)
        self.assertEqual(self.acc1.balance, 700)
        self.assertIn("Withdrew Nu.300", self.acc1.get_transactions()[-1])

    def test_withdraw_invalid(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.withdraw(0)
        with self.assertRaises(InvalidAmountError):
            self.acc1.withdraw(-10)

    def test_withdraw_insufficient(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc2.withdraw(600)

    def test_transfer_valid(self):
        self.acc1.transfer(200, self.acc2)
        self.assertEqual(self.acc1.balance, 800)
        self.assertEqual(self.acc2.balance, 700)
        self.assertIn("Sent Nu.200 to Bob (54321)", self.acc1.get_transactions()[-1])
        self.assertIn("Received Nu.200 from Alice (12345)", self.acc2.get_transactions()[-1])

    def test_transfer_invalid_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.transfer(0, self.acc2)
        with self.assertRaises(InvalidAmountError):
            self.acc1.transfer(-50, self.acc2)

    def test_transfer_insufficient(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc2.transfer(1000, self.acc1)

    def test_transfer_to_self(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.transfer(100, self.acc1)

    def test_mobile_topup_valid(self):
        self.acc1.mobile_topup(100, "17123456")
        self.assertEqual(self.acc1.balance, 900)
        self.assertIn("Mobile top-up Nu.100 to 17123456", self.acc1.get_transactions()[-1])

    def test_mobile_topup_invalid(self):
        with self.assertRaises(InvalidAmountError):
            self.acc1.mobile_topup(0, "17123456")
        with self.assertRaises(InvalidAmountError):
            self.acc1.mobile_topup(-20, "17123456")

    def test_mobile_topup_insufficient(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc2.mobile_topup(1000, "17123456")

    def test_get_transactions(self):
        self.acc1.deposit(50)
        self.acc1.withdraw(20)
        txns = self.acc1.get_transactions()
        self.assertTrue(any("Deposited Nu.50" in t for t in txns))
        self.assertTrue(any("Withdrew Nu.20" in t for t in txns))

if __name__ == "__main__":
    unittest.main()