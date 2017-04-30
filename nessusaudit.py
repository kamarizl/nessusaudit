#!/usr/bin/env python

import re

class NessusAudit():
    ''' convert nessus audit file python object '''

    def __init__(self, auditFile):
        self.auditFile = open(auditFile, 'r').readlines()


    def _elementList(self):
        ''' it return the element under <custom_item> .. </custom_item> '''
        elementList = []
        checkElementRegex = re.compile(r'^[\s](.+?):.+')
        for line in self.auditFile:
            checkElement = checkElementRegex.match(line)
            if checkElement:
                element = checkElement.group(1).lstrip()
                element = element.rstrip()
                # remove element contains '<'
                if not re.search(r'<', element):
                    if element not in elementList:
                        elementList.append(element)
        # new element for reference. it takes value from 'description'
        elementList.append('ref')
        return elementList


    def array(self):
        ''' this return list of dictionary contain all element'''
        startFlag = 99
        # temporary dict to store element
        tempDatastore = {}
        array = []
        # use to capture 'element : value'
        masterRegex = re.compile(r'^[\s](.+?):(.+)')
        elementList = self._elementList()
        for line in self.auditFile:
            # set the flag to start enumerate elemet under </custem_item>
            if re.match(r'.+(<custom_item).+', line):
                startFlag = 1           
            # if found line with </custom_item> reset the flag and start 
            # to store item in tempDatastore into actuall array
            if re.match(r'.+(</custom_item).+', line):
                startFlag = 0
                # fill empty element with value n/a
                for element in elementList:
                    if element not in tempDatastore:
                        tempDatastore[element] = "n/a"
                array.append(tempDatastore)
                tempDatastore = {} # reset datastore
            # START
            # start to collect the elements
            if startFlag == 1:
                matchLine = masterRegex.match(line)
                if matchLine:
                    # traverse all element found in audit file
                    for element in elementList:
                        if matchLine.group(1).lstrip().rstrip() == element:
                            value = matchLine.group(2).lstrip().rstrip()
                            # remove " from value
                            value = value.lstrip("\"")
                            value = value.rstrip("\"")
                            # for description contain numbering, we split it
                            if element == 'description':
                                # split number and real description
                                if re.match(r'^(\d)', value):
                                    ref = value.split(" ", 1)
                                    tempDatastore[element] = ref[1]
                                    # store the number in its keys
                                    tempDatastore["ref"] = ref[0]
                                # if description contains no numbering, just 
                                # push to temp datastore
                                else:
                                    tempDatastore[element] = value
                            else:
                                tempDatastore[element] = value
            # END
        return array


if __name__ == '__main__':
    auditFile = NessusAudit("file.audit")
    auditFile.array()
