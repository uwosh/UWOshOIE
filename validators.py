from Products.validation.interfaces.IValidator import IValidator

class ReferenceValidator:
    __implements__ = (IValidator,)
    def __init__(self, name="ReferenceValidator"):
        self.name = name
    def __call__(self, value, **kwargs):
        
        if len(value[0]) == 0:
            return ("You must select a program.")
        return 1
    
class isValidYearValidator:
    __implements__ = (IValidator,)
    def __init__(self, name="isValidYearValidator"):
        self.name = name
    def __call__(self, value, **kwargs):

        req = kwargs['REQUEST']
        year = req.get('programYear')

        if len(str(year)) != 4:
            return ("You must enter a valid year.")
        return 1
        
        
class isDifficultToWalkValidator:
    __implements__ = (IValidator,)
    def __init__(self, name="isDifficultToWalkValidator"):
        self.name = name
    def __call__(self, value, **kwargs):

        req = kwargs['REQUEST']
        walkingDistance = req.get('maxWalkingDistance')
        hasDifficulty = value
        
        if hasDifficulty in ["Yes", "True"] and (not walkingDistance or len(walkingDistance) == 0):
            return ("You must enter a walking distance if you have difficulty walking.")
        return 1
        
class orientationSession2hoursValidator:
    __implements__ = (IValidator,)
    def __init__(self, name="orientationSession2hoursValidator"):
        self.name = name
    def __call__(self, value, **kwargs):

        req = kwargs['REQUEST']
        willGo = value
        sessionOne = req.get('orientationHours1')
        sessionTwoDate = req.get('orientationDate2')

        if sessionOne == "3pm - 5pm":
            if willGo in ["No", "False"]:
                return ("You must specify that you will go to the session 2 orientation if you selected 3pm - 5pm for the first session.")
            elif not sessionTwoDate or len(sessionTwoDate) == 0:
                return ("You must specify a second date to go in the 'Orientation Session part 2 (Date)' field.")
        else:
            if willGo in ["Yes", "True"]:
                return ("You do not need to go to orientation session part 2 if you are going to the first four hour session")
        return 1
        
class orientationSession2DateValidator:
    __implements__ = (IValidator,)
    def __init__(self, name="orientationSession2DateValidator"):
        self.name = name
    def __call__(self, value, **kwargs):

        req = kwargs['REQUEST']
        year, month, day = value[:10].split('-')
        sessionOne = req.get('orientationHours1')

        if sessionOne == "3pm - 5pm" and (int(month) == 0 or int(day) == 0):
            return ("You must select a date to go to orientation 2 if you selected 3pm - 5pm for the first session.")
        return 1
        
class orientationConflictDateValidator:
    __implements__ = (IValidator,)
    def __init__(self, name="orientationConflictDateValidator"):
        self.name = name
    def __call__(self, value, **kwargs):

        req = kwargs['REQUEST']
        year, month, day = [0, 0, 0]
        try:
            year, month, day = req.get('conflictDate')[:10].split('-')
        except:
            pass
            
        conflict = value

        if conflict.startswith("Yes") and (int(month) == 0 or int(day) == 0):
            return ("You must select the date of your conflict.")
        return 1
        
class financialAidValidator:
    __implements__ = (IValidator,)
    def __init__(self, name="financialAidValidator"):
        self.name = name
    def __call__(self, value, **kwargs):

        req = kwargs['REQUEST']
        holdOrProcess = req.get('holdApplication')
        applyForAid = value

        if applyForAid in ["Yes", "True"] and (not holdOrProcess or len(holdOrProcess) == 0):
            return ("You must select Hold or Process is you are applying for Financial Aid.")
        elif applyForAid in ["No", "False"] and holdOrProcess == "HOLD":
            return ("Can't hold if you are not applying for Financial Aid.")
        return 1