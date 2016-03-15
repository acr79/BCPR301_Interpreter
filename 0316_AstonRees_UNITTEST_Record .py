ERP = __import__("0316_AstonRees_ERP_")
import unittest

class TestRecordClass(unittest.TestCase):

    def test_InvalidGenderException(self):
        """
        Ensure that a correct definition of gender is adhered to
        """
        self.assertRaises(ERP.InvalidGenderException,
                          ERP.Record, None, "")

    def test_DefaultAttributes(self):
        """
        Expect default atttibute values (age 0, sales 0, BMI Normal, income 0)
        """
        expAge = 0
        expSales = 0
        expBMI = "Normal"
        expIncome = 0
        rec = ERP.Record(None, "M")
        self.assertEqual(expAge, rec.getAge())
        self.assertEqual(expSales, rec.getSales())
        self.assertEqual(expBMI, rec.getBMI())
        self.assertEqual(expIncome, rec.getIncome())

    def test_NoChangeAge01(self):
        """
        Expect age to remain after attempting to set it to 100 (over the limit)
        """
        expAge = 99
        rec = ERP.Record(None, "M")
        """Prove expAge is not default value"""
        self.assertNotEqual(expAge, rec.getAge())
        rec.setAge(expAge)
        rec.setAge(100)
        self.assertEqual(expAge, rec.getAge())

    def test_NoChangeAge02(self):
        """
        Expect age to remain after attempting to set it to 40.5 (decimal)
        """
        expAge = 41
        rec = ERP.Record(None, "F")
        """Prove expAge is not default value"""
        self.assertNotEqual(expAge, rec.getAge())
        rec.setAge(expAge)
        rec.setAge(40.5)
        self.assertEqual(expAge, rec.getAge())

    def test_NoChangeAge03(self):
        """
        Expect age to remain after attempting to set it to "A"
        String can be used for the method, but "A" represents no number
        """
        expAge = 30
        ageStr = str(30)
        self.assertEqual(ageStr, "30")
        rec = ERP.Record(None, "F")
        """Prove expAge is not default value"""
        self.assertNotEqual(expAge, rec.getAge())
        rec.setAge(ageStr)
        rec.setAge("A")
        self.assertEqual(expAge, rec.getAge())

    def test_NoChangeSales01(self):
        """
        Expect sales to remain after attempting to set it to 1000
        (over the limit)
        """
        expSales = 999
        rec = ERP.Record(None, "M")
        """Prove expSales is not default value"""
        self.assertNotEqual(expSales, rec.getSales())
        rec.setSales(expSales)
        rec.setSales(1000)
        self.assertEqual(expSales, rec.getSales())

    def test_NoChangSales02(self):
        """
        Expect sales to remain after attempting to set it to 406.5 (decimal)
        """
        expSales = 410
        rec = ERP.Record(None, "F")
        """Prove expSales is not default value"""
        self.assertNotEqual(expSales, rec.getSales())
        rec.setSales(expSales)
        rec.setSales(406.5)
        self.assertEqual(expSales, rec.getSales())

    def test_NoChangeSales03(self):
        """
        Expect sales to remain after attempting to set it to "A"
        String can be used for the method, but "A" represents no number
        """
        expSales = 330
        salesStr = str(330)
        self.assertEqual(salesStr, "330")
        rec = ERP.Record(None, "F")
        """Prove expSales is not default value"""
        self.assertNotEqual(expSales, rec.getSales())
        rec.setSales(salesStr)
        rec.setSales("A")
        self.assertEqual(expSales, rec.getSales())

    def test_NoChangeBMI(self):
        """
        Expect BMI to remain after attempting to set it to 'other' (not
        recognised in enumeration)
        """
        expBMI = "Overweight"
        rec = ERP.Record(None, "M")
        """Prove expBMI is not default value"""
        self.assertNotEqual(expBMI, rec.getBMI())
        rec.setBMI(expBMI)
        rec.setBMI("other")
        self.assertEqual(expBMI, rec.getBMI())


if __name__ == "__main__":
    unittest.main()

