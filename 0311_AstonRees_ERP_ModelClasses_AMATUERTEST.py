# TEST BRO

class CustomException(Exception):

    def __init__(self, theReason=""):
        self._reason = theReason

    def __str__(self):
        return repr(self._reason)


class InvalidGenderException(CustomException):

    def __init__(self, theReason="Invalid Gender"):
        super(InvalidGenderException, self).__init__(theReason)


class StringException(CustomException):

    def __init__(self, theReason="Supplied Variable is not a String"):
        super(StringException, self).__init__(theReason)


class InvalidIDException(CustomException):

    def __init__(self, theReason="Invalid ID"):
        super(InvalidIDException, self).__init__(theReason)


class DuplicateIDException(CustomException):

    def __init__(self, theReason="ID Already Taken"):
        super(DuplicateIDException, self).__init__(theReason)


class EnumException(CustomException):

    def __init__(self, theReason="Enum not Committed"):
        super(EnumException, self).__init__(theReason)


class MaxRecordsException(CustomException):

    def __init__(self, theReason="ERP has the Maximum Amount of Records"):
        super(MaxRecordsException, self).__init__(theReason)


def typeCheckStringERR(*trials):
    for t in trials:
        if not (isinstance(t, str)):
            raise StringException()


class StringEnum(object):

    def __init__(self):
        self._values = {}
        self._default = None
        self._committed = False

    def addValue(self, newString):
        typeCheckStringERR(newString)
        if (not self._committed) and (newString.upper() not in self._values):
            self._values[newString.upper()] = newString

    def commit(self, default):
        typeCheckStringERR(default)
        if (not self._committed) and (default.upper() in self._values):
            self._committed = True
            self._default = self._values[default.upper()]

    def getValue(self, key):
        typeCheckStringERR(key)
        if not self._committed:
            raise EnumException()
        if key.upper() in self._values:
            return self._values[key.upper()]
        else:
            return self._default

    def hasKey(self, key):
        typeCheckStringERR(key)
        if key.upper() in self._values:
            return True
        else:
            return False


class Record(object):

    _enumBMI = StringEnum()
    _enumBMI.addValue("Normal")
    _enumBMI.addValue("Overweight")
    _enumBMI.addValue("Obesity")
    _enumBMI.addValue("Underweight")
    _enumBMI.commit("Normal")

    def __init__(self, newID, newGender):
        typeCheckStringERR(newGender)
        gender = newGender.upper()
        if (gender != "M" and gender != "F"):
            raise InvalidGenderException()
        self._id = newID
        self._gender = gender
        self._age = 0
        self._sales = 0
        self._bmi = Record._enumBMI.getValue("")  # default
        self._income = 0

    def setAge(self, newAge):
        if isinstance(newAge, int) and (0 <= newAge <= 99):
            self._age = newAge

    def setSales(self, newSales):
        if isinstance(newSales, int) and (0 <= newSales <= 999):
            self._sales = newSales

    def setBMI(self, newBMI):
        if isinstance(newBMI, str) and (Record._enumBMI.hasKey(newBMI)):
            self._bmi = Record._enumBMI.getValue(newBMI)

    def setIncome(self, newIncome):
        if isinstance(newIncome, int) and (0 <= newIncome <= 999):
            self._income = newIncome

    def getID(self):
        return self._id

    def getGender(self):
        return self._gender

    def getAge(self):
        return self._age

    def getSales(self):
        return self._sales

    def getBMI(self):
        return self._bmi

    def getIncome(self):
        return self._income


class RecordCollection(object):

    _letters = []
    _letters[:] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _numerals = []
    _numerals[:] = "0123456789"

    def __init__(self):
        self._allMyRecords = []

    def _prepID(self, theID):
        typeCheckStringERR(theID)
        if len(theID) != 4:
            raise InvalidIDException()
        prep = theID.upper()
        if prep[0] not in RecordCollection._letters:
            raise InvalidIDException()
        for x in range(1, 4):
            if prep[x] not in RecordCollection._numerals:
                raise InvalidIDException()
        return prep

    def _prot_findRecord(self, theID):
        if len(self._allMyRecords) == 0:
            return (None, 0)
        else:
            low = 0
            high = len(self._allMyRecords)
            i = int(high / 2)
            while low != high:
                record = self._allMyRecords[i]
                if theID < record.getID():
                    high = i
                elif record.getID() < theID:
                    if low == i:
                        low += 1
                    else:
                        low = i
                else:  # match found
                    return (record, i)
                i = int((high + low) / 2)
            return (None, i)  # (no match, index for prospect ID)

    def _autoID(self):
        if 26000 <= len(self._allMyRecords):
            raise MaxRecordsException()
        ch = 0
        while ch < len(RecordCollection._letters):
            n = 1000
            while n < 1999:
                trial = RecordCollection._letters[ch] + str(n)[1:4]
                rec, pos = self._prot_findRecord(trial)
                if rec is None:
                    return trial
                n += 1
            ch += 1

    def addRecord(self, newID, newGender, newAge, newSales, newBMI, newIncome,
                  autoID, overwrite):
        typeCheckStringERR(newID)
        preppedID = None
        invalidID = False
        origRec = None
        insertPos = None
        overwriteSignal = 0  # will become 1 if overwriting will be used
        try:
            preppedID = self._prepID(newID)
            origRec, insertPos = self._prot_findRecord(preppedID)
        except InvalidIDException:
            invalidID = True
        if origRec is not None and overwrite:
            overwriteSignal = 1
        elif (origRec is not None or invalidID) and autoID:
            preppedID = self._autoID()
            doNotUse, insertPos = self._prot_findRecord(preppedID)
        elif origRec is not None:
            raise DuplicateIDException()
        elif invalidID:
            raise InvalidIDException()
        newRec = Record(preppedID, newGender)
        self._allMyRecords[insertPos:insertPos + overwriteSignal] = [newRec]
        newRec.setAge(newAge)
        newRec.setSales(newSales)
        newRec.setBMI(newBMI)
        newRec.setIncome(newIncome)

    def getRecords(self):
        return self._allMyRecords

    def clearRecords(self):
        self._allMyRecords = []


