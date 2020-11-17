import requests


def get_session_maskanyaban(username, password):
    url = "http://www.maskanyaban.ir/Pages/login.aspx"

    data = {
        "__VIEWSTATE": "/wEPDwUJNjQ2Nzg2MDMxD2QWAmYPZBYGAgcPFgIeB1Zpc2libGVoZAIJDxYCHwBoZAILDxYCHwBoZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUgY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRjaF9SZW1J5B/wTGBXH1z3Om+xVoAOBaYsCmoenN2bsEt4/gL+DA==",
        "__VIEWSTATEGENERATOR": "D44F3332",
        "__EVENTVALIDATION": "/wEdAAUtlbrJQOzx/sGPcQf1RqtkEM3WKQ0M6QcLLA6U84ERJI2ZDQ+6hxqqfxIPxtgGY8yVx1oevN/bAHLPnc4v1rg6KhdgZ4TkaSORnDvSpQZQtoXC7nxFuX/1Rs9iZeOZICxTF/fRw83+cnJlB1VOQ3Ta"
        , "ctl00$ContentPlaceHolder1$Txt_UN": username
        , "ctl00$ContentPlaceHolder1$Txt_Pas": password
        , "ctl00$ContentPlaceHolder1$BtnLog": "ورود"}

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=10',
        'Origin': 'http://www.maskanyaban.ir',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://www.maskanyaban.ir/Pages/login.aspx',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': 'Cok_UserId=; ASP.NET_SessionId=msnt0l1tpkac2how0rlf5hst; ASP.NET_SessionId=me5e1qd1nat1fwidftexlh2z; '
    }

    s = requests.Session()

    s.post(url=url, headers=headers, data=data)

    cookies = s.cookies

    valid_session = cookies.__getitem__('.ASPXAUTH')

    return valid_session
