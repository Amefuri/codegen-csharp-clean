 
from jinja2 import Template, Environment, FileSystemLoader
import os.path
from PyQt5.QtWidgets import *

# class BaseResponseType(Enum):
#     BASE_RESULT = 1
#     BASE_ITEM_LIST = 2
#     BASE_PAGE_LIST = 3

def saveFile(folderPath: str, fileName: str, output: str):
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath, exist_ok=True)
    with open(f'{folderPath}{fileName}', "w") as fh:
        fh.write(output)

def genTemplate(templateName: str, folderPath: str, fileName: str, projectName: str, categoryName: str, actionName: str, removedGetActionName: str, isRequestBundle: bool = False, baseResponseType: str = '1'):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template(templateName)
    output_from_parsed_template = template.render(projectName=projectName, categoryName=categoryName, actionName=actionName, removedGetActionName=removedGetActionName, isRequestBundle=isRequestBundle, baseResponseType=baseResponseType)
    saveFile(folderPath, fileName, output_from_parsed_template)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever

def generate(rootFolderName: str, projectName: str, categoryName: str, actionName: str, isRequestBundle: bool, baseResponseType: str):

    removedGetActionName = remove_prefix(actionName, 'Get')

    #================ Config
    #folder path
    businessFolderPath = f'{rootFolderName}/{projectName}.Business/{categoryName}Business/'
    serviceFolderPath = f'{rootFolderName}/{projectName}.Service/{categoryName}Service/'
    requestFolderPath = f'{rootFolderName}/{projectName}.Domain/Api/Request/{categoryName}/'
    responseFolderPath = f'{rootFolderName}/{projectName}.Domain/Api/Response/{categoryName}/'
    requestBTDFolderPath = f'{rootFolderName}/{projectName}.Domain/BusinessTransformData/Request/{categoryName}/'
    responseBTDFolderPath = f'{rootFolderName}/{projectName}.Domain/BusinessTransformData/Response/{categoryName}/'

    #================ Business
    genTemplate(
        'business.txt', 
        businessFolderPath, 
        f'{actionName}Business.cs', 
        projectName, 
        categoryName, 
        actionName,
        removedGetActionName)

    #================ Service
    genTemplate(
        'service.txt', 
        serviceFolderPath, 
        f'{actionName}Service.cs', 
        projectName, 
        categoryName, 
        actionName,
        removedGetActionName,
        isRequestBundle)

    # #================ Request
    genTemplate(
        'request_bundle.txt' if isRequestBundle else 'request.txt', 
        requestFolderPath, 
        f'{removedGetActionName}Request.cs', 
        projectName, 
        categoryName, 
        actionName,
        removedGetActionName)

    # #================ Response
    genTemplate(
        'response.txt', 
        responseFolderPath, 
        f'{removedGetActionName}Response.cs', 
        projectName, 
        categoryName, 
        actionName,
        removedGetActionName,
        isRequestBundle,
        baseResponseType)

    # #================ BTDRequest
    genTemplate(
        'btd_request.txt', 
        requestBTDFolderPath, 
        f'{removedGetActionName}BTDRequest.cs', 
        projectName, 
        categoryName, 
        actionName,
        removedGetActionName)

    # #================ BTDResponse
    genTemplate(
        'btd_response.txt', 
        responseBTDFolderPath, 
        f'{removedGetActionName}BTDResponse.cs', 
        projectName, 
        categoryName, 
        actionName,
        removedGetActionName,
        isRequestBundle,
        baseResponseType)

def on_button_confirm_clicked():

    rootFolderName = textfieldRootFolderName.text()
    projectName = textfieldProjectName.text()
    categoryName = textfieldCategoryName.text()
    actionName = textfieldActionName.text()
    isRequestBundle = True if radioBundleYes.isChecked() else False
    baseResponseType = '1'
    if radioResponseTypeResult.isChecked():
        baseResponseType = '1'
    elif radioResponseTypeItemList.isChecked():
        baseResponseType = '2'
    else:
        baseResponseType = '3'
    
    generate(rootFolderName, projectName, categoryName, actionName, isRequestBundle, baseResponseType)

    # alert = QMessageBox()
    # alert.setText('You clicked the button! = ' + textfield1.text())
    # alert.exec_()

def register_business(actionName: str):

    f = open("RegisterBusinesses.cs", "r")
    sourceText = f.read()
    print(sourceText)

    foundIndexFunctionHead = sourceText.find("void Load(ContainerBuilder builder)")
    foundIndexCloseBracket = sourceText[foundIndexFunctionHead:].find("}")
    if(foundIndexCloseBracket != -1):
        writeIndex = foundIndexFunctionHead + foundIndexCloseBracket - 9
        newSourceText = sourceText[:writeIndex] + f'\n            Register{categoryName}Business(builder);' + sourceText[writeIndex:]
        print(newSourceText)

    foundIndexFunctionHead = sourceText.find(f"void Register{actionName}Business(ContainerBuilder builder)")
    foundIndexCloseBracket = sourceText[foundIndexFunctionHead:].find("}")
    if(foundIndexCloseBracket != -1):
        writeIndex = foundIndexFunctionHead + foundIndexCloseBracket - 9
        newSourceText = sourceText[:writeIndex] + f'\n            builder.RegisterType<{actionName}Business>().As<I{actionName}Business>().InstancePerDependency().EnableInterfaceInterceptors().InterceptedBy(_loggerInterceptor);' + sourceText[writeIndex:]
        print(newSourceText)
        #TODO write new source to file


