 
from jinja2 import Template, Environment, FileSystemLoader
import os.path

# class BaseResponseType(Enum):
#     BASE_RESULT = 1
#     BASE_ITEM_LIST = 2
#     BASE_PAGE_LIST = 3

def saveFile(folderPath: str, fileName: str, output: str):
    if not os.path.isdir(folderPath):
        os.makedirs(folderPath, exist_ok=True)
    with open(f'{folderPath}{fileName}', "w") as fh:
        fh.write(output)

def genTemplate(templateName: str, folderPath: str, fileName: str, projectName: str, categoryName: str, actionName: str, isRequestBundle: bool = False, baseResponseType: str = '1'):
    template = env.get_template(templateName)
    output_from_parsed_template = template.render(projectName=projectName, categoryName=categoryName, actionName=actionName, isRequestBundle=isRequestBundle, baseResponseType=baseResponseType)
    saveFile(folderPath, fileName, output_from_parsed_template)

rootFolderName = input('Enter RootFolderName: ')
categoryName = input('Enter CategoryName: ')
actionName = input('Enter ActionName: ')
isRequestBundle = (input('Is request bundle(y/n)?') == 'y')
baseResponseType = input('SelectBaseResponseType(1:BaseResult, 2:BaesItemList 3:BasePageList): ') 

print(isRequestBundle)
print(baseResponseType)

#================ Config
projectName = 'Ptar'
#folder path
businessFolderPath = f'{rootFolderName}/{projectName}.Business/{categoryName}Business/'
serviceFolderPath = f'{rootFolderName}/{projectName}.Service/{categoryName}Service/'
requestFolderPath = f'{rootFolderName}/{projectName}.Domain/Api/Request/{categoryName}/'
responseFolderPath = f'{rootFolderName}/{projectName}.Domain/Api/Response/{categoryName}/'
requestBTDFolderPath = f'{rootFolderName}/{projectName}.Domain/BusinessTransformData/Request/{categoryName}/'
responseBTDFolderPath = f'{rootFolderName}/{projectName}.Domain/BusinessTransformData/Response/{categoryName}/'

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
    actionName,
    isRequestBundle)

# #================ Request
genTemplate(
    'request_bundle.txt' if isRequestBundle else 'request.txt', 
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
    actionName,
    isRequestBundle,
    baseResponseType)

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
    actionName,
    isRequestBundle,
    baseResponseType)
