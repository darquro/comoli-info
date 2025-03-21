# COMOLI Info Notifier

COMOLIの情報ページ（https://www.comoli.jp/info） の更新を監視し、更新があった場合にLINE通知を送信するサービスです。

## セットアップ手順

1. LINE Developersでチャネルを作成
   - [LINE Developers](https://developers.line.biz/ja/)にアクセス
   - 新規プロバイダーを作成
   - Messaging APIチャネルを作成
   - チャネルアクセストークンを発行

2. LINE Notifyの友だち追加
   - 作成したLINE Botを友だち追加
   - ユーザーIDを取得

3. GitHubリポジトリの設定
   - このリポジトリをフォーク
   - GitHub Secretsに以下の値を設定:
     - `LINE_CHANNEL_ACCESS_TOKEN`: LINE Botのチャネルアクセストークン
     - `LINE_USER_ID`: 通知を受け取るLINEのユーザーID

4. GitHub Actionsの有効化
   - Actionsタブで「I understand my workflows, go ahead and enable them」をクリック

## 動作確認

1. GitHub Actionsタブで手動実行
   - `workflow_dispatch`イベントで実行可能
   - 実行結果とログを確認

## 仕様

- 毎日午後1時（日本時間）に自動実行
- 更新があった場合のみLINE通知
- 前回の内容は`previous_content.json`に保存

## 注意事項

- COMOLIウェブサイトの構造が変更された場合、スクレイピングの調整が必要な場合があります
- LINE Messaging APIの無料枠は月1000通までです 