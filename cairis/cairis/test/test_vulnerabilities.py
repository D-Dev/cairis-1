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

import unittest
import os
import json
import BorgFactory
from Borg import Borg
from VulnerabiltyParameters import VulnerabilityParameters

class VulnerabilityTest(unittest.TestCase):

  def setUp(self):
    BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/vulnerabilities.json')
    d = json.load(f)
    f.close()
    self.ienvs = d['vulnerabilities']

    
  def testStandardVulnerability(self):
    iep1 = VulnerabiltyParameters(self.ienvs[0]["theName"],self.ienvs[0]["theType"],self.ienvs[0]["theDescription"])
    iep2 = VulnerabiltyParameters(self.ienvs[1]["theName"],self.ienvs[1]["theType"],self.ienvs[1]["theDescription"])
    iep3 = VulnerabiltyParameters(self.ienvs[2]["theName"],self.ienvs[2]["theType"],self.ienvs[2]["theDescription"])
    b = Borg()
    b.dbProxy.addEnvironment(iep1)
    b.dbProxy.addEnvironment(iep2)
    b.dbProxy.addEnvironment(iep3)
    oenvs = b.dbProxy.getEnvironments()
    oep1 = oenvs[self.ienvs[0]["theName"]]
    self.assertEqual(iep1.name(), oep1.name())
    self.assertEqual(iep1.theType(),oep1.theType())
    self.assertEqual(iep1.description(),oep1.description())
    oep2 = oenvs[self.ienvs[1]["theName"]]
    self.assertEqual(iep2.name(), oep2.name())
    self.assertEqual(iep2.theType(),oep2.theType())
    self.assertEqual(iep2.description(),oep2.description())
    oep3 = oenvs[self.ienvs[2]["theName"]]
    self.assertEqual(iep3.name(), oep3.name())
    self.assertEqual(iep3.theType(),oep3.theType())
    self.assertEqual(iep3.description(),oep3.description())

    b.dbProxy.deleteEnvironment(oep1.id())
    b.dbProxy.deleteEnvironment(oep2.id())
    b.dbProxy.deleteEnvironment(oep3.id())

  def tearDown(self):
    b = Borg()
    b.dbProxy.close()

if __name__ == '__main__':
  unittest.main()