# TEST DATA

class Rec(object):

    count = 0

    @staticmethod
    def _(x):
        Rec.count += 1
        print("REC: " + str(Rec.count))
        print(x + "\n")


rec = Rec()._

def inspectRecord(theRecord):
    if isinstance(theRecord, Record):
        return "ID: {}\nGENDER: {}\nAGE: {}\nSALES: {}\nBMI: {}\nINCOME: \
{}\n".format(theRecord.getID(), theRecord.getGender(),
             theRecord.getAge(), theRecord.getSales(), theRecord.getBMI(),
             theRecord.getIncome())

def inspectRecordColl(theCollection):
    result = ""
    for r in theCollection:
        result += inspectRecord(r) + "\n"
    return result

rec("Expect InvalidGenderException")
try:
    r = Record(None, "k")
except InvalidGenderException as e:
    rec(str(e))

rec("Expect StringException")
try:
    r = Record(None, 4)
except StringException as e:
    rec(str(e))

_ra = Record("_ra", "m")
rec("Expect default atttibute values (age 0, sales 0, BMI Normal, income 0)")
rec(inspectRecord(_ra))
"""
rec("ID: {}\nGENDER: {}\nAGE: {}\nSALES: {}\nBMI: {}\nINCOME: {}\n".format(\
_ra.getID(), _ra.getGender(), _ra.getAge(), _ra.getSales(),\
_ra.getBMI(), _ra.getIncome()))
"""

_ra.setAge(100)
rec("Expect _ra age to remain 0 after attempting to set it to 100")
rec(str(_ra.getAge()))

_ra.setAge(99)
rec("_ra new age: {}".format(_ra.getAge()))

_ra.setAge(100)
rec("Expect _ra age to remain 99 after attempting to set it to 100")
rec(str(_ra.getAge()))

rec("_ra going throught all the BMI values")
_ra.setBMI("overWEIGHT")
rec(_ra.getBMI())
_ra.setBMI("OBESity")
rec(_ra.getBMI())
_ra.setBMI("underWEIGHT")
rec(_ra.getBMI())

_ra.setBMI("")
rec("Expect _ra BMI to remain Underweight after attempting to set it to an\
 empty string")
rec(_ra.getBMI())

coll = RecordCollection()

#  addRecord(self, newID, newGender, newAge, newSales, newBMI, newIncome,
#            autoID, overwrite):

rec("Expect InvalidIDException")
try:
    coll.addRecord("Fe", None, None, None, None, None, None, None)
except InvalidIDException as e:
    rec(str(e))

coll.addRecord("", "M", 88, 88, "Underweight", 88, True, None)
rec("Expect the first record to be added to coll to have an ID of A000\
 (automatically assigned)")
rec(inspectRecord(coll.getRecords()[0]))

rec("Expect DuplicateIDException")
try:
    coll.addRecord("a000", "F", 15, 8, "OVERWEIGHT", 45, False, False)
except DuplicateIDException as e:
    rec(str(e))

rec("Expect an entry with new ID specified as \"a000\" to get assigned \
\"A001\" due to auto ID")
coll.addRecord("a000", "F", 15, 8, "OVERWEIGHT", 45, True, False)
rec(inspectRecordColl(coll.getRecords()))

rec("Expect A001 to get overwritten")
coll.addRecord("a000", "M", 2, 2, "ObesitY", 4, False, True)
rec(inspectRecordColl(coll.getRecords()))

rec("Expect A001 to get overwritten (with autoID option also True)")
coll.addRecord("a000", "M", 90, 98, "ObesitY", 889, True, True)
rec(inspectRecordColl(coll.getRecords()))

rec("Expect MaxRecordsException")
try:
    for x in range(100):
        coll.addRecord("", "F", None, None, None, None, True, None)
except MaxRecordsException as e:
    rec(str(e))

rec("RECORDS: {}".format(len(coll.getRecords())))
