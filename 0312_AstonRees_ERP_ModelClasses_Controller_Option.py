# RECORDS MODEL SECTION

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
        theLength = len(self._allMyRecords)
        if 26000 <= theLength:
            raise MaxRecordsException()
        elif theLength % 500 == 0:
            print(theLength)
        i = 0
        ch = 0
        while ch < len(RecordCollection._letters):
            n = 1000
            while n < 2000:
                trial = RecordCollection._letters[ch] + str(n)[1:4]
                #  if len(self._allMyRecords) <= i:
                if theLength == i:
                    return (trial, i)
                elif self._allMyRecords[i].getID() != trial:
                    return (trial, i)
                # else:
                i += 1
                n += 1
            ch += 1

    """
    def __assumeID(self):
        theLength = len(self._allMyRecords)
        if 26000 <= theLength:
            raise MaxRecordsException()
        elif theLength == 0:
            return ("A000", 0)
        chIndex = int(theLength / 1000)
        theChar = RecordCollection._letters[chIndex]
        theNumber = (theLength % 1000)
        trial = theChar + str(theNumber + 1000)[1:4]
        if self._allMyRecords[theLength - 1].getID() == trial:
            # the next ID is guaranteed to be available
            theNumber += 1
            if theNumber == 1000:
                chIndex += 1
            trial = RecordCollection._letters[chIndex] + \
            str(theNumber + 1000)[1:4]
            return (trial, theLength)
        else:  # a lower ID is guaranteed to be available
            i = theLength - 2
            while 0 < chIndex:
                while 0 < theNumber:
                    if i <= -1:
                        return ("A000", 0)
                    trial = RecordCollection._letters[chIndex] + \
                    str(theNumber + 1000)[1:4]
                    if self._allMyRecords[i].getID() != trial:
                        return (trial, i)
    """

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
            preppedID, insertPos = self._autoID()
            # doNotUse, insertPos = self._prot_findRecord(preppedID)
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

    def getRecord(self, theID):
        try:
            trial = self._prepID(theID)
            rec, p = self._prot_findRecord(trial)
            return rec
        except InvalidIDException:
            return None

    def getAllRecords(self):
        return self._allMyRecords

    def clearRecords(self):
        self._allMyRecords = []

    def deleteRecord(self, theID):
        preppedID = self._prepID(theID)
        origRec, pos = self._prot_findRecord(preppedID)
        if origRec is not None:
            del self._allMyRecords[pos]
            return True
        else:
            return False


#CONTROL SECTION

import cmd

def safeInt(trial, default):
    result = 0
    if isinstance(default, int):
        result = default
    try:
        result = int(trial)
    except ValueError:
        pass
    return result

class ViewException(CustomException):

    def __init__(self, theReason="Not a View"):
        super(ViewException, self).__init__(theReason)


class Option(object):

    def __init__(self, newName, newOnDesc, newOffDesc):
        self._name = newName
        self._onDescription = newOnDesc
        self._offDescription = newOffDesc
        self._on = False

    def isOn(self):
        return self._on

    def turnOn(self):
        self._on = True

    def turnOff(self):
        self._on = False

    def getName(self):
        return self._name

    def getOnDescription(self):
        return self._onDescription

    def getOffDescription(self):
        return self._offDescription

class View(object):

    def show(self, message):
        print(message)


