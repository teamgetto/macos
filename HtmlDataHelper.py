from bs4 import BeautifulSoup
import string

def RemoveHtmlTags(htmlData):
    beautifulSoup = BeautifulSoup(htmlData, "html.parser")
    for data in beautifulSoup(['style', 'script']):
        data.decompose()
    return ' '.join(beautifulSoup.stripped_strings)

def GetDocumentContentByGivenParameterHtmlTag(htmlData,htmlTag):
    try:
        documentContent = ""
        childTagList = GetDocumentHtmlTagListByGivenParameterHtmlTag(htmlData,htmlTag)
        for childTag in childTagList:
            documentContent += childTag.text
        return documentContent
    except:
        return documentContent

def GetDocumentHtmlTagListByGivenParameterHtmlTag(htmlData,htmlTag):
    beautifulSoup = BeautifulSoup(htmlData, "html.parser")
    childTagList = beautifulSoup.find_all(htmlTag)
    return childTagList

def GetDocumentContentWithSpecifiedParentTag(htmlData,htmlTag,htmlParentTag):
    childTagList = GetDocumentHtmlTagListByGivenParameterHtmlTag(htmlData,htmlTag)
    documentContent = ""
    for childTag in childTagList:
        if childTag.parent.name == htmlParentTag:
            documentContent += childTag.text
    return documentContent 