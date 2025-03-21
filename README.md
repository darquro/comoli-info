# COMOLI Info Scraper

COMOLIの公式サイトの更新情報を自動的にスクレイピングし、LINE通知を送信するツールです。

## 機能

- COMOLIの[お知らせページ](https://www.comoli.jp/info)を定期的にスクレイピング
- 新しい投稿を検出すると、LINE通知で更新内容を送信
- GitHub Actionsで毎日自動実行（日本時間13:00）
- ローカル環境での手動実行にも対応

## 必要条件

- Python 3.10以上
- LINE Messaging API のアクセストークン
- LINE ユーザーID

## セットアップ

1. リポジトリをクローン
```bash
git clone https://github.com/darquro/comoli-info.git
cd comoli-info
```

2. 環境変数の設定
```bash
# .envファイルを作成（初回実行時に自動生成されます）
make check-env

# .envファイルを編集して、LINE認証情報を設定
vim .env
```

必要な環境変数：
- `LINE_CHANNEL_ACCESS_TOKEN`: LINE Messaging APIのチャネルアクセストークン
- `LINE_USER_ID`: 通知を受け取るLINEユーザーのID

3. 依存関係のインストール
```bash
make setup
```

## 使用方法

### ローカルでの実行

スクリプトを実行：
```bash
make run
```

生成されたファイルをクリーンアップ：
```bash
make clean
```

### GitHub Actionsでの自動実行

1. GitHubリポジトリの"Settings" > "Secrets and variables" > "Actions"に移動
2. 以下のシークレットを追加：
   - `LINE_CHANNEL_ACCESS_TOKEN`
   - `LINE_USER_ID`
3. GitHub Actionsのワークフローが自動的に実行されます（毎日日本時間13:00）

## ファイル構成

- `scrape_comoli.py`: メインのスクレイピングスクリプト
- `previous_content.json`: 前回取得した情報を保存するファイル
- `.github/workflows/scrape.yml`: GitHub Actionsのワークフロー設定
- `Makefile`: ローカル環境での実行を簡単にするためのMake設定
- `.env`: LINE認証情報を含む環境変数ファイル（gitignoreされます）
- `.env.example`: 環境変数のテンプレートファイル

## 注意事項

- `.env`ファイルはGitにコミットしないでください（セキュリティのため）
- LINE Messaging APIの利用制限に注意してください
- スクレイピングの際はサーバーに負荷をかけないよう配慮してください

## ライセンス

MIT License 