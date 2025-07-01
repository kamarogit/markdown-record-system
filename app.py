import os
from datetime import date
from pathlib import Path
from typing import Dict
import re

import streamlit as st
import yaml
from markdown import markdown

from backend.db import init_db, get_session
from backend.models import Record
from backend.crud import create_record, get_records

# 初期化
init_db()

# Markdown保存先
DATA_DIR = Path("data/records")
DATA_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(page_title="業務記録プラットフォーム", layout="wide")


def generate_markdown_frontmatter(data: Dict) -> str:
    """入力データをYAML frontmatter付きMarkdownに変換"""
    frontmatter = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    md_body = f"""
# 記録本文

- S: {data.get('S', '')}
- O: {data.get('O', '')}
- A: {data.get('A', '')}
- P: {data.get('P', '')}
"""
    return f"---\n{frontmatter}---\n{md_body}"


menu = st.sidebar.selectbox("メニュー", ["新規記録", "一覧"])

if menu == "新規記録":
    st.header("📄 新規業務記録")

    with st.form("record_form"):
        col1, col2 = st.columns(2)
        with col1:
            patient_name = st.text_input("患者名", "")
            patient_id = st.text_input("患者ID", "")
        with col2:
            visit_date = st.date_input("診察日", value=date.today())

        st.subheader("処方内容")
        prescription = st.text_area("処方内容", "")

        st.subheader("SOAP")
        s_val = st.text_area("S (主観的情報)", "")
        o_val = st.text_area("O (客観的情報)", "")
        a_val = st.text_area("A (評価・考察)", "")
        p_val = st.text_area("P (計画・指導内容)", "")

        submitted = st.form_submit_button("保存")

    if submitted:
        # バリデーション
        errors = []
        if not patient_name:
            errors.append("患者名は必須です。")
        elif len(patient_name) > 50:
            errors.append("患者名は50文字以内で入力してください。")
        if not patient_id:
            errors.append("患者IDは必須です。")
        elif not re.match(r'^[a-zA-Z0-9_-]+$', patient_id):
            errors.append("患者IDは英数字・ハイフン・アンダースコアのみ使用できます。")
        if not prescription:
            errors.append("処方内容は必須です。")
        if not s_val:
            errors.append("S (主観的情報)は必須です。")
        if not o_val:
            errors.append("O (客観的情報)は必須です。")
        if not a_val:
            errors.append("A (評価・考察)は必須です。")
        if not p_val:
            errors.append("P (計画・指導内容)は必須です。")

        if errors:
            for err in errors:
                st.error(err)
        else:
            meta = {
                "patient_name": patient_name,
                "patient_id": patient_id,
                "visit_date": str(visit_date),
                "prescription": prescription,
                "S": s_val,
                "O": o_val,
                "A": a_val,
                "P": p_val,
            }
            md_text = generate_markdown_frontmatter(meta)

            # ファイル保存
            filename = f"{date.today().isoformat()}_{patient_name or 'noname'}.md".replace(" ", "_")
            file_path = DATA_DIR / filename
            file_path.write_text(md_text, encoding="utf-8")

            # DB保存 (メタ情報のみ簡易的に)
            with next(get_session()) as session:
                rec = Record(
                    patient_name=patient_name,
                    patient_id=patient_id,
                    visit_date=visit_date,
                    markdown_path=str(file_path),
                )
                create_record(session, rec)

            st.success("記録を保存しました！")

elif menu == "一覧":
    st.header("📚 記録一覧")
    with next(get_session()) as session:
        records = get_records(session)

    for rec in records:
        with st.expander(f"{rec.visit_date} | {rec.patient_name}"):
            st.markdown(f"**ID:** {rec.id}")
            st.markdown(f"**ファイル:** {rec.markdown_path}")
            if os.path.exists(rec.markdown_path):
                md_raw = Path(rec.markdown_path).read_text(encoding="utf-8")
                # YAML frontmatter抽出
                match = re.match(r"^---\n(.*?)\n---\n(.*)", md_raw, re.DOTALL)
                if match:
                    yaml_str, md_body = match.groups()
                    meta = yaml.safe_load(yaml_str)
                    # メタ情報をユーザーフレンドリーに表示
                    st.info(
                        f"**患者名:** {meta.get('patient_name', '')}　"
                        f"**患者ID:** {meta.get('patient_id', '')}　"
                        f"**診察日:** {meta.get('visit_date', '')}"
                    )
                    # 本文のみプレビュー
                    st.markdown(md_body, unsafe_allow_html=True)
                else:
                    st.warning("YAML frontmatterの解析に失敗しました")
            else:
                st.warning("Markdownファイルが見つかりませんでした") 