"""
This code sample shows Custom Extraction Model operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

model_id = "https://docservicekyvault.vault.azure.net/secrets/modelID/c34dc940045742868eb2b3e2e67e6df9"
formUrl = 'https://raw.githubusercontent.com/MicrosoftLearning/mslearn-ai-document-intelligence/main/Labfiles/02-custom-document-intelligence/sample-forms/Form_5.jpg'

def get_doc_analysis_client():
    """
    Remember to remove the key from your code when you're done, and never post it publicly. For production, use
    secure methods to store and access your credentials. For more information, see 
    https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
    """
    endpoint = "https://docservicekyvault.vault.azure.net/secrets/endpoint/eb521c77eb8d4b1d86bc49682a485f78"
    key = "https://docservicekyvault.vault.azure.net/secrets/modelkey/6aaca68b4d794786b220a764fbb6c559"
    
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    return document_analysis_client

# Make sure your document's type is included in the list of document types the custom model can analyze
def scan_the_form(model_id, formUrl):
    document_analysis_client = get_doc_analysis_client()
    poller = document_analysis_client.begin_analyze_document_from_url(model_id, formUrl)
    result = poller.result()
    return result



def get_fields_and_data(result):
    data= {}
    for idx, document in enumerate(result.documents):
        print("--------Analyzing document #{}--------".format(idx + 1))
        print("Document has type {}".format(document.doc_type))
        print("Document has confidence {}".format(document.confidence))
        print("Document was analyzed by model with ID {}".format(result.model_id))
        for name, field in document.fields.items():
            field_value = field.value if field.value else field.content
            print("......found field {} of type '{}' with value '{}' and with confidence {}".format(name,field.value_type, field_value, field.confidence))
            data[name]=[field_value,"with confidence={}".format(field.confidence)]
    return data


def get_data():
    result = scan_the_form(model_id, formUrl)
    data = get_fields_and_data(result)
    return data

global_data=get_data()

def get_fieldValue(field_name:str):
    return global_data[field_name][0]

print(get_fieldValue("PurchaseOrder"))

# # iterate over tables, lines, and selection marks on each page
# for page in result.pages:
#     print("\nLines found on page {}".format(page.page_number))
#     for line in page.lines:
#         print("...Line '{}'".format(line.content.encode('utf-8')))
#     for word in page.words:
#         print(
#             "...Word '{}' has a confidence of {}".format(
#                 word.content.encode('utf-8'), word.confidence
#             )
#         )
#     for selection_mark in page.selection_marks:
#         print(
#             "...Selection mark is '{}' and has a confidence of {}".format(
#                 selection_mark.state, selection_mark.confidence
#             )
#         )

# for i, table in enumerate(result.tables):
#     print("\nTable {} can be found on page:".format(i + 1))
#     for region in table.bounding_regions:
#         print("...{}".format(i + 1, region.page_number))
#     for cell in table.cells:
#         print(
#             "...Cell[{}][{}] has content '{}'".format(
#                 cell.row_index, cell.column_index, cell.content.encode('utf-8')
#             )
#         )
print("-----------------------------------")
