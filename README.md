# 業務記録プラットフォーム（Markdown × AI × DB）

## 概要
ユーザー自身が自由に業務記録テンプレート（フォームUI）を作成でき、記録内容をMarkdown＋DBで保存・検索・AI活用（要約・タグ付けなど）まで一貫して実現できるプラットフォームを開発します。

例：服薬指導記録、医療業務記録、教育・法務などの記録業務全般

## 機能（予定・進捗）
- [ ] 業務記録用フォームUI（Streamlitベース）
- [ ] Markdown（YAML frontmatter付き）でローカル保存
- [ ] DB（SQLite）に記録メタデータ登録・検索
- [ ] AI要約・タグ付け機能（OpenAI API使用）
- [ ] 記録一覧・詳細・編集画面
- [ ] APIエンドポイント提供（将来的拡張）
- [ ] テンプレート編集機能（将来的拡張）
- [ ] MarkdownからHTML/PDF/Word出力機能（将来的拡張）

## システム構成・技術スタック
- フロントエンド：Streamlit
- バックエンド：FastAPI（Python）
- データベース：SQLite（MVP）→将来的にPostgreSQL対応
- AI連携：OpenAI API（現時点）
- デプロイ：Docker＋自宅サーバ（またはVPS/クラウド）

## 画面イメージ（予定）
- 記録フォーム画面  
- 記録一覧画面  
- 記録詳細・編集画面

## 今後の開発予定
- MVPをまずは完成させる
- DB保存、検索、編集の拡張
- AI要約・タグ付け機能の追加
- その他UI/UXや可視化機能の改善

## セットアップ（予定）
```bash
git clone https://github.com/yourname/yourproject.git
cd yourproject
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate for Windows
pip install -r requirements.txt
streamlit run app.py
