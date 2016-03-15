'''
Created on 2016/3/3

@author: kevin.sun
'''
import os
import unittest
import random
from appium import webdriver
from time import sleep
from com.kevin.TestSupport import imageSupport, genericSupport
import string

class im381ClientTests(unittest.TestCase):

    _isLoginSucceed = False
    _isLogoutSucceed = False
    _DEBUG = True
    _usrnameForSignUp = ''
    _usrnameForLogin = 'kevin'
    _usrpwdForLogin = '123456'
    testPicDir = os.path.abspath('.') + '\\screenshots'
    refPicDir = os.path.abspath('.') + '\\ref_shots'
    diffPicDir = os.path.abspath('.') + '\\diffofshots'
    
    def setUp(self):
        desired_capabilities = {}
        #desired_capabilities['language'] = 'en'
        desired_capabilities['platformName'] = 'Android'
        desired_capabilities['platformVersion'] = '4.2.2'
        desired_capabilities['deviceName'] = ''
        desired_capabilities['udid'] = '022GPLDU3B009993'
        desired_capabilities['appPackage'] = 'com.infomax.im381client'
        desired_capabilities['appActivity'] = ''
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities)
        
    
    '''clear user_data after test case done'''    
    def tearDown(self):
        self.driver.reset()
        self.driver.quit()
    
    def start_testapp(self):
        self.driver.start_activity('com.infomax.im381client', '.WelcomeActivity')
    
    
    '''Check if 'welcome' Activity would be successfully launched'''    
    def test1_WelcomePageLaunch(self):
        definedRegionForComparison = (0,50,720,1280)
        expectedActivity = '.WelcomeActivity'
        self.start_testapp()
        sleep(2)
        currentActivity = self.driver.current_activity
        self.driver.save_screenshot(self.testPicDir + '\\welcome.png')
        sleep(2)
        imageCompare = imageSupport()
        imageCompare.imageBlendComparison(self.testPicDir + '\\welcome.png', 
                                          self.refPicDir + '\\welcome.png', self.diffPicDir + '\\welcome_diff.png')
        result = imageCompare.imagePixelComparison(self.testPicDir + '\\welcome.png', 
                                              self.refPicDir + '\\welcome.png',definedRegionForComparison,0.9)
        if self._DEBUG: print 'test1_WelcomePageLaunch() --- currentActivity is: ' + currentActivity
        self.assertTrue(result and expectedActivity == currentActivity, 'testWelcomePageLaunch() --- Failed')


    '''Check if 'login' Activity would be successfully launched'''
    @unittest.skipIf(_isLoginSucceed, 'Already logged in. Skipped the test case')
    def test2_LoginActivityLaunch(self):
        expectedActivity = '.LoginActivity'
        sleep(6)
        currentActivity = self.driver.current_activity
        if self._DEBUG: print 'test2_LoginActivityLaunch() --- currentActivity is: ' + currentActivity
        self.assertSequenceEqual(expectedActivity, currentActivity, 'testLoginActivityLaunch() --- Failed')
    
    
    '''Perform account login function'''
    @unittest.skipIf(_isLoginSucceed, 'Already logged in. Skipped the test case')
    def test3_LoginFunction_with_CorrectAccountInfo(self):
        #isLoginSucceed = False
        sleep(6)
        if self.driver.current_activity == '.LoginActivity':
            '''call login() function here'''
            self.login(self._usrpwdForLogin)
            if self._DEBUG: print 'test3_LoginFunction_with_CorrectAccountInfo() --- currentActivity is: ' + self.driver.current_activity
            if self.driver.current_activity == '.MainActivity':
                self._isLoginSucceed = True
            self.assertTrue(self._isLoginSucceed)
        else:
            print 'Please logout first before performing login.'
    
    
    @unittest.skipIf(_isLoginSucceed, 'Already logged in. Skipped the test case')
    def test4_LoginFunction_with_IncorrectAccountInfo(self):
        #isLoginFailure = False
        sleep(6)
        if self.driver.current_activity == '.LoginActivity':
            '''call login() function here'''
            self.login('12345')
#             '''save captured picture to screenshots folder of current working directory'''
#             self.driver.save_screenshot(os.path.abspath('.')+'\screenshots\login_Failed.png')
            if self._DEBUG: print 'test4_LoginFunction_with_IncorrectAccountInfo() --- currentActivity is: ' + self.driver.current_activity
            if self.driver.current_activity == '.LoginActivity':
                self._isLoginSucceed = False
            self.assertFalse(self._isLoginSucceed)
        else:
            print 'Please logout first before performing login.'
    
    
    #@unittest.skipUnless(_isLoginSucceed, 'Already logged out. Skipped the test case')        
    def test5_LogoutFunction(self):
        sleep(6)
        if self.driver.current_activity == '.LoginActivity':
            self.login(self._usrpwdForLogin)
        sleep(10)
        if self.driver.current_activity == '.MainActivity':
            self.logout()
            if self.driver.current_activity == '.LoginActivity':
                self.isLogoutSucceed = True
                self.assertTrue(self.isLogoutSucceed, 'Logout failed!')
            
        else:
            print 'Please login first before performing logout.'
       
            
    def test6_SignUpFunction(self):
        sleep(8)
        self._usrnameForSignUp = string.join(random.sample(genericSupport.charList,6)).replace(" ","")
        if self._DEBUG: print 'usrnameForSignUp = ' + self._usrnameForSignUp
        if self.driver.current_activity == '.LoginActivity':
            self.driver.find_element_by_name('Sign up immediately').click()
            self.driver.find_element_by_xpath('//android.widget.EditText[contains(@index,0)]').send_keys(self._usrnameForSignUp)
            self.driver.find_element_by_xpath('//android.widget.EditText[contains(@index,2)]').send_keys('123456')
            self.driver.find_element_by_xpath('//android.widget.EditText[contains(@index,4)]').send_keys('123456')
            self.driver.find_element_by_class_name('android.widget.Button').click()
            sleep(10)
            if self._DEBUG: print 'test6_SignUpFunction() --- currentActivity is: ' + self.driver.current_activity
            self.assertSequenceEqual('.GatewayWizardActivity', self.driver.current_activity)
      
            
    def login(self, pwd):
        self.driver.find_element_by_name('Username:').send_keys(self._usrnameForLogin)
        sleep(2)
        '''use Xpath to locate element'''
        self.driver.find_element_by_xpath('//android.widget.EditText[contains(@index,2)]').send_keys(pwd)
        sleep(2)
        self.driver.find_element_by_class_name('android.widget.Button').click()
        sleep(10)
         
            
    def logout(self):
        self.driver.find_element_by_accessibility_id('More options').click()
        self.driver.find_element_by_name('Log out').click()
        self.driver.find_element_by_name('OK').click()

            
if __name__ == "__main__":
#     mLoader = unittest.TestLoader()
#     suite = mLoader.loadTestsFromTestCase(im381ClientTests)
#     unittest.TextTestRunner(verbosity=3).run(suite)
    gs = genericSupport()
    specifiedTestSuite = gs.setTestCycle(im381ClientTests('test1_WelcomePageLaunch'),1)
    
#    specifiedTestSuite.addTest(im381ClientTests('test3_LoginFunction_with_CorrectAccountInfo'))
#    specifiedTestSuite.addTest(im381ClientTests('test1_WelcomePageLaunch'))
#    specifiedTestSuite.addTest(im381ClientTests('test6_SignUpFunction'))
    unittest.TextTestRunner().run(specifiedTestSuite)
    
