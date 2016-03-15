import cmd
import sys
import matplotlib.pyplot as viewPlot

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
        trial = None
        if isinstance(newAge, int):
            trial = newAge
        elif isinstance(newAge, str):
            try:
                trial = int(newAge)
            except ValueError:
                pass
        if trial is not None and (0 <= trial <= 99):
            self._age = trial

    def setSales(self, newSales):
        trial = None
        if isinstance(newSales, int):
            trial = newSales
        elif isinstance(newSales, str):
            try:
                trial = int(newSales)
            except ValueError:
                pass
        if trial is not None and (0 <= trial <= 999):
            self._sales = trial

    def setBMI(self, newBMI):
        if isinstance(newBMI, str) and (Record._enumBMI.hasKey(newBMI)):
            self._bmi = Record._enumBMI.getValue(newBMI)

    def setIncome(self, newIncome):
        trial = None
        if isinstance(newIncome, int):
            trial = newIncome
        elif isinstance(newIncome, str):
            try:
                trial = int(newIncome)
            except ValueError:
                pass
        if trial is not None and (0 <= trial <= 999):
            self._income = trial

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


#  CONTROL SECTION

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


class InsufficientArgumentsException(CustomException):

    def __init__(self, theReason="Not Enough Arguments Provided"):
        super(InsufficientArgumentsException, self).__init__(theReason)


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

    def __init__(self, message=None):
        if message is not None:
            print(message)

    def show(self, message):
        print(message)

    def stall(self):
        input("- Enter to continue -")

    def barChart(self, labels, values):

        viewPlot.bar(range(len(labels)), values)
        viewPlot.show()

    def pieChart(self, data):
        if isinstance(data, list):
            theLabels = []
            theValues = []
            for d in data:
                if isinstance(d, tuple) and len(d) == 2:
                    l, v = d
                    theLabels.append(l)
                    theValues.append(v)
            viewPlot.pie(theValues, labels=theLabels)
            viewPlot.show()


