from mesa import Agent,Model
# from pyswip import Prolog

"""Here we define the avatar with all its functionalities"""

class Agent_Avatar(Agent):
    subjects = {}
    preferences = {}

    # First Deliverable
    def __init__(self):
        print('Hello human, I am your avatar, you can configure me to be as similar to you as possible, my creators are Anthony Garcia, Sebastian Arboleda and Katherin Valencia.')

    # Second Deliverable
    def setScheduleOptions(self, subjects, preferences):
        self.subjects = subjects
        self.preferences = preferences

    def getBetterSchedule(self):
        independent, schedule = self.__isIndependent(list(self.subjects.keys()))

        print("============== BETTER WAY TO CHOOSE SUBJECTS ==============")
        score = 0
        for h in schedule:
            subject, dayTime = h
            score += dayTime[1]
            print('Subject: %s, Schedule: %s, Score: %s' % (subject, str(dayTime[0]), dayTime[1]))
        print('TOTAL SCORE: %i' % score)
        return schedule,score

    def __isIndependent(self, subjs):
        '''Determines if a set of subjects is independent'''
        subjs = self.__orderSubjects(subjs)
        if len(subjs) == 0:
            return False, []
        score, independent = self.__overlap(subjs)
                        
        return True, independent

    def __orderSubjects(self, subjs):
        ordered = []
        for sub in subjs:
            ordered.append([
                sub, self.preferences['subjects'][sub]
            ])
            ordered = sorted(ordered, key=lambda d: d[1], reverse=True)
        subs = []
        for i in ordered:
            subs.append(i[0])
        return subs

    def __overlap(self, subjs):
        return self.__recursiveOverlap([], subjs)

    def __recursiveOverlap(self, actualSchedule, subjs):
        if len(subjs) == 0:
            return 0, actualSchedule
        actualSbj = subjs[0]
        currentScore = 0
        actualScheduleCopy = actualSchedule.copy()

        for i in self.subjects[actualSbj]:
            if not self.__overlapClass(actualSchedule, i):
                newScore = self.__getScore(actualSbj, i)
                schedule = actualScheduleCopy.copy()
                schedule.append((actualSbj, (i, newScore)))
                score, schedule = self.__recursiveOverlap(schedule, subjs[1:])
                if score + newScore > currentScore:
                    actualSchedule = actualScheduleCopy.copy()
                    currentScore = score + newScore
                    actualSchedule = schedule
            score, schedule = self.__recursiveOverlap(actualSchedule, subjs[1:])
            if score > currentScore:
                actualSchedule = actualScheduleCopy.copy()
                currentScore = score
                actualSchedule = schedule
        return currentScore, actualSchedule


    def __overlapClass(self, schedulesList, actualSchedule):
        overlap = True
        for h2 in actualSchedule:
            currentOverlap = False
            for schedule in schedulesList:
                classes = schedule[1][0]
                for h1 in classes:
                    if h1[0] == h2[0]:
                        # Which one starts before
                        if h1[1] <= h2[1]:
                            first, second = h1, h2  
                        else:
                            first, second = h2, h1
                        currentOverlap = currentOverlap or first[2] > second[1]
            overlap = overlap and currentOverlap
        return overlap

    def __getScore(self, subj, schedule):
        subjScore = self.preferences['subjects'][subj]
        scheduleScore = 0.0
        for i in schedule: 
            scheduleScore += self.preferences['days'][i[0]]
        return scheduleScore/len(schedule) + subjScore

"""Test data for Second Deliverable"""

subjects = {
    "AI introduction": [[("Monday","0830","1130")], [("Friday", "0830","1130")]] ,
    "Modern SW development processes":  [[("Friday","1800","2100"), ("Saturday", "0800","1100")]],
    "Projects management":  [[("Monday","0600","0900")]],
    "UX Design": [[("Wednesday","1800","2100")]],
    "Karate":  [[("Monday","1630","1800")], [("Wednesday", "1630","1800")], [("Friday", "1630","1800")]],
    "Rest": [[("Friday","0400","0930")]]
}


preferences = {
    "subjects": {
        "AI introduction": 3,
        "Modern SW development processes": 2,
        "Projects management": 1,
        "UX Design": 1,
        "Karate": 2,
        "Rest": 3,
    },
    "days" : {
        "Monday": 2,
        "Tuesday": 4,
        "Wednesday": 4,
        "Thursday": 4,
        "Friday": 3,
        "Saturday": 1,
    },
}