def register_service(actionName: str):

    f = open("RegisterServices.cs", "r")
    sourceText = f.read()
    print(sourceText)

    foundIndexFunctionHead = sourceText.find("void Load(ContainerBuilder builder)")
    foundIndexCloseBracket = sourceText[foundIndexFunctionHead:].find("}")
    if(foundIndexCloseBracket != -1):
        writeIndex = foundIndexFunctionHead + foundIndexCloseBracket - 9
        newSourceText = sourceText[:writeIndex] + f'\n            Register{categoryName}Service(builder);' + sourceText[writeIndex:]
        print(newSourceText)

    foundIndexFunctionHead = sourceText.find(f"void Register{actionName}Service(ContainerBuilder builder)")
    foundIndexCloseBracket = sourceText[foundIndexFunctionHead:].find("}")
    if(foundIndexCloseBracket != -1):
        writeIndex = foundIndexFunctionHead + foundIndexCloseBracket - 9
        newSourceText = sourceText[:writeIndex] + f'\n            builder.RegisterType<{actionName}Service>().As<I{actionName}Service>().InstancePerDependency().EnableInterfaceInterceptors().InterceptedBy(_loggerInterceptor);' + sourceText[writeIndex:]
        print(newSourceText) 
        #TODO write new source to file


app = QApplication([])
window = QWidget()
hBox1 = QHBoxLayout()
hBoxProjectName = QHBoxLayout()
hBox2 = QHBoxLayout()
hBox3 = QHBoxLayout() 
hBox4 = QHBoxLayout()
hBox5 = QHBoxLayout()
hBox6 = QHBoxLayout()
layout = QVBoxLayout()

label1 = QLabel("rootFolderName: ")
textfieldRootFolderName = QLineEdit()
hBox1.addWidget(label1)
hBox1.addWidget(textfieldRootFolderName)

labelPrjectName = QLabel("projectName: ")
textfieldProjectName = QLineEdit()
hBoxProjectName.addWidget(labelPrjectName)
hBoxProjectName.addWidget(textfieldProjectName)

label2 = QLabel("categoryName: ")
textfieldCategoryName = QLineEdit()
hBox2.addWidget(label2)
hBox2.addWidget(textfieldCategoryName)

label3 = QLabel("actionName: ")
textfieldActionName = QLineEdit()
hBox3.addWidget(label3)
hBox3.addWidget(textfieldActionName)

labelIsBundle = QLabel("Is request bundle (y/n) ?")
groupBoxIsBundle = QGroupBox("")
radioBundleYes = QRadioButton("Yes")
radioBundleNo = QRadioButton("No")
radioBundleNo.setChecked(True)
hBox4.addWidget(labelIsBundle)
hBox4.addWidget(radioBundleYes)
hBox4.addWidget(radioBundleNo)
groupBoxIsBundle.setLayout(hBox4)

labelBaseResponseType = QLabel("SelectBaseResponseType: ")
groupBoxResponseType = QGroupBox("")
radioResponseTypeResult = QRadioButton("BaseResult")
radioResponseTypeItemList = QRadioButton("BaesItemList")
radioResponseTypePageList = QRadioButton("BasePageList")
radioResponseTypeResult.setChecked(True)
hBox5.addWidget(labelBaseResponseType)
hBox5.addWidget(radioResponseTypeResult)
hBox5.addWidget(radioResponseTypeItemList)
hBox5.addWidget(radioResponseTypePageList)
groupBoxResponseType.setLayout(hBox5)

buttonConfirm = QPushButton("Generate (finger crossed)")
buttonConfirm.clicked.connect(on_button_confirm_clicked)
hBox6.addWidget(buttonConfirm)

layout.addLayout(hBox1)
layout.addLayout(hBoxProjectName)
layout.addLayout(hBox2)
layout.addLayout(hBox3)
#layout.addLayout(hBox4)
layout.addWidget(groupBoxIsBundle)
# layout.addLayout(hBox5)
layout.addWidget(groupBoxResponseType)
layout.addLayout(hBox6)

window.setLayout(layout)
window.show()
app.exec_()


#aa = sourceText[foundIndexFunctionHead+foundIndexOpenBracket:foundIndexFunctionHead+foundIndexCloseBracket].splitlines()



# copyString = aa[len(aa)-2]
# print(copyString)
# aa.insert(len(aa)-1, copyString)

# print(aa)
# print("\n".join(aa))

# foundIndex3 = foundIndex + foundIndex2

# print(foundIndex)
# print(foundIndex2)
# print(foundIndex3)

# newSourceText = sourceText[:foundIndex3] + '    TEST\n' + sourceText[foundIndex3:]
# print(newSourceText)

# button1 = QPushButton('Top')
# button1.clicked.connect(on_button_clicked)
# button2 = QPushButton('Bottom')
# layout.addWidget(button1)
# layout.addWidget(button2)

# rootFolderName = input('Enter RootFolderName: ')
# categoryName = input('Enter CategoryName: ')
# actionName = input('Enter ActionName: ')
# isRequestBundle = (input('Is request bundle(y/n)?') == 'y')
# baseResponseType = input('SelectBaseResponseType(1:BaseResult, 2:BaesItemList 3:BasePageList): ') 


