
from dockerjudge import judge 
from dockerjudge.processor import Python, OpenJDK, GCC

from django.conf import settings
from django.core.cache import cache
from .models import *

import redis
# redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
from django.conf import settings

redis_client = redis.StrictRedis(host=settings.REDIS_HOST_IP, port=6379, db=0)

# StatusDict={
#     AC : 'Accepted',
#     WA : 'Wrong Answer',
#     ONF : 'Output Not Found',
#     RE : 'Runtime Error',
#     TLE : 'Time Limit Exceeded',
#     UE : 'Unknown Error',
#     CE : 'Compilation Error',
# }

def convertTextToByteCode(ipText):
    byteCode = ipText.encode('utf-8')
    return byteCode

def runGCC(code,inputs,timeLimit=1):
    op = judge(
        GCC(GCC.Language.cpp),  # or `GCC('cpp')` / `GCC('C++')`, which means compile the source code in the C++ programming language with `g++` command
        code,
        inputs,
        {
            'limit': {
                'time': timeLimit
            }
        }
    )

    return op

def runC(code,inputs,timeLimit=1):
    op = judge(
        GCC(GCC.Language.c),  
        code,
        inputs,
        {
            'limit': {
                'time': timeLimit
            }
        }
    )

    return op

def runJava(code,inputs,timeLimit=1):
    op = judge(
        OpenJDK(11),  
        code,
        inputs,
        {
            'limit': {
                'time': timeLimit+1
            }
        }
    )

    return op

def runPython(code,inputs,timeLimit=1):
    op = judge(
        Python(3),  
        code,
        inputs,
        {
            'limit': {
                'time': timeLimit+1
            }
        }
    )

    return op
    

def getInputListsWithCache(question):

    # Check if the data is already cached
    # if you used this you have make logic to delete all testcases from all vm
    cache_key = f"testcases_{question}"  # Assuming 'question' is a Django model instance
    print("from utils",cache_key)
    cached_data = cache.get(cache_key)
    if cached_data:
        print("inputs are present in cache")
        return cached_data
    
    print("inputs are not present in cache")
    

    # Data is not cached, fetch it from the database
    # implemetn api logic to fetch test cases from main db
    return []

def deleteContainerById(obj):
    container_id = obj[2].id
    containerObj = ActivatedContainer.objects.create(containerId=container_id)
    

def getAllStatus(comipledObj):
    TestCaseResult = comipledObj[0]
    print("tescase result : ",TestCaseResult)
    opDict ={
        'time':0,
        'totalTestcase':len(TestCaseResult),
    }

    timeTaken = 0

    opList=[]
    for testcase in TestCaseResult:
        status_enum = testcase[0]
        status_string = status_enum.name
        opList.append(status_string)
        # opDict['time']+=testcase[2]
        timeTaken = max(timeTaken,testcase[2])

    opDict['status'] = opList

    opDict['finalStat'] = getOutputOnPriority(opList)
    # opDict['time'] = format(opDict['time'], '.3f')
    opDict['time'] = "{:.2f}".format(timeTaken*1000 )

    deleteContainerById(comipledObj)
    return opDict


def getOneStatus(comipledObj):
    opDict={
    }
    TestCaseResult = comipledObj[0]
    singleTestCaseResult = TestCaseResult[0]

    status_enum = singleTestCaseResult[0]
    status_string = status_enum.name

    if(status_string == 'AC' or status_string == 'WA'):
        opDict ={
            'status':'AC',
            'output':singleTestCaseResult[1][0].decode('utf-8') if singleTestCaseResult[1][0] is not None else "",
            'error':singleTestCaseResult[1][1].decode('utf-8') if singleTestCaseResult[1][1] is not None else ""
        }
    else:
        if status_string == 'CE':
            rError=comipledObj[1].decode('utf-8') if comipledObj[1] is not None else ""
        else:
            rError = singleTestCaseResult[1][1].decode('utf-8') if singleTestCaseResult[1][1] is not None else ""
        opDict ={
            'status':status_string,
            'output':singleTestCaseResult[1][0].decode('utf-8') if singleTestCaseResult[1][0] is not None else "",
            'error':rError
        }

    deleteContainerById(comipledObj)
    return opDict

def getOutputOnPriority(statuses):

    # Define status priorities
    priority_order = {'CE': 0, 'RE': 1, 'TLE': 2, 'WA': 3, 'UE': 4}

    # Sort the statuses based on priority order
    sorted_statuses = sorted(statuses, key=lambda status: priority_order.get(status, float('inf')))

    # Get the status with the highest priority
    highest_priority_status = sorted_statuses[0] if sorted_statuses else None

    # print("Highest Priority Status:", highest_priority_status)
    return highest_priority_status

def solveByLang(language,byteCode,inputsList,timeLimit):
    if(language == "cpp"):
        compiledOP= runGCC(byteCode,inputsList,timeLimit)
    elif(language == "c"):
        compiledOP= runC(byteCode,inputsList,timeLimit)
    elif(language == "java"):
        compiledOP= runJava(byteCode,inputsList,timeLimit)
    elif(language == "java"):
        compiledOP= runJava(byteCode,inputsList,timeLimit)
    elif(language == "python"):
        compiledOP= runPython(byteCode,inputsList,timeLimit)


    return compiledOP

def getRCStatus(comipledObj):
    TestCaseResult = comipledObj[0]

    opList=[]
    for testcase in TestCaseResult:
        op = testcase[1][0]
        opList.append(op)


    return opList

def executeRunRc(questionId,language,inputStart,endStart,code):
    inputsList=[(convertTextToByteCode(str(i)),b'') for i in range(inputStart,endStart)]
    byteCode = convertTextToByteCode(code)
    submitOp = solveByLang(language,byteCode,inputsList,1)

    opList = getRCStatus(submitOp)
    print(submitOp)
    try:
        for i,j in  zip(range(inputStart,endStart), opList):
            redis_client.hset(questionId, i, j.decode('UTF-8'))  
            # cache.hset(questionId, i, j.decode('UTF-8'))  
        return True
    except Exception as e:
        print(e)
        return False


 
def executeSubmit(language,code,timeLimit,question):
    # inputsList = getInputLists(question)
    inputsList = getInputListsWithCache(question)
    byteCode = convertTextToByteCode(code)
    submitOp= solveByLang(language,byteCode,inputsList,timeLimit)
    print(submitOp)
    return getAllStatus(submitOp)

def execteRun(language,code,timeLimit,input):
    byteCode = convertTextToByteCode(code)
    byteInput =  convertTextToByteCode(input) if input != '' or input is not None else b''
    inputList = [ (byteInput,b'') ]
    runOp = solveByLang(language,byteCode,inputList,timeLimit)
    print(runOp)
    return getOneStatus(runOp)
    

def runCodeDockerJudge(question,code,language,isSubmitted,timeLimit=1,input_data=None):

    if not (isSubmitted):
        print("in run ",input_data)
        TC_OP = execteRun(language,code,timeLimit,input_data)
        return TC_OP

    TC_OP = executeSubmit(language,code,timeLimit,question)
    return TC_OP