"""Here we define the Model"""

class Model_Avatar(Model):
    agent = {}

    def __init__(self):
        self.agent = Agent_Avatar()

    def secondDeliverable(self):
        self.agent.setScheduleOptions(subjects, preferences)
        return self.agent.getBetterSchedule()

"""## Call for Hello World (1st Deliverable)"""

Avatar = Model_Avatar()

"""## Call for the Search Problem (2nd Deliverable)

"""

# Avatar.secondDeliverable()

# """# 3rd Deliverable"""



# prolog = Prolog()
# prolog.consult("prolog.pl")

# """Here is defined the First chronicle"""

# def isUnderstanding(subject):
#     query_args = "understood_class(%s,X)" % (subject.lower().replace(" ","_"))
#     query = list(prolog.query(query_args))
#     count = 0
#     for res in query:
#         count+= res["X"]
#     return (count/len(query)) >= 0.8

# subjects = [
#     "AI Introduction",
#     "Modern SW development processes",
#     "Projects management",
#     "UX Design"
# ]

# def calcUnderstanding():
#     response = ''
#     for i in subjects:
#         response += "Is understanding %s? %s \n" % (i, isUnderstanding(i))
#     return response

# """Here is defined the Second Chronicle"""

# def getAvailableTime():
#     query = prolog.query("week(X,Y)")
#     freeTime = {}
#     for res in query:
#         freeTime[res["X"]] = int(res["Y"])
#     return freeTime

# def printAvailableTime():
#     for week, time in getAvailableTime().items():
#         print("Available time for week %s: %i" % (week, time))

# def  addHomework(name, week, time):
#     print("Adding Homework %s..." % (name))
#     query = prolog.query("add_homework(%s,%s,%s,X)" % (name.lower().replace(" ","_"), week.lower(), str(time)))
#     for res in query:
#         print("AvailableTime: "+ str(res["X"]))

# def  completeHomework(name, time):
#     print("Completed Homework %s..." % (name))
#     query = prolog.query("complete_homework(%s,%s,X)" % (name.lower().replace(" ","_"), str(time)))
#     for res in query:
#         print("AvailableTime: "+ str(res["X"]))

# def listPendingHomeworks(week):
#     print("Pending Homeworks for week %s:" % (week))
#     query = prolog.query("homework(X,%s,Y)" % (week.lower()))
#     for res in query:
#         print("Homework: %s, Time: %s" % (res["X"],res["Y"]))

# def addHomeworks():
#     addHomework("Reading Forum", "one", 3)
#     addHomework("Task 1", "one", 3)
#     addHomework("Task 2", "one", 6)
#     addHomework("Task 3", "one", 10)
#     addHomework("Task 4", "one", 8)
#     addHomework("UX Diagram", "two", 4)
#     addHomework("Presentations ", "two", 3)
#     addHomework("PMDS Test", "three", 10)
#     addHomework("AI Agent", "four", 3)
#     addHomework("Task 5", "four", 10)
#     addHomework("Task 6", "four", 5)
#     addHomework("Task 7", "four", 4)
#     addHomework("Task 8", "four", 9)
#     addHomework("Task 9", "four", 10)
#     addHomework("Task 10", "four", 10)
#     addHomework("Delivery 3", "four", 8)

# addHomeworks()
# printAvailableTime()

# listPendingHomeworks("four")
# completeHomework("AI Agent", 8)
# listPendingHomeworks("four")

# activities = {
#     "Karate": 16,
#     "Reading": 10,
# }

# def hasEnoughFreeTime():
#     neededTime = 0
#     for act in activities.values():
#         neededTime += act
#     weeklyTime = {}
#     for week,time in getAvailableTime().items():
#         condition = time >= neededTime
#         weeklyTime[week] = condition
#     return weeklyTime

# """Here is defined the Third Chronicle"""

# weeks = ["one","two","three","four","five","six","seven"]

# def isHealthy(week):
#     weeklyTime = hasEnoughFreeTime()
#     query = list(prolog.query("weekly_health(%s,X)" % (week)))
#     score = 0
#     for res in query:
#         score += res["X"]
#     return (score) > 0 and weeklyTime[week]

# def calcWeeklyHealth():
#     for i in weeks:
#         print ("Is healthy on week %s?..." % (i))
#         print(isHealthy(i))

