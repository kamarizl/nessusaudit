#!/usr/bin/env python

import re

class NessusAudit():
  ''' convert nessus audit file python object '''

  def __init__(self, auditFile):
    self.auditFile = open(auditFile, 'r').readlines()


  def _elementList(self):
    elementList = []
    checkElementRegex = re.compile(r'^[\s](.+?):.+')
    for line in self.auditFile:
      checkElement = checkElementRegex.match(line)
      if checkElement:
        element = checkElement.group(1).lstrip()
        element = element.rstrip()
        if not re.search(r'<', element):
          if element not in elementList:
            elementList.append(element)
    elementList.append('ref')
    return elementList


  def array(self):
    startFlag = 99
    tempDatastore = {}
    array = []

    masterRegex = re.compile(r'^[\s](.+?):(.+)')

    elementList = self._elementList()

    for line in self.auditFile:

      if re.match(r'.+(<custom_item).+', line):
        startFlag = 1
        
      # store the dictionaty in list 
      if re.match(r'.+(</custom_item).+', line):
        startFlag = 0
        
        # datastore filler with all element found
        for element in elementList:
          if element not in tempDatastore:
            tempDatastore[element] = "n/a"
        
        array.append(tempDatastore)
        tempDatastore = {} # reset datastore

      # start collect the element
      if startFlag == 1:
        matchLine = masterRegex.match(line)
        if matchLine:
          for element in elementList:
            if matchLine.group(1).lstrip().rstrip() == element:
              
              value = matchLine.group(2).lstrip().rstrip()
              value = value.lstrip("\"")
              value = value.rstrip("\"")

              if element == 'description':
                if re.match(r'^(\d)', value):
                  ref = value.split(" ", 1)
                  tempDatastore[element] = ref[1]
                  tempDatastore["ref"] = ref[0]
                else:
                  tempDatastore[element] = value
              else:
                tempDatastore[element] = value

    return array

if __name__ == '__main__':
  auditFile = NessusAudit("file.audit")
  auditFile.array()

