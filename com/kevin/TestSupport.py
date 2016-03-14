'''
Created on 2016/3/4

@author: kevin
'''

from PIL import Image
from PIL import ImageChops
import unittest

class genericSupport(object):
    
    charList = ['a','b','c','d','e','f','g','h','i','j','k','l', \
                'm','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
   
    # A method to set testing rounds for certain testing case.	
    def setTestCycle(self, testcase, count=1):
        suite = unittest.TestSuite()
        for i in range(0,count):
            suite.addTest(testcase)
            i+=1
        return suite   

class imageSupport(object):
    
    _DEBUG = True
    
    def getImage(self, path):
        img = Image.open(path)
        return img
    
    # A method to show the picture differences by blending reference image and actual snapshot.
    def imageBlendComparison(self, testImgPath, refImgPath, diffPath, alpha=0.5):
        testImg = self.getImage(testImgPath)
        refImg = self.getImage(refImgPath)
        tmpImg = ImageChops.invert(testImg)
        Image.blend(refImg, tmpImg, alpha).save(diffPath)

    # A method to make pixel comparison between reference image and acutal snapshot.
    def imagePixelComparison(self, testImgPath, refImgPath, region=None, percent=1.0):
        if region is None:
            testImg = self.getImage(testImgPath)
            refImg = self.getImage(refImgPath)
    
            diffPixelCount = 0
            testImg_width = testImg.size[0]
            testImg_height = testImg.size[1]
            
            refImg_width = refImg.size[0]
            refImg_height = refImg.size[1]
            
            if testImg_width != refImg_width:
                return False
            
            if testImg_height != refImg_height:
                return False
            
            for i in range(0,refImg_width):
                for j in range(0,refImg_height):
                    if testImg.getpixel((i,j)) != refImg.getpixel((i,j)):
                        diffPixelCount += 1
            
            totalPixelCount = testImg_height * refImg_width
            diffPercent = float(diffPixelCount)/float(totalPixelCount)
            if self._DEBUG : print 'Total pixel is: ' + str(totalPixelCount) + '  Different pixel is: ' + \
                            str(diffPixelCount) + '  Diff percent is: ' + str(diffPercent)
            return percent <= 1.0 - diffPercent
        
        else:
            croppedTestPicRegion = self.getImage(testImgPath).crop(region)
            croppedRefPicRegion = self.getImage(refImgPath).crop(region)
            diffPixelCount = 0
            testImg_width = croppedTestPicRegion.size[0]
            testImg_height = croppedTestPicRegion.size[1]
            
            refImg_width = croppedRefPicRegion.size[0]
            refImg_height = croppedRefPicRegion.size[1]
            
            if testImg_width != refImg_width:
                return False
            
            if testImg_height != refImg_height:
                return False
            
            for i in range(0,refImg_width):
                for j in range(0,refImg_height):
                    if croppedTestPicRegion.getpixel((i,j)) != croppedRefPicRegion.getpixel((i,j)):
                        diffPixelCount += 1
            
            totalPixelCount = testImg_height * refImg_width
            diffPercent = float(diffPixelCount)/float(totalPixelCount)
            if self._DEBUG : print 'Total pixel is: ' + str(totalPixelCount) + '  Different pixel is: ' + \
                            str(diffPixelCount) + '  Diff percent is: ' + str(diffPercent)
            return percent <= 1.0 - diffPercent
            
