import locale
import datetime
import pandas as pd
import matplotlib.pyplot as plt


##=================================================================================##

    
class LabourExportClass:
    """
##=================================================================================##
    1.init
        __init__ method
        Ex:
        >>> c1 = LabourExportClass("Nguyen Minh Nhat", students = [s1])
        
    2.show
        showing student fullname (if any)
        Ex:
        >>> c1.show_students()
             Full name
        0 Nguyen Van A
        
    3.sort students by name, older, younger
        Ex:
        >>> c1.sort(by = "younger")
            Age        Fullname           DoB
        0    28    Nguyen Van A    1990-01-01
        
    4.insert student
        raise ValueError if student already in LabourExportClass
        Ex:
        >>> s2 = Student("Nguyen Thi", "B", "female", "1991-01-01", "University")
        >>> c1.new_student(s2)
        
    5.delete student
        raise ValueError if student not in LabourExportClass
        Ex:
        >>> c1.leave_student(s1)
        
    6.check number of students
        return 'AVAILABLE' if has student else 'NOT AVAILABLE'
        Ex1:
        >>> c1.check_status()
        Class Nguyen Minh Nhat has 1 student.
        'AVAILABLE'
        Ex2:
        >>> status = c1.check_status()
        Class Nguyen Minh Nhat has 1 student.
        >>> status
        'AVAILABLE'
        
    7.classify students by gender, certificate
        showing pie chart of gender or certificate in class
        Ex:
        >>> c1.classify(by = "gender")
        >>> c1.classify(by = "certificate")
        
    8.filter by gender, certificate, age
        yield student if has any match else None
        Ex:
        >>> for student in c1.filter_by(filter_value = "female", by = "gender"):
            print(student)
        
        Student("Nguyen Thi", "B", "female", "1991-01-01", "University")
        >>>

    9.age range:
        yield student if student.age() in age range else None
        Ex:
        >>> for student in c1.age_range_filter(minvalue = 1, maxvalue = 100):
                print(student)
                
        Student("Nguyen Thi", "B", "female", "1991-01-01", "University")
        >>>

    10.education filter:
        yield student if student.certificate >= minvalue else None
        high school < college < university < master
        >>> for student in c1.education_filter(minvalue = "high school"):
                print(student)
            
        Student("Nguyen Thi", "B", "female", "1991-01-01", "University")
        >>> for student in c1.education_filter(minvalue = "university"):
                print(student)

        Student("Nguyen Thi", "B", "female", "1991-01-01", "University")
        >>>
        
##=================================================================================##
    """

    def __init__(self, class_name, students = None):
        self.class_name   = class_name 
        if students       ==  None:
            self.students = []
        else:
            self.students = students

    def show_students(self):
        if len(self.students) > 0:
            dataframe = []
            for student in self.students:
                dataframe.append(student.fullname())
            print(pd.DataFrame(dataframe, columns = ["Fullname"]))
        else:
            raise IOError("Class {} hasn't had any student!".format(self.class_name))

    def sort(self, by):
        if len(self.students) > 0:
            if by == "name":
                locale.setlocale(locale.LC_ALL, "")
                names = {}
                given = []
                for student in self.students:
                    names[student.sortname()] = student.fullname()
                given = sorted(names, key = locale.strxfrm)
                fullname = []
                for given_name in given:
                    fullname.append(names[given_name])
                print(pd.DataFrame(fullname, columns = ["Fullname"]))
            elif by in ["older", "younger"]:
                nameage = []
                for student in self.students:
                    nameage.append((student.age(), student.fullname(), student.DOB))
                if by == "older":
                    nameage.sort()
                else:
                    nameage.sort(reverse = True)
                print(pd.DataFrame(nameage, columns = ["Age", "Fullname", "DoB"]))
            else:
                raise IOError('args "by" in ["name", "older", "younger"]')
        else:
            raise IOError("Class {} hasn't had any student!".format(self.class_name))


    def new_student(self, student):
        if student.__repr__() not in [stu.__repr__() for stu in self.students]:
            self.students.append(student)
        else:
            raise ValueError("Student {} already in class {}!!!".format(student.fullname(), self.class_name))

    def leave_student(self, student):
        if student in self.students:
            self.students.remove(student)
        else:
            raise ValueError("Student {} is not in class {}!!!".format(student.fullname(), self.class_name))

    def check_status(self):
        if len(self.students) != 0:
            status             = "AVAILABLE"
            print("Class {} has {} {}.".format(self.class_name, len(self.students), "students" if len(self.students) > 1 else "student"))
        else:
            status             = "NOT AVAILABLE"
            print("Class {} hasn't had any student yet!".format(self.class_name))
        return status

    def classify(self, by = ["gender", "certificate"]):
        if by         == "gender":
            male       = 0
            female     = 0
            for student in self.students:
                if student.gender == "male":
                    male          += 1
                else:
                    female        += 1
            labels     = ["Male", "Female"]
            sizes      = [male, female]
            explode    = (0, 0.1)
            fig1, ax1  = plt.subplots()
            fig1.patch.set_facecolor('grey')
            ax1.pie(sizes, explode = explode, labels = labels, autopct = "%1.2f%%", shadow = True, startangle = 90)
            ax1.axis("equal")
            plt.show()
        elif by == "certificate":
            certificates = dict()
            for student in self.students:
                certificates[student.certificate.capitalize()] = certificates.get(student.certificate.capitalize(), 0) + 1
            labels  = []
            sizes   = []
            for key, val in certificates.items():
                labels.append(key)
                sizes.append(val)
            l       = [0] * len(labels)
            l[-1]    = 0.1
            explode = tuple(l)
            fig1, ax1  = plt.subplots()
            fig1.patch.set_facecolor('grey')
            ax1.pie(sizes, explode = explode, labels = labels, autopct = "%1.2f%%", shadow = True, startangle = 90)
            ax1.axis("equal")
            plt.show()
        else:
            raise IOError('args "by" in ["gender", "certificate"]')

    def filter_by(self, filter_value, by = ["gender", "certificate", "age", "birth-month"]):
        match = 0
        if by == "gender":
            for student in self.students:
                if student.gender == filter_value.lower():
                    yield student
                    match += 1
        elif by == "certificate":
            for student in self.students:
                if student.certificate.lower() == filter_value.lower():
                    yield student
                    match += 1
        elif by == "age":
            for student in self.students:
                if student.age() == filter_value:
                    yield student
                    match += 1
        elif by == "birth-month":
            for student in self.students:
                if student.month == filter_value:
                    yield student
                    match += 1
        if match == 0:
            return None

    def age_range_filter(self, minvalue, maxvalue):
        match = 0
        for student in self.students:
            if student.age() in range(minvalue, maxvalue + 1):
                yield student
                match += 1
        if match == 0:
            return None

    def education_filter(self, minvalue):
        match = 0
        data = {"high school": 1,
                "college": 2,
                "university": 3,
                "master": 4}
        minvalue = data[minvalue]
        for student in self.students:
            if data[student.certificate] >= minvalue:
                yield student
                match += 1
        if match == 0:
            return None


##=================================================================================##


class Student:
    """
##=================================================================================##
    1.init
        __init__ method
        Ex:
        >>> s1 = Student("Nguyen Van", "A", "male", "1990-01-01", "Collage")
        
    2.repr
        __repr__ format for debugging
        Ex:
        >>> s1
        Student("Nguyen Van", "A", "male", "1990-01-01", "Collage")

    3.eq
        __eq__ method for compare
        if 2 __repr__ string are equal ---> return True
        else                           ---> return False 
        
    4.age
        return student age
        Ex:
        >>> # this year = 2018
        >>> print(s1.age())
        28
        
    5.fullname
        return student fullname = family_name + given_name
        Ex:
        >>> print(s1.fullname())
        'Nguyen Van A'
        
    6.sortname for sorting <Nguyen Van A # Bui Van A>
        return student sortname = given_name + full_name
        Ex:
        >>> print(s1.sortname())
        'A Nguyen Van'
        
##=================================================================================##
    """

    def __init__(self, family_name, given_name, gender, DOB, certificate):
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
        self.certificate = certificate

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
