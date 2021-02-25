import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
#ADD IMPORT STATEMENT FOR YOUR GENERATED UI.PY FILE HERE
import Ui_Country
import math
import csv
        
#      ^^^^^^^^^^^ Change this!

#CHANGE THE SECOND PARAMETER (Ui_ChangeMe) TO MATCH YOUR GENERATED UI.PY FILE
class MyForm(QMainWindow, Ui_Country.Ui_MainWindow):
#                         ^^^^^^^^^^^   Change this!
    #Declare the following as global variables
    my2dList=[]
   
    # if the user updates values in the list this value should be toggled
    # to true...so that when they exit, they can be prompted to save their updates to the file
    # before the application closes
    unsaved_changes = False
    # DO NOT MODIFY THIS CODE
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
    # END DO NOT MODIFY
        #Hidden framebase
        self.frameBase.setVisible(False)
        
        # ADD SLOTS HERE, indented to this level (ie. inside def __init__)
        
        # slot for when the Qaction is triggered
        self.actionLoad_countries.triggered.connect(self.Loadcountries)
        # slot for when an item is selected in the list
        self.listCountries.currentRowChanged.connect(self.list_Changed)
        # slot for when the radiobutton is selected
        self.radioButtonKm.clicked.connect(self.populationKm)
        # slot for when the radiobutton is selected
        self.radioButtonMile.clicked.connect(self.populationMile)
        # slot for when the comboBox is selected
        self.comboBoxMilesKm.currentIndexChanged.connect(self.comboBoxMK)
        # slot for when the button is clicked
        self.pushButtonUpdate.clicked.connect(self.updatePopulation)
        # slot for when the Qaction is triggered
        self.actionSave_To_File.triggered.connect(self.savedata)
        # slot for when the Qaction is triggered
        self.actionExit.triggered.connect(self.exit_program)
        
    # ADD SLOT FUNCTIONS HERE
    # These are the functions your slots will point to
    # Indent to this level (ie. inside the class, at same level as def __init__)
        
        #call the function to read the country name and make framebase visible
    def Loadcountries(self):
       
        #1. Read a file & Store the file in memory
        #Use logic to check WHETHER to reload from file (ie. don't do it if the list is already filled)
        if len(self.my2dList)==0:
            self.ReadFiles()
        #2. Retrieve file contents from memory and load into the listWidget    
        self.Loadcountriesname()
        
        
        #When selecting listCountries, the data in my2DList corresponding to index will be matched, 
        # and flag and population area operations will be displayed
    def list_Changed(self,newindex):
         #show the framebase
        self.frameBase.setVisible(True)
        #Convert newindex to a global variable
        self.index=self.listCountries.currentRow()
        #Read the name of my2dList and put it in the lable    
        self.labelCountryName.setText(self.my2dList[newindex][0])    
        #Read the name of my2dList and put it in the textEdit    
        self.lineEditPopulation.setText("{:,}".format(int(self.my2dList[newindex][1])))
        
        #Read the square miles of my2dList and put it in the textEdit    
        self.labelArea_2.setText("{:.1f}".format(float(self.my2dList[newindex][2])))
   
        #Select radioButtonMile by default
        self.radioButtonMile.setChecked(True)
        #Call the pMile function to show the population density result
        self.labelDensity.setText(str(self.pMile()))
        #Call the mage_display function to show flag
        self.image_display()
        #Call the percentageOfWorld function to show the percentage Of World population
        self.labelPercentagePopulation.setText(self.percentageOfWorld())
        
        # slot for when the Exit command in the menu is clicked
        self.actionExit.triggered.connect(self.exit_program)
       
    
        #Call the populationKm function to show the population density result
    def populationKm(self) :   
        self.labelDensity.setText(str(self.pKm()))
        #Call the populationMile function to show the population density result
    def populationMile(self):
        self.labelDensity.setText(str(self.pMile()))
        #The display area is selected as square kilometers or square miles based on currentIndex
    def comboBoxMK(self,nindex):
        if self.comboBoxMilesKm.currentIndex()==0:
            self.labelArea_2.setText("{:.1f}".format(float(self.my2dList[self.index][2])))
        else :
            self.labelArea_2.setText(str(self.sqKm()))
    #call the updateQm and Determine whether the data is valid and give corresponding propmt
    def updatePopulation(self):
        self.updateQM()
        # toggle the unsaved_changes variable to True so that the program
        # prompts you to save to file when shutting down.
        self.unsaved_changes = True
        self.actionSave_To_File.setEnabled(True)

        
    def savedata(self):
        # call the save_changes_to_file helper function which does the heavy lifting
        self.save_changes_to_file()
        # popup a message to the user confirming that the changes were saved to the file
        QMessageBox.information(self, 'Saved', 'Changes were saved to the file', QMessageBox.Ok)
        # toggle the unsaved_changes variable back to False because we no longer have any unsaved changes
        self.actionLoad_countries.setEnabled(False)#Set ActionLoad -- Coutries is unenabled
        self.unsaved_changes = False
    
    def exit_program(self):
        QApplication.closeAllWindows()
        
    
