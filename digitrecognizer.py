
from nupic.research.spatial_pooler import SpatialPooler as SP
from PIL import Image
import numpy as np
import os
import sys

class DigitRecognizer(object):
      
    def __init__(self, trainingDataDir, testingDataDir):
        self.trainingDataDir = trainingDataDir
        self.testingDataDir = testingDataDir
        self.inputShape = (28, 28)
        self.columnDimensions = (64, 64)
        self.columnNumber = np.array(self.columnDimensions).prod()
        self.inputSize = np.array(self.inputShape).prod()
        self.spatialPooler = self._initSpatialPooler()

    def _initSpatialPooler(self):

        print "Creating spatial pooler .. go check twitter"
        spatialPooler = SP(
            self.inputSize,   
            self.columnDimensions,
            potentialRadius = self.inputSize,
            numActiveColumnsPerInhArea = int(0.02*self.columnNumber),
            globalInhibition = True,
            synPermActiveInc = 0.01
        )
        print "Spatial pooler is operational."
        return spatialPooler


    def run(self):
        trainingResults = self._train()
        print "Training results: %s" % trainingResults
        testingResults = self._test(trainingResults)
        print "Testing results: %s" % testingResults
    
    def _train(self):

        trainingResults = {}

        # - For each image in the labeled training data 
        # - Present to spatial pooler
        # - Save the activecolumns returned by the spatial pooler in 
        #   results dictionary, keyed on the image label (eg, "1")
        for filename in os.listdir(self.trainingDataDir):
            if not filename.endswith("png"):
                continue

            print filename
            filenameWithPath = os.path.join(self.trainingDataDir, filename)
            image = Image.open(filenameWithPath)
            inputArray = self._convertToInputArray(image)
            activeColumns = np.zeros(self.columnNumber)

            print "Calling spatial pooler compute() with input: "
            self._prettyPrintInputArray(inputArray)

            self.spatialPooler.compute(inputArray, True, activeColumns)
            print "called compute(), activeColumns:" 
            print activeColumns.nonzero()

            trainingResults[filename] = activeColumns

            print "done spatial pooler"

        return trainingResults


    def _prettyPrintInputArray(self, inputArray):
        reshaped = inputArray.reshape(28, 28)
        print reshaped

    def _convertToInputArray(self, image):

        image = image.convert('1')  # Convert to black and white

        inputArray = np.zeros(self.inputSize, np.int8)

        # is there a slicker way to get the image data into a numpy array?
        
        imageData = image.getdata()

        i = 0
        for pixel in imageData:
            if pixel == 0:
                inputArray[i] = 1
            i += 1

        return inputArray


    def _test(self, trainingResults):
        pass


if __name__ == "__main__":
    _trainingDataDir = os.path.join("data", "training")
    _testingDataDir = os.path.join("data", "testing")
    digitRecognizer = DigitRecognizer(_trainingDataDir, _testingDataDir)
    digitRecognizer.run()

