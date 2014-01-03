#!/usr/bin/env python
#-*- coding:utf-8 -*-

from BeautifulSoup import BeautifulSoup as BS
import urllib2, urllib, cookielib, sys

URL = "http://supermailer.jp/"

def html_decode(text):
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&nbsp;", " ").replace("&amp;", "&")

class Message(object):
    def __init__(self, sender, date, subject, messageID):
        self.sender = sender
        self.date = date
        self.subject = subject
        self.messageID = messageID
        
    def view(self):
        print "From:", self.sender
        print "Date:", self.date
        print "Subject:", self.subject
        return
        
class Mailer(object):
    def __init__(self, cookiefile="cookie.txt"):
        self.running = True
        self.cookiefile = cookiefile
        self.cj = cookielib.LWPCookieJar()
        try:
            self.cj.load(self.cookiefile, True, False)
        except IOError:
            print "Cookieを新規作成"

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        opener.addheaders = [("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)")]
        urllib2.install_opener(opener)
        self.have_email = False
        
        # outputing codecs
        if sys.platform == "win32":
            self.codec = "cp932"
        else:
            self.codec = "utf-8"        

    def __del__(self):
        print u"Cookieを保存中.."
        self.cj.save(self.cookiefile, True, True)
        return
    
    def _get_email(self):
        html = urllib2.urlopen(URL, urllib.urlencode({"getemail":"作成"}))
        return self._check_gotten_email(html)
    def get_email(self):
        print u"----メールアドレス取得中----".encode(self.codec)
        if self._get_email():
            print u"<取得成功>".encode(self.codec)
        else:
            print u"<取得失敗>".encode(self.codec)
        return
    
    def _check_gotten_email(self, html=None):
        if not html:
            html = urllib2.urlopen(URL).read()
        soup = BS(html)
        mailform = soup.find("form", {"name":"mailform"})
        if not mailform:
            self.have_email = False
            return False
        else:
            self.mail_address = mailform.input.get("value")
            self.have_email = True
            return True
        
    def check_gotten_email(self):
        print u"----メールアドレス確認中----"
        if self._check_gotten_email():
            print u"<取得済み>".encode(self.codec)
            print "Address:", self.mail_address
        else:
            print u"<未取得>".encode(self.codec)
        return
    
    def _delete_email(self):
        html = urllib2.urlopen(URL, urllib.urlencode({"ditchemail":"削除"})).read()
        return self._check_gotten_email(html)
    def delete_email(self):
        print u"----メールアドレス削除中----".encode(self.codec)
        if self._delete_email():
            print u"<削除失敗>".encode(self.codec)
        else:
            print u"<削除成功>".encode(self.codec)
        return

    def _check_mails(self, html=None):
        if not html:
            html = urllib2.urlopen(URL).read()
        soup = BS(html)
        mail_table = soup.find("table", {"class":"t12l_mail_list"})
        self.messages = []
        for mail in mail_table.findAll("tr")[2:]:
            tds = mail.findAll("td")
            self.messages.append(
                Message(
                    sender = html_decode(tds[1].text),
                    date = html_decode(tds[3].text),
                    subject = html_decode(tds[2].a.text),
                    messageID = tds[2].a.get("href").split("=")[-1],
                    )
                )
        return len(self.messages)
    def check_mails(self):
        print u"----メールチェック中----".encode(self.codec)
        print (u"メール:  %d件" % self._check_mails()).encode(self.codec)
        for c, mes in enumerate(self.messages):
            print "No.%d - - - - -" % (c + 1)
            mes.view()
            print ""
        return

    def _read_mail(self, messageID):
        html = urllib2.urlopen(URL + "index.php?d=xhr&f=message&m=" + messageID).read()
        soup = BS(html)
        details_table = soup.find("table", {"class":"t12l_mail_details"})
        contents = details_table.findAll("tr")
        # show sender, date, subject
        for detail in contents[:-1]:
            d = detail.findAll("td")
            print html_decode(d[0].text + ":"), html_decode(d[1].text.replace("<br />", "\n"))
        # show message
        d = contents[-1].findAll("td")
        print html_decode(d[0].text + ":")
        print html_decode(d[1].text.replace("<br />", "\n"))

            
        print ""
        return
    def read_mail(self, mID=None):
        print u"----メールを開きます----"
        if not mID:
            mID = raw_input("Message No.>")
        try: 
            s = int(mID) - 1
            if s < 0:
                raise
        except:
            print "Error Invalid messageID!"
            return
        else:
            print "================"
            try:
                self._read_mail(self.messages[s].messageID)
            except IndexError:
                print "Error: Invalid messageID!"
            return
        
def main():
    mailer = Mailer()
    mailer.check_gotten_email()
    r = raw_input("get new?<y/n>")
    if r == "y":
        mailer.delete_email()
        mailer.get_email()
        mailer.check_gotten_email()
    while mailer.running:
        command = raw_input(">").strip().split(" ")
        if command[0] == "check":
            mailer.check_mails()
        elif command[0] == "read":
            if len(command) < 2:
                print "Error: Invalid command!"
                print "type 'help' to show help."
            else:
                mailer.read_mail(command[1])
        elif command[0] == "exit":
            mailer.running = False
        else:
            print "<help>"
            print "check\tメール一覧取得"
            print "read [messageID]\t指定したメッセージIDの本文取得"
            print "exit\t終了"
    return

if __name__ == "__main__": main()
