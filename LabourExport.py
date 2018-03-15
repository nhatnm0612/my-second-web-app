import locale
import datetime
from bson import ObjectId

    
class LabourExportClass:

    
    def __init__(self, class_name, students = None):
        self.class_name   = class_name 
        if students       ==  None:
            self.students = []
        else:
            self.students = students

    def new_student(self, student):
        self.students.append(student)

    def sort(self, by):
        if len(self.students) > 0:
            if by == "name":
                locale.setlocale(locale.LC_ALL, "")
                names = {}
                given = []
                for student in self.students:
                    names[student.sortname()] = (student.age(), student.fullname(), student.DOB, student.gender, student.certificate, student.ID)
                given = sorted(names, key = locale.strxfrm)
                return given, names
            elif by == "age":
                nameage = []
                for student in self.students:
                    nameage.append((student.age(), student.fullname(), student.DOB, student.gender, student.certificate, student.ID))
                nameage.sort()
                return nameage
        else:
            if by == "name":
                return [],{}
            else:
                return []

    def classify(self, by):
        if by         == "gender":
            genders    = dict()
            for student in self.students:
                genders[student.gender.capitalize()] = genders.get(student.gender.capitalize(), 0) + 1
            labels  = []
            sizes   = []
            for key, val in genders.items():
                labels.append(key)
                sizes.append(val)
            if len(self.students) > 0:
                l       = [0] * len(labels)
                l[-1]   = 0.1
            else: l = ()
            explode = tuple(l)
            return labels, sizes, explode
        elif by == "certificate":
            certificates = dict()
            for student in self.students:
                certificates[student.certificate.capitalize()] = certificates.get(student.certificate.capitalize(), 0) + 1
            labels  = []
            sizes   = []
            for key, val in certificates.items():
                labels.append(key)
                sizes.append(val)
            if len(self.students) > 0:
                l       = [0] * len(labels)
                l[-1]   = 0.1
            else: l = ()
            explode = tuple(l)
            return labels, sizes, explode
        elif by == "birth month":
            birth = dict()
            data  = {1: "01. January", 2: "02. February", 3: "03. March", 4: "04. April",
                     5: "05. May", 6: "06. June", 7: "07. July", 8: "08. August",
                     9: "09. September", 10: "10. October", 11: "11. November", 12: "12. December"}
            for student in self.students:
                birth[data[student.month]] = birth.get(data[student.month], 0) + 1
            return birth

    def filter_by(self, filter_value, by):
        MATCH = []
        if by.lower() == "gender":
            for student in self.students:
                if student.gender == filter_value.lower():
                    MATCH.append((student.age(), student.fullname(), student.DOB, student.gender, student.certificate, student.ID))
        elif by.lower() == "certificate":
            for student in self.students:
                if student.certificate.lower() == filter_value.lower():
                    MATCH.append((student.age(), student.fullname(), student.DOB, student.gender, student.certificate, student.ID))
        elif by.lower() == "age":
            for student in self.students:
                if student.age() == int(filter_value):
                    MATCH.append((student.age(), student.fullname(), student.DOB, student.gender, student.certificate, student.ID))
        elif by.lower() == "name":
            for student in self.students:
                if filter_value.lower() in student.fullname().lower():
                    MATCH.append((student.age(), student.fullname(), student.DOB, student.gender, student.certificate, student.ID))
        return MATCH


class Student:
    

    def __init__(self, family_name, given_name, gender, DOB, certificate, ID = None):
        ## DOB format: YYYY-MM-DD
        self.family_name = family_name
        self.given_name  = given_name
        if gender.lower() in ["m", "male"]:
            self.gender  = "male"
        elif gender.lower() in ["f", "female"]:
            self.gender  = "female"
        self.DOB         = DOB
        self.year        = int(self.DOB.split("-")[0])
        self.month       = int(self.DOB.split("-")[1])
        self.date        = int(self.DOB.split("-")[2])
        self.certificate = certificate.lower()
        self.ID          = str(ID)

    def __repr__(self):
        return "Student(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(self.family_name,
                                                                        self.given_name,
                                                                        self.gender,
                                                                        self.DOB,
                                                                        self.certificate)

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def age(self):
        this_year        = datetime.datetime.today().year
        return this_year - self.year

    def fullname(self):
        return "{} {}".format(self.family_name, self.given_name)

    def sortname(self):
        return "{} {}".format(self.given_name, self.family_name)

    def to_json(self):
        return {"FamilyName": self.family_name,
                "GivenName": self.given_name,
                "Gender": self.gender,
                "DateOfBirth": self.DOB,
                "Certificate": self.certificate,
                "CreationDate": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = 7)))}
