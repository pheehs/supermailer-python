# supermailer-python

## What's this?
[SuperMailer](http://supermailer.jp/)の非公式CLIクライアントです。  
SuperMailerとは、使い捨てメールアドレスを取得できるサービスで詳しくは[公式サイト](http://supermailer.jp/)を見てください。

Cookieを保存して前回のメールアドレスをそのまま使えるようになっています。

    ----メールアドレス確認中----
    <取得済み>
    Address: viostaim@supermailer.jp
    get new?<y/n>n
    >help
    <help>
    check	メール一覧取得
    read [messageID]	指定したメッセージIDの本文取得
    exit	終了
    >check
    ----メールチェック中----
    メール:  1件
    No.1 - - - - -
    From: **************
    Date: 00:33:20 AM 10/22/2012
    Subject: subject です。
    
    >read 1
    ----メールを開きます----
    ================
    From: **************
    Date: 10/22/2012, 00:33:20 AM
    Subject: subject です。
    Message:
    本文です。テストです。以上です。
    
    >exit
    Cookieを保存中..

メールアドレス確認後コマンド入力を要求されます。
 * check
   - メール一覧の取得
 * read [messageID]
   - 指定したメッセージIDの本文取得
 * exit
   - プログラムを終了

## TODO
 * 返信機能追加
 