# """Call For first result"""

# # calcUnderstanding()

# """Call for second result"""

# # hasEnoughFreeTime()

# """Call for third result"""

# # calcWeeklyHealth()

"""# 4th deliverable

Sistemas que busca anticipar el desempeño del avatar en una actividad universitaria.

Antecedentes (Inputs)

    Worth
    Universo (ie, crisp value range): How much is the activity Worth?
    Fuzzy set (ie, fuzzy value range): poor, average, good

    Interest
    Universo (ie, crisp value range): How interesting is the activity?
    Fuzzy set (ie, fuzzy value range): poor, average, good

    Teamwork
    Universo (ie, crisp value range): How is teamwork performed? 
    Fuzzy set (ie, fuzzy value range): poor, average, good

Consecuentes (Outputs)

    Performance
    Universe: ¿Qué tan desempeño se espera en la actividad?
    Fuzzy set: low, medium, high

Reglas

    -IF the activity has a AVERAGE worth and has a AVERAGE interest and has a POOR teamwork, THEN the performance will be LOW.

    -IF the activity has a AVERAGE worth and has a POOR interest and has a POOR teamwork, THEN the performance will be LOW.

    -IF the activity has a POOR worth and has a POOR interest and has a POOR teamwork, THEN the performance will be LOW.

    -IF the activity has a GOOD worth and has a GOOD interest and has a GOOD teamwork, THEN the performance will be HIGH.

    -IF the activity has a GOOD worth and has a GOOD interest and has a AVERAGE teamwork, THEN the performance will be HIGH.

    -IF the activity has a POOR worth and has a GOOD interest and has a GOOD teamwork, THEN the performance will be MEDIUM.

    -IF the activity has a AVERAGE worth and has a GOOD interest and has a AVERAGE teamwork, THEN the performance will be HIGH.

    -IF the activity has a AVERAGE worth and has a AVERAGE interest and has a AVERAGE teamwork, THEN the performance will be HIGH.

    -IF the activity has a GOOD worth and has a GOOD interest and has a POOR teamwork, THEN the performance will be HIGH.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install -U scikit-fuzzy
# %pip install matplotlib

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
worth = ctrl.Antecedent(np.arange(0, 11, 1), 'worth')
interest = ctrl.Antecedent(np.arange(0, 11, 1), 'interest')
teamwork = ctrl.Antecedent(np.arange(0, 11, 1), 'teamwork')

performance = ctrl.Consequent(np.arange(0, 51, 1), 'performance')

# Auto-membership function population is possible with .automf(3, 5, or 7)
worth.automf(3)
interest.automf(3)
teamwork.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
performance['low'] = fuzz.pimf(performance.universe, 0, 10, 20, 30)
performance['medium'] = fuzz.pimf(performance.universe, 25, 30, 35, 40)
performance['high'] = fuzz.pimf(performance.universe, 35, 40, 50, 50)

# worth.view()

# interest.view()

# teamwork.view()

# performance.view()

rule1 = ctrl.Rule(worth['average'] & interest['average'] & teamwork['poor'], performance['low'])
rule2 = ctrl.Rule(worth['average'] & interest['poor'] & teamwork['average'], performance['low'])
rule3 = ctrl.Rule(worth['poor'] & interest['poor'] & teamwork['poor'], performance['low'])

rule4 = ctrl.Rule(worth['good'] & interest['good'] & teamwork['good'], performance['high'])
rule5 = ctrl.Rule(worth['good'] & interest['good'] & teamwork['average'], performance['high'])

rule6 = ctrl.Rule(worth['poor'] & interest['good'] & teamwork['good'], performance['medium'])
rule7 = ctrl.Rule(worth['average'] & interest['good'] & teamwork['average'], performance['medium'])
rule8 = ctrl.Rule(worth['average'] & interest['average'] & teamwork['average'], performance['medium'])
rule9 = ctrl.Rule(worth['good'] & interest['good'] & teamwork['poor'], performance['medium'])

# rule1.view()

performance_ctrl = ctrl.ControlSystem([rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

result = ctrl.ControlSystemSimulation(performance_ctrl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
# result.input['worth'] = 1
# result.input['interest'] = 1
# result.input['teamwork'] = 4
# Crunch the numbers
# result.compute()

"""# Metaverse Avatar"""

# print (result.output['performance'])
# performance.view(sim=result)