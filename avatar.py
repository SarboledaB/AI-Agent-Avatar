from array import array
from mesa import Agent,Model

class Agent_Avatar(Agent):
    def __init__(self):
        print('Hello human, I am your avatar, you can configure me to be as similar to you as possible, my creators are Anthony Garcia, Sebastian Arboleda and Katherin Valencia.')

class Model_Avatar(Model):
    def __init__(self):
        agent = Agent_Avatar()

Avatar = Model_Avatar()


subjects = {
    "AI introduction": [[("Lunes","0830","1130")], [("Viernes", "0830","1130")]] ,
    "Modern SW development processes":  [[("Viernes","1800","2100"), ("Sábado", "0800","1100")]],
    "Projects management":  [[("Lunes","0600","0900")]],
    "UX Design": [[("Miércoles","1800","2100")]],
    "Karate":  [[("Lunes","1630","1800")], [("Miércoles", "1630","1800")], [("Viernes", "1630","1800")]],
    "Rest": [[("Viernes","0400","0930")]]
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
        "Lunes": 2,
        "Martes": 4,
        "Miércoles": 4,
        "Jueves": 4,
        "Viernes": 3,
        "Sábado": 1,
    },
}

def getScore(subj, schedule):
    subjScore = preferences['subjects'][subj]
    scheduleScore = 0.0
    for i in schedule: 
        scheduleScore += preferences['days'][i[0]]
    return scheduleScore/len(schedule) + subjScore

def overlap(subjs):
    return recursiveOverlap([], subjs)

def recursiveOverlap(actualSchedule, subjs):
    if len(subjs) == 0:
        return 0, actualSchedule
    actualSbj = subjs[0]
    currentScore = 0
    actualScheduleCopy = actualSchedule.copy()

    for i in subjects[actualSbj]:
        if not overlapClass(actualSchedule, i):
            newScore = getScore(actualSbj, i)
            schedule = actualScheduleCopy.copy()
            schedule.append((actualSbj, (i, newScore)))
            score, schedule = recursiveOverlap(schedule, subjs[1:])
            if score + newScore > currentScore:
                actualSchedule = actualScheduleCopy.copy()
                currentScore = score + newScore
                actualSchedule = schedule
        else:
            score, schedule = recursiveOverlap(actualSchedule, subjs[1:])
            if score > currentScore:
                actualSchedule = actualScheduleCopy.copy()
                currentScore = score
                actualSchedule = schedule
    return currentScore, actualSchedule


def overlapClass(schedulesList, actualSchedule):
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

def sub_lists (l):
    lists = [[]]
    for i in range(len(l) + 1):
        for j in range(i):
            lists.append(l[j: i])
    return lists

def orderSubjects(subjs):
    ordered = []
    for sub in subjs:
        ordered.append([
            sub, preferences['subjects'][sub]
        ])
        ordered = sorted(ordered, key=lambda d: d[1], reverse=True)
    subs = []
    for i in ordered:
        subs.append(i[0])
    return subs

def isIndependent(subjs):
    '''Determines if a set of subjects is independent'''
    subjs = orderSubjects(subjs)
    if len(subjs) == 0:
        return False, []
    score, independent = overlap(subjs)
                    
    return True, independent

def isConvenient(s):
    if len(s) >= 4:
        return isIndependent(s)
    return False, []

if __name__ == '__main__':
    s = sub_lists(list(subjects.keys()))
    validWays = []

    for x in s:
        independent, schedule = isConvenient(x)
        if independent:
            validWays.append((x, schedule))

    print("Valid ways to choose subjects: %i" % len(validWays))
    
    for c in validWays:
        print('---------------')
        score = 0
        for h in c[1]:
            subject, schedule = h
            score += schedule[1]
            print('Materia: %s, Horario: %s, Score: %s' % (subject, str(schedule[0]), schedule[1]))
        print('TOTAL SCORE: %i' % score)
        print('---------------')