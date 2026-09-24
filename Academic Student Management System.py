import os

# ==========================================
# CLASSES & OBJECTS
# ==========================================

class Student:
    def __init__(self, student_id, name, course):
        self.student_id = student_id
        self.name = name
        self.course = course
        self.marks = {}        # Dictionary: Subject -> Mark
        self.attendance = 0.0  # Float representing percentage

    def calculate_total(self):
        return sum(self.marks.values())

    def calculate_grade(self):
        if not self.marks:
            return "N/A"

        avg = self.calculate_total() / len(self.marks)

        # Conditional Statements
        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        else:
            return "F (Fail)"

    # Formats student data for TXT storage
    def to_txt_format(self):
        marks_str = ",".join(
            [f"{sub}:{mark}" for sub, mark in self.marks.items()]
        )
        return f"{self.student_id}|{self.name}|{self.course}|{self.attendance}|{marks_str}"

    # Parses TXT line back into a Student object
    @classmethod
    def from_txt_format(cls, line):
        parts = line.strip().split('|')

        student = cls(parts[0], parts[1], parts[2])
        student.attendance = float(parts[3])

        if parts[4]:  # If marks exist
            marks_list = parts[4].split(',')

            for item in marks_list:
                sub, mark = item.split(':')
                student.marks[sub] = float(mark)

        return student


class AcademicManagementSystem:

    def __init__(self, filename="students_record.txt"):
        self.filename = filename
        self.students = {}     # Dictionary: student_id -> Student object
        self.courses = set()   # Set for unique courses

        self.load_data()

    # ==========================================
    # FILE HANDLING & EXCEPTION HANDLING
    # ==========================================

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:

                for line in file:
                    if line.strip():

                        student = Student.from_txt_format(line)

                        self.students[student.student_id] = student
                        self.courses.add(student.course)

        except FileNotFoundError:
            # File doesn't exist yet
            pass

        except Exception as e:
            print(f"Error loading data: {e}")

    def save_data(self):
        try:
            with open(self.filename, 'w') as file:

                for student in self.students.values():
                    file.write(student.to_txt_format() + "\n")

        except IOError as e:
            print(f"Error saving data: {e}")

    # ==========================================
    # MODULES / FEATURES
    # ==========================================

    def register_student(self, student_id, name, course):

        if student_id in self.students:
            print("Error: Student ID already exists!")
            return

        new_student = Student(student_id, name, course)

        self.students[student_id] = new_student
        self.courses.add(course)

        self.save_data()

        print(f"Student {name} registered successfully!")

    def enter_marks(self, student_id, subject, mark):

        if student_id in self.students:

            self.students[student_id].marks[subject] = float(mark)

            self.save_data()

            print(f"Marks added for {self.students[student_id].name}.")

        else:
            print("Student not found.")

    def track_attendance(self, student_id, percentage):

        if student_id in self.students:

            self.students[student_id].attendance = float(percentage)

            self.save_data()

            print("Attendance updated.")

        else:
            print("Student not found.")

    def search_student(self, search_query):

        # Searching by ID or Name
        found = False

        for sid, student in self.students.items():

            if (search_query.lower() in sid.lower()
                    or search_query.lower() in student.name.lower()):

                self.print_report(student)

                found = True

        if not found:
            print("No matching student found.")

    # ==========================================
    # CORRECTED TOPPER FUNCTION
    # ==========================================

    def identify_topper(self):

        if not self.students:
            print("No students registered.")
            return

        highest_marks = -1

        # List to store all students having highest marks
        toppers = []

        for student in self.students.values():

            total = student.calculate_total()

            # New highest mark found
            if total > highest_marks:

                highest_marks = total

                # Start a new topper list
                toppers = [student]

            # Same highest mark found
            elif total == highest_marks:

                # Add the student to the topper list
                toppers.append(student)

        print("\n🏆 CLASS TOPPER(S)")
        print("------------------")

        for student in toppers:

            print(
                f"{student.name} ({student.student_id}) "
                f"with {highest_marks} total marks."
            )

    # ==========================================
    # LOW PERFORMERS
    # ==========================================

    def identify_low_performers(self):

        # List to collect multiple records
        low_performers = []

        for student in self.students.values():

            if student.calculate_grade() in ["D", "F (Fail)", "N/A"]:

                low_performers.append(student)

        print("\n--- Low Performance Alert ---")

        if not low_performers:

            print("No low performers found! Everyone is doing well.")

        else:

            for s in low_performers:

                print(
                    f"- {s.name} ({s.student_id}) : "
                    f"Grade {s.calculate_grade()}"
                )

    # ==========================================
    # PRINT STUDENT REPORT
    # ==========================================

    def print_report(self, student):

        print("\n" + "=" * 30)

        print(f"ACADEMIC REPORT: {student.name}")

        print("=" * 30)

        print(
            f"ID: {student.student_id} | "
            f"Course: {student.course}"
        )

        print(f"Attendance: {student.attendance}%")

        print("-" * 30)

        print("SUBJECT MARKS:")

        for sub, mark in student.marks.items():

            print(f"  {sub}: {mark}")

        print("-" * 30)

        print(f"Total Marks: {student.calculate_total()}")

        print(f"Final Grade: {student.calculate_grade()}")

        print("=" * 30 + "\n")


# ==========================================
# MAIN INTERACTIVE LOOP
# ==========================================

def main():

    system = AcademicManagementSystem()

    while True:

        print("\n🎓 ACADEMIC MANAGEMENT SYSTEM")

        print("1. Register Student")
        print("2. Enter Marks")
        print("3. Track Attendance")
        print("4. Search Student")
        print("5. Identify Topper")
        print("6. Identify Low Performers")
        print("7. Exit")

        choice = input("Select an option (1-7): ")

        try:

            if choice == '1':

                sid = input("Enter Student ID: ")
                name = input("Enter Name: ")
                course = input("Enter Course: ")

                system.register_student(
                    sid,
                    name,
                    course
                )

            elif choice == '2':

                sid = input("Enter Student ID: ")

                sub = input("Enter Subject: ")

                mark = float(
                    input("Enter Marks: ")
                )

                system.enter_marks(
                    sid,
                    sub,
                    mark
                )

            elif choice == '3':

                sid = input("Enter Student ID: ")

                att = float(
                    input("Enter Attendance Percentage: ")
                )

                system.track_attendance(
                    sid,
                    att
                )

            elif choice == '4':

                query = input(
                    "Enter Student ID or Name to search: "
                )

                system.search_student(query)

            elif choice == '5':

                system.identify_topper()

            elif choice == '6':

                system.identify_low_performers()

            elif choice == '7':

                print(
                    "Exiting System. "
                    "Data is saved in TXT file."
                )

                break

            else:

                print(
                    "Invalid choice. Please try again."
                )

        # Exception Handling
        except ValueError:

            print(
                "Invalid input! Please enter numeric "
                "values for marks/attendance."
            )

        except Exception as e:

            print(
                f"An unexpected error occurred: {e}"
            )


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    main()
