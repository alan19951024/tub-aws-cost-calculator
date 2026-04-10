"""
generate_log.py
---------------
由 GitHub Actions 呼叫，分析本次 commit 的變更內容，
透過 Claude API 生成繁體中文更新摘要，並寫入 COMMIT_LOG.md。
"""

import os
import anthropic


# ── 工具函式 ────────────────────────────────────────────────────────────────

def read_file(path: str, default: str = "") -> str:
    """讀取檔案，若失敗則回傳預設值。"""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return default


def read_or_init_log(log_path: str) -> str:
    """讀取現有 COMMIT_LOG.md，若不存在則回傳初始標頭。"""
    if os.path.exists(log_path):
        return read_file(log_path)
    return (
        "# Commit 更新日誌\n\n"
        "> 此檔案由 GitHub Actions 自動產生，記錄每次 commit 的重點更新內容。\n\n"
        "---\n\n"
    )


def prepend_entry(log_content: str, new_entry: str) -> str:
    """將新的 log entry 插入在標頭分隔線 `---` 之後。"""
    separator = "---\n\n"
    idx = log_content.find(separator)
    if idx != -1:
        insert_pos = idx + len(separator)
        return log_content[:insert_pos] + new_entry + log_content[insert_pos:]
    # 找不到分隔線就直接附加在最前面
    return new_entry + log_content


# ── 主流程 ──────────────────────────────────────────────────────────────────

def main() -> None:
    # 從 GitHub Actions 環境變數讀取 commit 資訊
    short_sha    = os.environ.get("COMMIT_SHORT_SHA", "unknown")
    full_sha     = os.environ.get("COMMIT_FULL_SHA",  "unknown")
    author       = os.environ.get("COMMIT_AUTHOR",    "unknown")
    date         = os.environ.get("COMMIT_DATE",       "")
    branch       = os.environ.get("BRANCH_NAME",       "main")
    repo         = os.environ.get("REPO_NAME",         "")

    # 從暫存檔讀取 git 資訊
    commit_message = read_file("/tmp/commit_message.txt").strip()
    diff_stat      = read_file("/tmp/diff_stat.txt").strip()
    changed_files  = read_file("/tmp/changed_files.txt").strip()
    diff_content   = read_file("/tmp/diff_content.txt").strip()

    # ── 呼叫 Claude API ──────────────────────────────────────────────────────
    client = anthropic.Anthropic()

    prompt = f"""你是一位資深軟體工程師，專門負責撰寫清晰易懂的程式碼更新紀錄。
請根據以下 Git commit 資訊，用「繁體中文」撰寫一份結構化的更新摘要。

━━━━━━━━━━━━━━━━━━━━━━━━
Commit 基本資訊
━━━━━━━━━━━━━━━━━━━━━━━━
- SHA：{short_sha}
- 作者：{author}
- 日期：{date}
- 分支：{branch}
- Commit Message：
{commit_message}

━━━━━━━━━━━━━━━━━━━━━━━━
變更統計
━━━━━━━━━━━━━━━━━━━━━━━━
{diff_stat or "（無統計資訊）"}

━━━━━━━━━━━━━━━━━━━━━━━━
變更檔案（A=新增 M=修改 D=刪除 R=重新命名）
━━━━━━━━━━━━━━━━━━━━━━━━
{changed_files or "（無變更檔案）"}

━━━━━━━━━━━━━━━━━━━━━━━━
程式碼差異（部分內容）
━━━━━━━━━━━━━━━━━━━━━━━━
{diff_content[:3000] or "（無差異內容）"}

━━━━━━━━━━━━━━━━━━━━━━━━

請嚴格按照以下格式輸出，不要加入任何額外說明或前言：

### 🔑 更新重點
- （列出 3~5 個本次更新的核心變更，每點簡明扼要）

### 📦 影響範圍
（說明這次變更影響了哪些功能、頁面或模組，1~3 句）

### 🛠 技術細節
（重要的實作細節、演算法、API 變更等；若無則填「無特殊技術細節」）

### ⚠️ 注意事項
（部署注意事項、破壞性變更、相依套件更新等；若無則填「無」）"""

    print(f"🤖 呼叫 Claude API 分析 commit {short_sha}...")

    with client.messages.stream(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        final = stream.get_final_message()

    # 取出文字內容（略過 thinking block）
    summary = next(
        (block.text for block in final.content if block.type == "text"),
        "（Claude 未回傳摘要）",
    )

    # ── 組合 log entry ───────────────────────────────────────────────────────
    github_url = f"https://github.com/{repo}/commit/{full_sha}" if repo else ""
    sha_link   = f"[`{short_sha}`]({github_url})" if github_url else f"`{short_sha}`"

    log_entry = (
        f"## {sha_link} · {date[:10]}\n\n"
        f"| 項目 | 內容 |\n"
        f"|------|------|\n"
        f"| 分支 | `{branch}` |\n"
        f"| 作者 | {author} |\n"
        f"| Commit | {commit_message.splitlines()[0]} |\n\n"
        f"{summary}\n\n"
        f"---\n\n"
    )

    # ── 寫入 COMMIT_LOG.md ───────────────────────────────────────────────────
    log_path    = "COMMIT_LOG.md"
    log_content = read_or_init_log(log_path)
    updated     = prepend_entry(log_content, log_entry)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"✅ COMMIT_LOG.md 已更新（commit {short_sha}）")
    print(f"   使用 tokens：input={final.usage.input_tokens}  output={final.usage.output_tokens}")


if __name__ == "__main__":
    main()
