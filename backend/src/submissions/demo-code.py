# id is submission id
instance = Submission.objects.get(pk = id)
# Get problem and problem_code
problem = instance.problem
problem_code = problem.problem_code
# Get the testcases
testcases = TestCase.objects.filter(problem = problem)

testcase_files = []
# Stores a list of tuple, for first is the testcase id, and second is the file name
for testcase in testcases:
	testcase_file_name = testcase.input
	testcase_file_name = str(testcase_file_name).split("/")[1].split(".")[0]
	testcase_files.append((testcase.id, testcase_file_name))

# Create the submission task
subtask = SubmissionTasks()
subtask.submission = instance
subtask.testcase = TestCase.objects.get(id = testcase_files[0][0])
""" 
Status options are: 
ACCEPTED_ANSWER = 'AC'
WRONG_ANSWER = 'WA'
RUNTIME_ERROR = 'RE'
TIME_EXCEEDED = 'TLE'
INTERNAL_ERROR = 'IE'
RUNNING = 'R'
"""
subtask.status = "WA"
# save the instance
subtask.save()