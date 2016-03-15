ERP = __import__("0316_AstonRees_ERP_")
import unittest

class TestRecordCollectionClass(unittest.TestCase):

    def test_InvalidIDException(self):
        """
        Ensure that a correct definition of ID format is adhered to
        """
        coll = ERP.RecordCollection()
        self.assertRaises(ERP.InvalidIDException,
                          coll.addRecord, "", "F", None, None, None, None,
                          None, None)

    def test_DuplicateIDException(self):
        """
        Ensure that a record cannot be added when ID is already taken
        """
        coll = ERP.RecordCollection()
        theID = "S111"
        coll.addRecord(theID, "F", None, None, None, None, None, None)
        # firstRec = coll.findRecord(theID)
        self.assertRaises(ERP.DuplicateIDException,
                          coll.addRecord, theID, "F", None, None, None, None,
                          None, None)

    def test_AutoIDOnInvalidID(self):
        """
        If the ID is specified incorrectly, the new record will still get
        added if autoID is True
        """
        expSize = 1
        coll = ERP.RecordCollection()
        """Prove expSize is not achieved yet"""
        self.assertNotEqual(expSize, len(coll.getAllRecords()))
        coll.addRecord("", "F", None, None, None, None, True, None)
        self.assertEqual(expSize, len(coll.getAllRecords()))

    def test_AutoIDOnDuplicateID(self):
        """
        If the ID specified is a duplicate, the new record will still get added
        if autoID is True
        Note that the auto ID function only guarantees that the new record will
        get added, it does not guarantee the value of the ID
        This is because the auto ID function may be up for improvement
        """
        expSize = 2
        autoID = True
        coll = ERP.RecordCollection()
        theID = "W222"
        coll.addRecord(theID, "F", None, None, None, None, autoID, None)
        """Prove expSize is not achieved yet"""
        self.assertNotEqual(expSize, len(coll.getAllRecords()))
        coll.addRecord(theID, "F", None, None, None, None, autoID, None)
        self.assertEqual(expSize, len(coll.getAllRecords()))

    def test_OverwriteOnDuplicateID(self):
        """
        If the ID specified is a duplicate, the new record will replace the
        existing record
        """
        expSize = 1
        overwrite = True
        coll = ERP.RecordCollection()
        theID = "F333"
        coll.addRecord(theID, "M", None, None, None, None, None, overwrite)
        self.assertEqual(expSize, len(coll.getAllRecords()))
        originalRec = coll.getAllRecords()[0]
        coll.addRecord(theID, "M", None, None, None, None, None, overwrite)
        """Prove expSize remains the same"""
        self.assertEqual(expSize, len(coll.getAllRecords()))
        newRec = coll.getAllRecords()[0]
        """Prove that objects are different"""
        self.assertNotEqual(originalRec, newRec)
        """Prove that they have the same ID"""
        self.assertEqual(originalRec.getID(), newRec.getID())

    def test_RecordOrdering01_AddingRecords(self):
        """
        Ensure that records are ordered in the collection by ID
        A000 comes before A001
        A999 comes before B000
        """
        rec1 = None
        rec2 = None
        rec3 = None
        rec4 = None
        id1 = "A000"
        id2 = "A001"
        id3 = "A999"
        id4 = "B000"
        self.assertTrue(id1 < id2 < id3 < id4)
        coll = ERP.RecordCollection()
        """A001 added first"""
        coll.addRecord(id2, "M", None, None, None, None, None, None)
        rec2 = coll.getAllRecords()[0]
        self.assertEqual(id2, rec2.getID())
        """B000"""
        coll.addRecord(id4, "M", None, None, None, None, None, None)
        rec4 = coll.getAllRecords()[1]
        self.assertEqual(id4, rec4.getID())
        """A999"""
        coll.addRecord(id3, "M", None, None, None, None, None, None)
        rec3 = coll.getAllRecords()[1]
        self.assertEqual(id3, rec3.getID())
        """A000"""
        coll.addRecord(id1, "M", None, None, None, None, None, None)
        rec1 = coll.getAllRecords()[0]
        self.assertEqual(id1, rec1.getID())
        """"""
        self.assertTrue(rec1 != rec2 != rec3 != rec4)
        self.assertTrue([rec1, rec2, rec3, rec4], coll.getAllRecords())

    def test_RecordOrdering02_DeletingRecords(self):
        """
        Ensure that records are ordered in the collection by ID
        Collection will contatin C000, C050, C100 in order
        Then when C050 gets deleted, it will be C000, C100 in order
        """
        id1 = "C000"
        id2 = "C050"
        id3 = "C100"
        self.assertTrue(id1 < id2 < id3)
        coll = ERP.RecordCollection()
        coll.addRecord(id1, "M", None, None, None, None, None, None)
        coll.addRecord(id2, "M", None, None, None, None, None, None)
        coll.addRecord(id3, "M", None, None, None, None, None, None)
        rec1 = coll.getRecord(id1)
        rec2 = coll.getRecord(id2)
        rec3 = coll.getRecord(id3)
        self.assertEqual([rec1, rec2, rec3], coll.getAllRecords())
        coll.deleteRecord(id2)
        self.assertEqual([rec1, rec3], coll.getAllRecords())


if __name__ == "__main__":
    unittest.main()
