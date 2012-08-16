#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


from xml.sax.handler import ContentHandler,EntityResolver
from ValueTypeParameters import ValueTypeParameters
from Borg import Borg

class DomainValueContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theValuesMap = {}
    self.theValuesMap['threat_value'] = []
    self.theValuesMap['risk_class'] = []
    self.theValuesMap['countermeasure_value'] = []
    self.theValuesMap['severity'] = []
    self.theValuesMap['likelihood'] = []
    self.theValuesMap['capability'] = []
    self.theValuesMap['motivation'] = []
    b = Borg()
    self.configDir = b.configDir
    self.resetAttributes()

  def resolveEntity(self,publicId,systemId):
    return self.configDir + '/domainvalues.dtd'

  def values(self):
    return (self.theValuesMap['threat_value'],self.theValuesMap['risk_class'],self.theValuesMap['countermeasure_value'],self.theValuesMap['severity'],self.theValuesMap['likelihood'],self.theValuesMap['capability'],self.theValuesMap['motivation'])

  def resetAttributes(self):
    self.inDescription = 0
    self.theTypeName = ''
    self.theDescription = ''

  def startElement(self,name,attrs):
    if (name == 'description'):
      self.inDescription = 1
    elif (name == 'threat_value') or (name == 'countermeasure_value'):
      self.theName = attrs['name']
      self.theTypeName = name
    elif (name == 'capability_value'):
      self.theName = attrs['name']
      self.theTypeName = 'capability'
    elif (name == 'motivation_value'):
      self.theName = attrs['name']
      self.theTypeName = 'motivation'
    elif name == 'risk_value':
      self.theName = attrs['name']
      self.theTypeName = 'risk_class'
    elif name == 'severity_value':
      self.theName = attrs['name']
      self.theTypeName = 'severity'
    elif name == 'likelihood_value':
      self.theTypeName = 'likelihood'
      self.theName = attrs['name']

  def characters(self,data):
    if self.inDescription:
      self.theDescription = data
      self.inDescription = 0

  def endElement(self,name):
    if (name == 'threat_value') or (name == 'risk_value') or (name == 'countermeasure_value') or (name == 'severity_value') or (name == 'likelihood_value') or (name == 'capability') or (name == 'motivation'):
      p = ValueTypeParameters(self.theName,self.theDescription,self.theTypeName)
      self.theValuesMap[self.theTypeName].append(p)
      self.resetAttributes()
