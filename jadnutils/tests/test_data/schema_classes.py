j_schema = {
  "meta": {
    "package": "https://demo.com",
    "roots": ["Student-Info"]
  },
  "types": [
    ["Class-Options", "Enumerated", ["="], "Classes that a CS student can pick from", [
        [131, "object_oriented_programming_1", ""],
        [132, "object_oriented_programming_2", ""],
        [216, "intro_to_computer systems", ""],
        [250, "discrete_math", ""],
        [330, "programming_languages", ""],
        [351, "algorithms", ""],
        [414, "network_security", ""],
        [420, "data_structures", ""]
      ]],
    ["Academic-Standing", "Enumerated", [], "Student's current academic status", [
        [1, "good_standing", ""],
        [2, "academic_probation", ""],
        [3, "academic_warning", ""],
        [4, "suspended", ""]
      ]],
    ["Student-Classification", "Enumerated", [], "Student's year/level", [
        [1, "freshman", ""],
        [2, "sophomore", ""],
        [3, "junior", ""],
        [4, "senior", ""],
        [5, "graduate", ""]
      ]],
    ["Instructor-Info", "Record", [], "Information about the class instructor", [
        [1, "name", "String", [], ""],
        [2, "email", "String", ["/email", "[0"], ""],
        [3, "office_location", "String", ["[0"], ""],
        [4, "office_hours", "String", ["[0"], ""]
      ]],
    ["Prerequisites", "ArrayOf", ["*Class-Options"], "Required courses before enrollment", []],
    ["Semester-Classes", "ArrayOf", ["*Class-Selection", "{2", "}5", "q"], "", []],
    ["Class-Selection", "Record", [], "", [
        [1, "class", "Class-Options", [], ""],
        [2, "start_date", "String", ["/date"], ""],
        [3, "class_time", "String", ["/time"], ""],
        [4, "class_days", "Class-Days", [], ""],
        [5, "credits", "Integer", [], "waiting on JADN2 minInclusive maxInclusive functionality"],
        [6, "instructor", "Instructor-Info", [], ""],
        [7, "location", "String", [], "Building and room number"],
        [8, "section_number", "String", ["%^\\d{3}$"], "3-digit section identifier"],
        [9, "capacity", "Integer", [], "Maximum enrollment"],
        [10, "enrolled_count", "Integer", [], "Current enrollment"],
        [11, "prerequisites", "Prerequisites", ["[0"], "Required prerequisite courses"]
      ]],
    ["Days-Of-Week", "Enumerated", [], "", [
        [1, "Monday", ""],
        [2, "Tuesday", ""],
        [3, "Wednesday", ""],
        [4, "Thursday", ""],
        [5, "Friday", ""]
      ]],
    ["Class-Days", "MapOf", ["+Days-Of-Week", "*Boolean"], "", []],
    ["Student-Info", "Record", [], "Information about the student registering for classes", [
        [1, "full_name", "String", ["%^[A-Za-z]+\\s[A-Za-z]+$"], ""],
        [2, "uid", "String", ["%^\\d{9}$"], "University ID number"],
        [3, "email", "String", ["/email", "[0"], "Student email address"],
        [4, "phone", "String", ["%^\\d{3}-\\d{3}-\\d{4}$", "[0"], "Phone number"],
        [5, "majors", "String", ["[0", "]-2"], "Student's declared major - using field multiplicity"],
        [6, "minors", "String", ["[0", "]-2"], "Optional minor field of study - using field multiplicity"],
        [7, "gpa", "Number", ["[0"], "Current GPA"],
        [8, "total_credits", "Integer", ["[0"], "Total credits earned"],
        [9, "classification", "Student-Classification", ["[0"], ""],
        [10, "academic_standing", "Academic-Standing", ["[0"], ""],
        [11, "advisor_name", "String", ["[0"], "Academic advisor"],
        [12, "graduation_date", "String", ["/date", "[0"], "Expected graduation date"],
        [13, "student_token", "Binary", [], "To show binary viewer"],
        [14, "class_selections", "Semester-Classes", [], ""]
      ]]
  ]
}