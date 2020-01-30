 
from jinja2 import Template, Environment, FileSystemLoader
import os.path

def saveFile(folderPath: str, fileName: str, output: str):
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath, exist_ok=True)
    with open(f'{folderPath}{fileName}', "w") as fh:
        fh.write(output)

def genTemplate(templateName: str, folderPath: str, fileName: str, projectName: str, categoryName: str, actionName: str):
    template = env.get_template(templateName)
    output_from_parsed_template = template.render(projectName=projectName, categoryName=categoryName, actionName=actionName)
    saveFile(folderPath, fileName, output_from_parsed_template)

categoryName = input('Enter CategoryName: ')
actionName = input('Enter ActionName: ')
isRequestBundle = (input('Is request bundle(y/n)?') == 'y')

#================ Config
projectName = 'Ptar'
#folder path
businessFolderPath = f'{projectName}.Business/{categoryName}Business/'
serviceFolderPath = f'{projectName}.Service/{categoryName}Service/'
requestFolderPath = f'{projectName}.Domain/Api/Request/{categoryName}/'
responseFolderPath = f'{projectName}.Domain/Api/Response/{categoryName}/'
requestBTDFolderPath = f'{projectName}.Domain/BusinessTransformData/Request/{categoryName}/'
responseBTDFolderPath = f'{projectName}.Domain/BusinessTransformData/Response/{categoryName}/'

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

#================ Business
genTemplate(
    'business.txt', 
    businessFolderPath, 
    f'{actionName}Business.cs', 
    projectName, 
    categoryName, 
    actionName)

#================ Service
genTemplate(
    'service.txt', 
    serviceFolderPath, 
    f'{actionName}Service.cs', 
    projectName, 
    categoryName, 
    actionName)

# #================ Request
genTemplate(
    'request.txt' if isRequestBundle else 'request_bundle.txt', 
    requestFolderPath, 
    f'{actionName}Request.cs', 
    projectName, 
    categoryName, 
    actionName)

# #================ Response
genTemplate(
    'response.txt', 
    responseFolderPath, 
    f'{actionName}Response.cs', 
    projectName, 
    categoryName, 
    actionName)

# #================ BTDRequest
genTemplate(
    'btd_request.txt', 
    requestBTDFolderPath, 
    f'{actionName}BTDRequest.cs', 
    projectName, 
    categoryName, 
    actionName)

# #================ BTDResponse
genTemplate(
    'btd_response.txt', 
    responseBTDFolderPath, 
    f'{actionName}BTDResponse.cs', 
    projectName, 
    categoryName, 
    actionName)