class Controller(cmd.Cmd):

    def __init__(self, newView):
        super(Controller, self).__init__()
        if not isinstance(newView, View):
            raise ViewException()
        self.prompt = "ERP "
        self._myView = newView
        self._options = {}
        self._options["AUTOID"] = Option("Auto ID", "If an invalid or \
duplicate ID is specified when adding a record, that record is assigned \
an ID automatically (a blank ID is invalid)", "No automatic IDs will be \
used when adding records")
        self._options["OVERWRITE"] = Option("Overwrite", "If a duplicate \
ID is specified when adding a record, the original record with the same \
ID is removed (this overpowers auto ID)", "No records will be removed \
when adding records")
        self._theColl = RecordCollection()
        self._selectedRecord = None
        self._selectedOption = None

    def _representRecord(self, theRecord):
        self._myView.show("ID: {}\nGENDER: {}\nAGE: {}\nSALES: {}\nBMI: {}\
\nINCOME: {}\n".format(theRecord.getID(), theRecord.getGender(),
        theRecord.getAge(), theRecord.getSales(), theRecord.getBMI(),
        theRecord.getIncome()))

    def _representOption(self, theOption):
        state = "OFF"
        if theOption.isOn():
            state = "ON"
        self._myView.show("{}: TURNED {}\n\nON: {}\nOFF: {}\n".format(
        theOption.getName(), state, theOption.getOnDescription(),
        theOption.getOffDescription()))

    def _representERP(self):
        self._myView.show("Records in ERP: {}".format\
        (len(self._theColl.getAllRecords())))

    def _enterRecordSelectedState(self):
        self._selectedOption = None
        self._myView.show("Selected Record")
        self._representRecord(self._selectedRecord)
        self._myView.show("Use the following with the appropriate argument \
to edit the record:\n+ edit_age\n+ edit_sales\n+ edit_bmi\n+ edit_income\n")

    def _enterOptionSelectedState(self):
        self._selectedRecord = None
        self._myView.show("Selected Option")
        self._representOption(self._selectedOption)
        self._myView.show("Use the following to set the option:\n+ on\n\
+ off\n")

    def _enterNeutralState(self):
        self._selectedRecord = None
        self._selectedOption = None

    def do_select_rec(self, arg):
        trial = self._theColl.getRecord(arg)
        if trial is not None:
            self._selectedRecord = trial
            self._enterRecordSelectedState()
        else:
            self._myView.show("There is no record with that ID\n")
            self._enterNeutralState()

    def do_select_option(self, arg):
        trial = arg.upper()
        if trial in self._options:
            self._selectedOption = self._options[trial]
            self._enterOptionSelectedState()
        else:
            self._myView.show("There is no option\n")
            self._enterNeutralState()

    def do_add_rec(self, arg):
        self._enterNeutralState()
        recArgs = arg.split(" ")
        if 6 <= len(recArgs):
            try:
                self._theColl.addRecord(recArgs[0], recArgs[1],
                int(recArgs[2]), int(recArgs[3]), recArgs[4], int(recArgs[5]),
                self._options["AUTOID"].isOn(),
                self._options["OVERWRITE"].isOn())
            except CustomException as e:
                self._myView.show("EXCEPTION: " + str(e) + "\n")
            else:
                self._myView.show("Record added\n")
                self._representERP()
        else:
            self._myView.show("Not enough arguments were specified\n")

    def do_edit_age(self, arg):
        if self._selectedRecord is not None:
            self._selectedRecord.setAge(int(arg))
            self._enterRecordSelectedState()
        else:
            self._myView.show("No record selected")
            self._enterNeutralState()

    def do_edit_sales(self, arg):
        if self._selectedRecord is not None:
            self._selectedRecord.setSales(int(arg))
            self._enterRecordSelectedState()
        else:
            self._myView.show("No record selected")
            self._enterNeutralState()

    def do_edit_bmi(self, arg):
        if self._selectedRecord is not None:
            self._selectedRecord.setBMI(arg)
            self._enterRecordSelectedState()
        else:
            self._myView.show("No record selected")
            self._enterNeutralState()

    def do_edit_income(self, arg):
        if self._selectedRecord is not None:
            self._selectedRecord.setIncome(int(arg))
            self._enterRecordSelectedState()
        else:
            self._myView.show("No record selected")
            self._enterNeutralState()

    def do_on(self, arg):
        if self._selectedOption is not None:
            self._selectedOption.turnOn()
            self._enterOptionSelectedState()
        else:
            self._myView.show("No option selected")
            self._enterNeutralState()

    def do_off(self, arg):
        if self._selectedOption is not None:
            self._selectedOption.turnOff()
            self._enterOptionSelectedState()
        else:
            self._myView.show("No option selected")
            self._enterNeutralState()

    def do_neutral(self, arg):
        self._enterNeutralState()
        self._representERP()

    def do_exit(self, arg):
        if self._selectedRecord is not None or \
        self._selectedOption is not None:
            self._enterNeutralState()
            self._representERP()
        else:
            self._myView.show("END")
            input()
            return True


Controller(View()).cmdloop()

# TEST DATA
"""
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

def doInput(b):
    if b:
        input()

stall = False
"""