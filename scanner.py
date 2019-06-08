import logging as log
import re
import datetime
from pprint import pprint
from flask import Flask, render_template, request
app = Flask(__name__)

CODES = {
    "DCA" : "Jurisdiction - Specific Vehicle Class",
    "DCB" : "Jurisdiction - Specific Restriction Codes",
    "DCD" : "Jurisdiction - Specific Endorsement Codes",
    "DBA" : "Document Expiration Date",
    "DCS" : "Customer Family Name",
    "DAC" : "Customer First Name",
    "DAD" : "Customer Middle Name",
    "DBD" : "Document Issue Date",
    "DBB" : "Date of Birth",
    "DBC" : "Physical Description - Sex",
    "DAY" : "Physical Description - Eye Color",
    "DAU" : "Physical Description - Height",
    "DAG" : "Address - Street 1",
    "DAI" : "Address - City",
    "DAJ" : "Address - State",
    "DAK" : "Address - Postal Code",
    "DAQ" : "Customer ID Number",
    "DCF" : "Document Descriminator",
    "DCG" : "Country Identification",
    "DDE" : "Family Name Truncation",
    "DDF" : "First Name Truncation",
    "DDG" : "Middle Name Truncation",

    "DAH" : "Address - Street 2",
    "DAZ" : "Hair Color",
    "DCI" : "Place of Birth",
    "DCJ" : "Audit Information",
    "DCK" : "Inventory Control Number",
    "DBN" : "Alias AKA Family Name",
    "DBG" : "Alias Given Name",
    "DBS" : "Alias Suffix Name",
    "DCU" : "Name Suffix",
    "DCE" : "Physical Description - Weight Range",
    "DCL" : "Ethnicity",
    "DCM" : "Standard Vehicle Classification",
    "DCN" : "Standard Endorsement Code",
    "DCO" : "Standard Restriction Code",
    "DCP" : "Jurisdiction - Specific Vehicle Classification Description",
    "DCQ" : "Jurisdiction - Specific Endorsement Code Description",
    "DCR" : "Jurisdiction - Specific Restriction Code Description",
    "DDA" : "Compliance Type",
    "DDB" : "Card Revision Date",
    "DDC" : "HAZMAT Endorsement Expiration Date",
    "DDD" : "Limited Duration Document Indicator",
    "DAW" : "Weight Pounds",
    "DAX" : "Weight Kilo",
    "DDH" : "Under 18 until",
    "DDI" : "Under 19 until",
    "DDJ" : "Under 21 until",
    "DDK" : "Organ Donor Indicator",
    "DDL" : "Veteran Indicator"
}

LENGTHS = {
    "DBA" : 8,
    "DBB" : 8,
    "DBD" : 8,
    "DBC" : 1,
    "DAY" : 3,
    "DAU" : 6,
    "DAJ" : 2,
    "DAK" : 11
}

IS_NUMBER = {
    "DBA" : True,
    "DBB" : True,
    "DBD" : True,
    "DBC" : True,
    "DAY" : False,
    "DAU" : False,
    "DAJ" : False,
    "DAK" : False
}

EYE_COLORS = {
    "BLK" : "Black", 
    "BLU" : "Blue",
    "BRO" : "Brown",
    "GRY" : "Gray",
    "GRN" : "Green",
    "HAZ" : "Hazel",
    "MAR" : "Maroon",
    "PNK" : "Pink", 
    "DIC" : "Dichromatic", 
    "UNK" : "Unknown"
}