class Controller(cmd.Cmd):

    def __init__(self, newView, newRecordColl=None):
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
        self._options["STALL"] = Option("Stall", "ERP view stalls (waits for \
your acknowledgement) in some activities", "ERP view flows naturally")
        if (newRecordColl is not None and
                isinstance(newRecordColl, RecordCollection)):
            self._theColl = newRecordColl
        else:
            self._theColl = RecordCollection()
        self._selectedRecord = None
        self._selectedOption = None
        self._myView.show("EMPLOYEE RECORD PROGRAM - ")

    def _add(self, data):
        recArgs = data.split(" ")
        if 6 <= len(recArgs):
            self._theColl.addRecord(recArgs[0], recArgs[1], recArgs[2],
                                    recArgs[3], recArgs[4], recArgs[5],
                                    self._options["AUTOID"].isOn(),
                                    self._options["OVERWRITE"].isOn())
        else:
            raise InsufficientArgumentsException()

    def _stall(self):
        if self._options["STALL"].isOn():
            self._myView.stall()

    def _representRecord(self, theRecord):
        self._myView.show("ID: {}\nGENDER: {}\nAGE: {}\nSALES: {}\nBMI: {}\
\nINCOME: {}\n".format(theRecord.getID(), theRecord.getGender(),
                       theRecord.getAge(), theRecord.getSales(),
                       theRecord.getBMI(), theRecord.getIncome()))

    def _representOption(self, theOption):
        state = "OFF"
        if theOption.isOn():
            state = "ON"
        self._myView.show("{}: TURNED {}\n. . .\nON: {}\nOFF: {}\n\n\
".format(theOption.getName(), state, theOption.getOnDescription(),
         theOption.getOffDescription()))

    def _representERP(self):
        self._myView.show("Records in ERP: {}\
".format(len(self._theColl.getAllRecords())))

    def _enterRecordSelectedState(self):
        self._selectedOption = None
        self._myView.show("Selected Record")
        self._representRecord(self._selectedRecord)
        self._stall()
        self._myView.show("Use the following with the appropriate argument \
to edit the record:\n+ edit_age\n+ edit_sales\n+ edit_bmi\n+ edit_income\n")

    def _enterOptionSelectedState(self):
        self._selectedRecord = None
        self._myView.show("Selected Option")
        self._representOption(self._selectedOption)
        self._stall()
        self._myView.show("Use the following to set the option:\n+ on\n\
+ off\n")

    def _enterNeutralState(self):
        self._selectedRecord = None
        self._selectedOption = None

    def do_view_records(self, arg):
        """
        View all the records
        """
        allRecords = self._theColl.getAllRecords()
        result = ""
        for r in allRecords:
            result += "{} {} {} {} {} {}\n".format(r.getID(), r.getGender(),
                                                   r.getAge(), r.getSales(),
                                                   r.getBMI(), r.getIncome())
        self._myView.show(result)

    def do_view_options(self, arg):
        """
        View the options and their purpose
        """
        result = ""
        for code in self._options:
            self._myView.show("Option Code: {}".format(code))
            self._representOption(self._options[code])

    def do_graphic_gender_pie_chart(self, arg):
        """
        Graphic: Pie chart representing gender ratio of employee records
        """
        mCount = 0
        fCount = 0
        allRecords = self._theColl.getAllRecords()
        for r in allRecords:
            if r.getGender() == "M":
                mCount += 1
            elif r.getGender() == "F":
                fCount += 1
        self._myView.pieChart([("Males", mCount), ("Females", fCount)])

    def do_graphic_age_bar_chart(self, arg):
        """
        Graphic: Bar chart representing number of people per age group
        arg1: Lowest age (default 0)
        arg2: Highest age (default 100)
        arg3: Size of each age group (default 5)
        The arguments are optional, for example if you only enter one
        argument then that is the lowest age
        """
        start = 0
        end = 100
        interval = 5
        spec = arg.split(" ")
        if 2 < len(spec):
            trial = safeInt(spec[2], interval)
            if trial != 0:
                interval = trial
        if 1 < len(spec):
            end = safeInt(spec[1], end)
        if 0 < len(spec):
            start = safeInt(spec[0], start)
        limits = []
        ageCount = []
        for i in range(start, end, interval):
            limits.append(i)
            ageCount.append(0)
        allRecords = self._theColl.getAllRecords()
        for r in allRecords:
            a = r.getAge()
            lastLimit = None
            k = 0
            while k < len(limits) and limits[k] < a:
                lastLimit = k
                k += 1
            if lastLimit is not None:
                ageCount[lastLimit] += 1
        self._myView.barChart(limits, ageCount)

    def do_select_rec(self, arg):
        """
        Select a record by ID, for inspection and editing
        arg: The ID of the existing record

        """
        trial = self._theColl.getRecord(arg)
        if trial is not None:
            self._selectedRecord = trial
            self._enterRecordSelectedState()
        else:
            self._myView.show("There is no record with that ID\n")
            self._enterNeutralState()

    def do_select_option(self, arg):
        """
        Select an option for turning on/off, and seeing what it will do
        arg: The option code
        For option codes, please command view_options
        """
        trial = arg.upper()
        if trial in self._options:
            self._selectedOption = self._options[trial]
            self._enterOptionSelectedState()
        else:
            self._myView.show("There is no option\n")
            self._enterNeutralState()

    def do_text_load(self, arg):
        """
        Load records from a text file; depending on their IDs and the options,
        ERP will attempt to append all records to the collection
        arg: The loaction of the text file
        """
        self._enterNeutralState()
        try:
            theFile = open(arg, 'r')
            theLines = theFile.readlines()
            theFile.close()
            added = 0
            report = ""
            for i in range(len(theLines)):
                data = ""
                if 0 < len(theLines[i]) and theLines[i][-1] == '\n':
                    data = theLines[i][0:-1]
                else:
                    data = theLines[i]
                try:
                    self._add(data)
                except CustomException as e:
                    report += "BAD LINE {}: {}\n".format(i + 1, str(e))
                else:
                    added += 1
        except IOError as e:
            self._myView.show("EXCEPTION: {}\n".format(str(e)))
        else:
            self._myView.show("Records Added: {}\nProblems: \n{}\n\
".format(added, report))
        self._stall()

    def do_text_save(self, arg):
        """
        Save records to a text file
        arg: The location of the text file
        Please specify a non existing file
        """
        import os
        if not os.path.isfile(arg):
            try:
                theFile = open(arg, 'w')
                theLines = []
                allRecords = self._theColl.getAllRecords()
                total = len(allRecords)
                for i in range(total):
                    r = allRecords[i]
                    asStr = "{} {} {} {} {} {}".format(r.getID(),
                                                       r.getGender(),
                                                       r.getAge(),
                                                       r.getSales(),
                                                       r.getBMI(),
                                                       r.getIncome())
                    if i < (total - 1):
                        asStr += "\n"
                    theLines.append(asStr)
                theFile.writelines(theLines)
                theFile.close()
            except IOError as e:
                self._myView.show("EXCEPTION: {}\n".format(str(e)))
            else:
                self._myView.show("Saved As Text")
            self._stall()
        else:
            self._myView.show("Will not overwrite an existing file\n\
Please, enter a new file when using serial_save\n")
        self._enterNeutralState()

    def do_serial_load(self, arg):
        """
        Instructions for loading a serial record collection as the ERP starts
        """
        myView.show("++ APPLIES TO SERIAL COLLECTION, NOT TEXT ++\n\
When starting ERP via the command line, enter the argument\
\n    COLL:[file location]\nERP will then attempt to load the collection \
from that\n")

    def do_serial_save(self, arg):
        """
        Save records as serial data
        arg: The location of the text file
        Please specify a non existing file
        For instructions on loading serial data, please command serial_load
        """
        import pickle
        import os
        if not os.path.isfile(arg):  # protection from overwriting files
            try:
                with open(arg, 'wb') as f:
                    pickle.dump(self._theColl, f)
            except IOError as e:
                self._myView.show("EXCEPTION: {}\n".format(str(e)))
        else:
            self._myView.show("Will not overwrite an existing file\n\
Please, enter a new file when using serial_save\n")
        self._enterNeutralState()

    def do_add_rec(self, arg):
        """
        Add a record to the collection
        Separate each argument with a space
        arg 1: ID [A-Z][0-9]{3}
        arg 2: Gender (M|F)
        arg 3: Age [0-9]{2}
        arg 4: Sales [0-9]{3}
        arg 5: BMI (Normal|Overweight|Obesity|Underweight)
        arg 6: Income [0-9]{2,3}
        """
        self._enterNeutralState()
        try:
            self._add(arg)
        except CustomException as e:
            self._myView.show("EXCEPTION: {}\n".format(str(e)))
        else:
            self._myView.show("Record added\n")
        self._stall()

    def do_edit_age(self, arg):
        """
        A record must be selected
        Change the age of the record
        arg: [0-9]{2}
        """
        if self._selectedRecord is not None:
            self._selectedRecord.setAge(int(arg))
            self._enterRecordSelectedState()
        else:
            self._myView.show("No record selected")
            self._enterNeutralState()

    def do_edit_sales(self, arg):
        """
        A record must be selected
        Change the sales of the record
        arg: [0-9]{3}
        """
        if self._selectedRecord is not None:
            self._selectedRecord.setSales(int(arg))
            self._enterRecordSelectedState()
        else:
            self._myView.show("No record selected")
            self._enterNeutralState()

    def do_edit_bmi(self, arg):
        """
        A record must be selected
        Change the BMI of the record
        arg: (Normal|Overweight|Obesity|Underweight)
        """
        if self._selectedRecord is not None:
            self._selectedRecord.setBMI(arg)
            self._enterRecordSelectedState()
        else:
            self._myView.show("No record selected")
            self._enterNeutralState()

    def do_edit_income(self, arg):
        """
        A record must be selected
        Change the income of the record
        arg: [0-9]{3}
        """
        if self._selectedRecord is not None:
            self._selectedRecord.setIncome(int(arg))
            self._enterRecordSelectedState()
        else:
            self._myView.show("No record selected")
            self._enterNeutralState()

    def do_on(self, arg):
        """
        An option must be selected
        Turn the option on
        """
        if self._selectedOption is not None:
            self._selectedOption.turnOn()
            self._enterOptionSelectedState()
        else:
            self._myView.show("No option selected")
            self._enterNeutralState()

    def do_off(self, arg):
        """
        An option must be selected
        Turn the option off
        """
        if self._selectedOption is not None:
            self._selectedOption.turnOff()
            self._enterOptionSelectedState()
        else:
            self._myView.show("No option selected")
            self._enterNeutralState()

    def do_neutral(self, arg):
        """
        Put the control of ERP in a neutral state
        """
        self._enterNeutralState()
        self._representERP()

    def do_exit(self, arg):
        """
        If a record or an option is selected, ERP enters a neutral state
        Otherwise, ERP ends
        """
        if (self._selectedRecord is not None or
                self._selectedOption is not None):
            self._enterNeutralState()
            self._representERP()
        else:
            self._myView.show("END")
            return True

    def do_help(self, arg):
        """
        Special help
        """
        super(Controller, self).do_help(arg)


# ARGUMENT METHODS

def serialLoad(arg):
    report = ""
    import pickle
    x = None
    try:
        with open(arg, 'rb') as f:
            x = pickle.load(f)
    except IOError as e:
        report = "Failed to do serial load: {}\n".format(str(e))
    except AttributeError as e:
        report += "Failed to do serial load: {}\n".format(str(e))
    if isinstance(x, RecordCollection):
        report += "Serial load of record collection successful\n"
        return (x, report)
    else:
        return (None, report)


if __name__ == "__main__":
    report = ""
    existingColl = None
    for a in sys.argv:
        if a.upper()[0:5] == "COLL:":
            existingColl, report = serialLoad(a[5:])
    Controller(View(report), existingColl).cmdloop()
