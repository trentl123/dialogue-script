import time

"""
NOTE: THIS INTERPRETER IS INTENDED TO BE CHANGED AND ALTERED TO SUIT THE NEEDS OF THE USER.
"""

class DialogueScript():
    def __init__(self, filePath, respondant=None):
        # The interpreter's memory
        self.filePath = filePath # Path of the file
        self.respondant = respondant # Incase you want to embed this in something else (i.e. a game)
        self.memory = {
            "options-list": [], # The memory for the list of options the user can choose from
            "keys": {} # The memory for the interpreter's variables
        }
        self.contents = [] # All lines in the file
        for eachLine in open(self.filePath).read().splitlines():
            self.contents.append(eachLine)
            
    def indexForJumpPoint(self, point):
        count = 0
        for eachLine in self.contents:
            if eachLine.lower() == f'@ jumppoint {point}':
                return count
            count += 1
    def getVariable(self, keyName):
        return self.memory['keys'][keyName]['value']
    def getVariableType(self, keyName):
        return self.memory['keys'][keyName]['type']
    def run(self, point=1):
        self.memory['options-list'] = []
        x = self.contents[self.indexForJumpPoint(point):]
        for eachLine in x:
            if eachLine.startswith('>'):
                # Text Operator
                if eachLine.split(' ',2)[1].lower() == 'dialogue':
                    toPrint = eachLine.split(' ',2)[2]
                    if toPrint[0] in ['"', "'"]:
                        toPrint = toPrint[1:][:-1]
                    elif toPrint[0] == '#':
                        toPrint = self.getVariable(toPrint[1:])
                    print(toPrint)
                elif eachLine.split(' ',2)[1].lower() == 'jumpto':
                    self.memory['options-list'].append(eachLine)
            elif eachLine.startswith('*'):
                # Indicator Operator
                if eachLine.split(' ', 1)[1].lower() == 'end':
                    max = -1
                    for eachOption in range(len(self.memory['options-list'])):
                        max += 1
                        pr = self.memory['options-list'][eachOption].split('JumpTo ',1)[1].split(' ',1)[1]
                        if pr[0] in ['"', "'"]:
                            pr = pr[1:][:-1]
                        elif pr[0] == '#':
                            pr = self.getVariable(pr[1:])
                        print(str(eachOption)+' | '+pr)
                    choice = int(input(f"Enter number based on choice (range 0-{max})\n:> "))
                    if choice in range(len(self.memory['options-list'])):
                        p = self.memory['options-list'][choice].split(' ', 3)[2]
                        if p.lower() == 'exit':
                            return
                        else:
                            return self.run(int(self.memory['options-list'][choice].split(' ', 3)[2]))
                elif eachLine.split(' ', 2)[1].lower() == 'endat':
                    if eachLine.split(' ',2)[2].lower() == 'exit':
                        return
                    return self.run(int(eachLine.split(' ',2)[2]))
            elif eachLine.startswith('~'):
                # Functional Operator
                if eachLine.split(' ')[1].lower() == 'wait':
                    time.sleep(int(eachLine.split(' ')[2]))
                elif eachLine.split(' ')[1].lower() == 'key':
                    keyName = eachLine.split(' ')[2].strip('"')
                    keyValue = eachLine.split(' ',4)[4]
                    keyType = 'str'
                    # Test if integer
                    try:
                        keyValue = int(str(keyValue).strip(' '))
                        keyType = 'int'
                    except Exception:
                        if keyValue[0] == '"' or "'":
                            keyValue = keyValue[1:][:-1]
                    if eachLine.split(' ',4)[3].lower() == 'is':
                        self.memory['keys'][keyName] = {'value': keyValue, 'type': keyType}
                    elif eachLine.split(' ',4)[3].lower() in ['isnt', "isn't"]:
                        del self.memory['keys'][keyName]
                elif eachLine.split(' ')[1].lower() == 'increase':
                    components = eachLine.split(' ')
                    keyName = components[2]
                    by = components[3]
                    amount = components[4]
                    value = self.getVariable(keyName.strip('"'))
                    if self.getVariableType(keyName.strip('"')) == 'int' and by == 'by':
                        self.memory['keys'][keyName.strip('"')]['value'] = int(value) + int(amount)

x = DialogueScript('test.ds')
x.run()