#Example Slot Function
#   def SaveButton_Clicked(self):
#       Make a call to the Save() helper function here

    #ADD HELPER FUNCTIONS HERE
    # These are the functions the slot functions will call, to 
    # contain the custom code that you'll write to make your progam work.
    # Indent to this level (ie. inside the class, at same level as def __init__)
    def Loadcountriesname(self):
        #Take whatever is in memory (in 2dlist) and load it into the onscreen list widget
        self.listCountries.clear()#Clear the contents of the ListCoutuIRES before reading
        for row in self.my2dList:
            self.listCountries.addItem(row[0])

    
    def ReadFiles(self) :   
    #Open the countires file and read it's contents into memory
    #Use csv.reader to get the data
        #Open the people file and read it's contents into memory
        #Use csv.reader to get the data
        
        fileName = "Final Project/Files/countries.txt"
        accessMode = "r"        #Read mode

        with open(fileName, accessMode) as myFile:
            fileContents = csv.reader(myFile)   #Gives me something LIKE a 2d list containing the data in the file

            for row in fileContents:    #Loop through the fileContents NOT-QUITE-LIST
                self.my2dList.append(row)    #Create my own 2d list out of the csv reader object

    def pMile(self):#Calculate population density for square miles
        self.miles=float(self.my2dList[self.index][2])
        self.population=float(self.my2dList[self.index][1])
        perMiles=self.population/self.miles
        perMiles=('%.2f' % perMiles)#Take 2 decimal places
        return perMiles
    
    def sqKm(self):#Convert the unit of area to square kilometers
        km=self.miles*2.59
        self.km=('%.1f' % km)
        return self.km
    
    def pKm(self):#opulation density is measured in square kilometers   
        perKm=self.population/(self.miles*2.59)
        perKm=('%.2f' % perKm)
        return perKm
    
    def image_display(self):#Display the national flag in lableCountryFlag
        imagePath=str(self.my2dList[self.index][0])#Read country name
        image=imagePath.replace(" ","_")#Replace Spaces to "_"
        image = QPixmap("Final Project/Files/Flags/"+image)
        self.labelCountryFlag.setPixmap(image)#Display the national flag in lableCountryFlag
        
    def percentageOfWorld(self):# Calculate the value of percentage of world population
        total=0.0
        for r in range(0,len(self.my2dList)):#Count the world's population
            total+=float(self.my2dList[r][1])
        
        perOfWorld=float(self.my2dList[self.index][1])/total*100 #Calculate percentage
        perOfWorld=('%.4f' % perOfWorld)+"%"  
        return perOfWorld

    def updateQM(self):#Determine whether the data is valid and give corresponding propmt
        lineEdit=self.lineEditPopulation.text()
        #Determine if the input is valid, store the content in memory and execute the list_change function
        if  lineEdit.isdigit()==True and int(self.lineEditPopulation.text())>=0:
            self.my2dList[self.index][1]=self.lineEditPopulation.text()#set the new value to my2dlist
            self.list_Changed(self.index)
            QMessageBox.information(self,
                                    'Update',
                                    'Data has been update in memory, but hasn"t been update in the file yet',
                                     QMessageBox.Ok)
            #self.actionSave_To_File.setCheckable(True)
        
        else:#Prompt user data invalid, display the original data
            QMessageBox.information(self,
                                    'Invaild',
                                    'Data is invaild so not update in memory',
                                     QMessageBox.Ok)
            self.lineEditPopulation.setText(self.my2dList[self.index][1])
            
    def save_changes_to_file(self):
        # open the file for writing (w). Make sure it is the same location as the file you opened.
        with open("Final Project/Files/countries.txt", "w") as myFile:
            #loop through each list within the in-memory people list
            for population in self.my2dList: #<- refer to each list as population
                # join each value in the my2dList list and write them with a line break
                myFile.write(",".join(population) + "\n")  
                
    def closeEvent(self, event):#If the changed data is not saved, asking the user whether to save before exiting
    
        if self.unsaved_changes == True:

            msg = "Save changes to file before closing?"
            reply = QMessageBox.question(self, 'Save?',
                     msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:#if click yes call the save_chages_to_file function to save date
                self.save_changes_to_file()
                event.accept()  
    
        

#Example Helper Function
#    def Save(self):
#       Implement the save functionality here

# DO NOT MODIFY THIS CODE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_form = MyForm()
    the_form.show()
    sys.exit(app.exec_())
# END DO NOT MODIFY