class Scanner(object):
    def __init__(self):
        self.data = None
        self.expiration = None
        self.last_name = None
        self.middle_name = None
        self.first_name = None
        self.document_issued_date = None
        self.date_of_birth = None
        self.gender = None
        self.eye_color = None
        self.height = None
        self.street = None
        self.city = None
        self.state = None
        self.postal_code = None
        self.customer_id = None

    def __str__(self):
        return """
data: {}
expiration: {}
last_name: {}
middle_name: {}
first_name: {}
document_issued_date: {}
date_of_birth: {}
gender: {}
eye_color: {}
height: {}
street: {}
city: {}
state: {}
postal_code: {}
customer_id: {}
        """.format(self.data, self.expiration, self.last_name,
        self.middle_name, self.first_name, self.document_issued_date,
        self.date_of_birth, self.gender, self.eye_color, self.height,
        self.street, self.city, self.state, self.postal_code,
        self.customer_id)

    def scan(self):
        self.setExpiration()
        self.setDateOfBirth()
        self.setDocumentIssuedDate()
        self.setGender()
        self.setEyeColor()
        self.setHeight()
        self.setState()
        self.setPostalCode()

    def setData(self, data):
        self.data = data
    def setExpiration(self):
        """
        DBA
        """
        num_instances = self._searchNumInstances("DBA")
        returned_data = self._getFixedNumberField("DBA", num_instances, LENGTHS["DBA"], IS_NUMBER["DBA"])
        print(returned_data)
        if returned_data is not None:
            month = returned_data[0:2]
            day = returned_data[2:4]
            year = returned_data[4:8]
            self.expiration = datetime.datetime(int(year), int(month), int(day))

    def setLastName(self):
        pass
    def setMiddleName(self):
        pass
    def setFirstName(self):
        pass
    def setDocumentIssuedDate(self):
        """
        DBD
        """
        num_instances = self._searchNumInstances("DBD")
        returned_data = self._getFixedNumberField("DBD", num_instances, LENGTHS["DBD"], IS_NUMBER["DBD"])
        if returned_data is not None:
            month = returned_data[0:2]
            day = returned_data[2:4]
            year = returned_data[4:8]
            self.document_issued_date = datetime.datetime(int(year), int(month), int(day))

    def setDateOfBirth(self):
        """
        DBB
        """
        num_instances = self._searchNumInstances("DBB")
        returned_data = self._getFixedNumberField("DBB", num_instances, LENGTHS["DBB"], IS_NUMBER["DBB"])
        if returned_data is not None:
            month = returned_data[0:2]
            day = returned_data[2:4]
            year = returned_data[4:8]
            self.date_of_birth = datetime.datetime(int(year), int(month), int(day))

    def setGender(self):
        """
        DBC
        """
        num_instances = self._searchNumInstances("DBC")
        returned_data = self._getFixedNumberField("DBC", num_instances, LENGTHS["DBC"], IS_NUMBER["DBC"])
        if returned_data is not None:
            returned_data = int(returned_data)
            if returned_data == 1:
                self.gender = "Male"
            elif returned_data == 2:
                self.gender = "Female"
            else:
                self.gender = "Unknown"
    def setEyeColor(self):
        """
        DAY
        """
        num_instances = self._searchNumInstances("DAY")
        returned_data = self._getFixedNumberField("DAY", num_instances, LENGTHS["DAY"], IS_NUMBER["DAY"])
        if returned_data is not None:
            self.eye_color = EYE_COLORS[returned_data]

    def setHeight(self):
        """
        DAU
        """
        num_instances = self._searchNumInstances("DAU")
        returned_data = self._getFixedNumberField("DAU", num_instances, LENGTHS["DAU"], IS_NUMBER["DAU"])
        if returned_data is not None:
            self.height = returned_data
    def setStreet(self):
        pass
    def setCity(self):
        pass
    def setState(self):
        """
        DAJ
        """
        num_instances = self._searchNumInstances("DAJ")
        returned_data = self._getFixedNumberField("DAJ", num_instances, LENGTHS["DAJ"], IS_NUMBER["DAJ"])
        if returned_data is not None:
            self.state = returned_data
    def setPostalCode(self):
        """
        DAK
        """
        num_instances = self._searchNumInstances("DAK")
        returned_data = self._getFixedNumberField("DAK", num_instances, LENGTHS["DAK"], IS_NUMBER["DAK"])
        if returned_data is not None:
            returned_data = returned_data.strip()
            if len(returned_data) == 9:
                self.postal_code = returned_data[0:5] + "-" + returned_data[5:]
            else:
                self.postal_code = returned_data

    def setCustomerId(self):
        pass

    def _searchNumInstances(self, keyword):
        numInstances = self.data.count(keyword)
        if numInstances == 0:
            log.warning("No instances of {} found.".format("DBA"))
        elif numInstances > 1:
            log.warning("Multiple instances of {} found in {}".format(keyword, self.data))
        return numInstances
    def _getFixedNumberField(self, field, num_instances, length, is_number):
        if num_instances == 0:
            return None
        elif num_instances == 1:
            index = self.data.find(field)
            return self.data[index + len(field) : index + len(field) + length]
        else:
            last_index = 0
            curr_index = 0
            for _ in range(num_instances):
                last_index = curr_index + 1
                curr_index = self.data.find(field, last_index)
                chunk = self.data[curr_index + len(field): curr_index + len(field) + length]
                if field == "DAY":
                    if chunk in EYE_COLORS.keys():
                        return chunk
                else:
                    if is_number and chunk.isdecimal():
                        return chunk
                    elif not is_number and chunk.isalnum():
                        return chunk
            return None

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        s = Scanner()
        data = request.form['paragraph_text'].replace("\n", " ")
        if len(data) < 20:
            log.warning("WARNING: data is less than 20 characters. Here is the data\n{}".format(data))
        s.data = data
        s.scan()
        print(s)
        
    return render_template("home.html")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
