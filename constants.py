from bs4 import BeautifulSoup 
import requests 
import json
import boto3

input_bucket = "your-input-bucket"
output_bucket = "your-output-bucket"
output_dump = "dump/"
bedrock_ep_url = "https://your-bedrock-endpoint-url"
smjs_endpoint = "jumpstart-dft-hf-text2text-flan-t5-xl"
region_name = "us-west-2"
ctx_sz = 4000
byte_sz = 4500

def listFiles(bucket, prefix=""):
    result = []
    session = boto3.Session()
    s3 = session.client('s3', region_name=region_name)
    response = s3.list_objects(Bucket=bucket, Prefix=prefix)
    if not "Contents" in response:
        return result
    for obj in response["Contents"]:
        result.append(obj["Key"])
    return result

def getTextFromWeb(url):
    website = requests.get(url)
    soup = BeautifulSoup(website.content, features="html.parser")
    webText = soup.get_text()
    return webText.replace('\n', ' ').replace('\r', '')

def truncate(s, n):
    return ' '.join(s.split()[:n])

lang_dict = {
    "English":"en",
    "Afrikaans":"af",
    "Albanian":"sq",
    "Amharic":"am",
    "Arabic":"ar",
    "Armenian":"hy",
    "Azerbaijani":"az",
    "Bengali":"bn",
    "Bosnian":"bs",
    "Bulgarian":"bg",
    "Catalan":"ca",
    "Chinese (Simplified)":"zh",
    "Chinese (Traditional)":"zh-TW",
    "Croatian":"hr",
    "Czech":"cs",
    "Danish":"da",
    "Dari":"fa-AF",
    "Dutch":"nl",
    "Estonian":"et",
    "Farsi (Persian)":"fa",
    "Filipino, Tagalog":"tl",
    "Finnish":"fi",
    "French":"fr",
    "French (Canada)":"fr-CA",
    "Georgian":"ka",
    "German":"de",
    "Greek":"el",
    "Gujarati":"gu",
    "Haitian Creole":"ht",
    "Hausa":"ha",
    "Hebrew":"he",
    "Hindi":"hi",
    "Hungarian":"hu",
    "Icelandic":"is",
    "Indonesian":"id",
    "Irish":"ga",
    "Italian":"it",
    "Japanese":"ja",
    "Kannada":"kn",
    "Kazakh":"kk",
    "Korean":"ko",
    "Latvian":"lv",
    "Lithuanian":"lt",
    "Macedonian":"mk",
    "Malay":"ms",
    "Malayalam":"ml",
    "Maltese":"mt",
    "Marathi":"mr",
    "Mongolian":"mn",
    "Norwegian (Bokmål)":"no",
    "Pashto":"ps",
    "Polish":"pl",
    "Portuguese (Brazil)":"pt",
    "Portuguese (Portugal)":"pt-PT",
    "Punjabi":"pa",
    "Romanian":"ro",
    "Russian":"ru",
    "Serbian":"sr",
    "Sinhala":"si",
    "Slovak":"sk",
    "Slovenian":"sl",
    "Somali":"so",
    "Spanish":"es",
    "Spanish (Mexico)":"es-MX",
    "Swahili":"sw",
    "Swedish":"sv",
    "Tamil":"ta",
    "Telugu":"te",
    "Thai":"th",
    "Turkish":"tr",
    "Ukrainian":"uk",
    "Urdu":"ur",
    "Uzbek":"uz",
    "Vietnamese":"vi",
    "Welsh":"cy"
}

def escape_str(a_string):
    escaped = a_string.translate(str.maketrans({"-":  r"\-",
                                          "]":  r"\]",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "$":  r"\$",
                                          "*":  r"\*",
                                          ".":  r"\."}))
    return escaped
