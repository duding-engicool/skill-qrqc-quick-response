#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QRQC 快速响应战情板生成器：读取结构化数据，输出 文字版(.txt) + Markdown(.md)。

不生成网页版本，重实效、便于打印或粘贴流转。

内置小样本（4 行），直接运行 `python build_report.py` 即可产出样例 TXT+MD。
默认输出到用户当前工作目录（用户运行技能时所在目录），可用 --out-dir 指定。
"""
import argparse
import json
import os
import sys

# 内置小样本：4 行当班异常（演示用，非真实数据）
SAMPLE = {
    "plant": "XX工厂 / 总装车间",
    "shift": "2026-07-13 A班",
    "owner": "张班长",
    "items": [
        {
            "no": 1, "datetime": "0713-A 08:20", "prod": "支架/焊接",
            "issue": "焊点虚焊 12 件", "contain": "隔离当班产品+全检",
            "owner": "张班长", "due": "当班内", "status": "已闭环",
            "evidence": "全检合格记录+首件确认",
        },
        {
            "no": 2, "datetime": "0713-A 09:05", "prod": "门板/涂装",
            "issue": "漆面颗粒", "contain": "加过滤+首件确认",
            "owner": "李主管", "due": "跨班跟踪", "status": "跟踪中",
            "evidence": "—",
        },
        {
            "no": 3, "datetime": "0713-A 10:40", "prod": "线束/装配",
            "issue": "插接不到位 3 台", "contain": "停线复检+防错工装评估",
            "owner": "王工艺", "due": "当班内", "status": "已升级",
            "evidence": "升级至质量经理，待资源",
        },
        {
            "no": 4, "datetime": "0713-A 11:10", "prod": "壳体/注塑",
            "issue": "缺料号标签", "contain": "补标+追溯",
            "owner": "待补充", "due": "待补充", "status": "待补充",
            "evidence": "—",
        },
    ],
}


def summarize(items):
    """统计当日状态分布。"""
    stat = {}
    for it in items:
        s = it.get("status", "待补充")
        stat[s] = stat.get(s, 0) + 1
    return stat


def build_md(data):
    lines = []
    lines.append("# QRQC 快速响应战情板\n")
    lines.append(f"**工厂/车间**：{data.get('plant','—')}")
    lines.append(f"**班次**：{data.get('shift','—')}")
    lines.append(f"**战情板主责**：{data.get('owner','—')}\n")
    stat = summarize(data.get("items", []))
    if stat:
        parts = [f"{k} {v}" for k, v in stat.items()]
        lines.append(f"> 当日态势：{' ｜ '.join(parts)}\n")
    lines.append("## 战情板明细\n")
    lines.append("| 序号 | 时间 | 产品/工序 | 异常现象 | 遏制措施 | 责任人 | 闭环时点 | 状态 | 证据 |")
    lines.append("|------|------|-----------|----------|----------|--------|----------|------|------|")
    for it in data.get("items", []):
        lines.append(
            f"| {it.get('no','')} | {it.get('datetime','')} | {it.get('prod','')} | "
            f"{it.get('issue','')} | {it.get('contain','')} | {it.get('owner','')} | "
            f"{it.get('due','')} | {it.get('status','待补充')} | {it.get('evidence','—')} |"
        )
    lines.append("")
    lines.append("## 日清日结说明\n")
    lines.append("- **已闭环**：当班内完成遏制+验证，证据齐备。")
    lines.append("- **跟踪中**：需跨班交接，下一班次战情会复核。")
    lines.append("- **已升级**：超当班能力/权限，已上报指定对象。")
    lines.append("- **待补充**：缺责任人或闭环时点，需现场补全后再判定。")
    lines.append("")
    return "\n".join(lines)


def build_txt(data):
    """纯文字版：去 MD 语法，用缩进/横线排版，便于打印或粘贴流转。"""
    lines = []
    lines.append("=" * 48)
    lines.append("QRQC 快速响应战情板")
    lines.append("=" * 48)
    lines.append(f"工厂/车间：{data.get('plant','—')}")
    lines.append(f"班次：{data.get('shift','—')}")
    lines.append(f"战情板主责：{data.get('owner','—')}")
    stat = summarize(data.get("items", []))
    if stat:
        parts = [f"{k} {v}" for k, v in stat.items()]
        lines.append(f"当日态势：{' ｜ '.join(parts)}")
    lines.append("-" * 48)
    for it in data.get("items", []):
        lines.append(f"【问题 {it.get('no','')}】")
        lines.append(f"  时间：{it.get('datetime','')}")
        lines.append(f"  产品/工序：{it.get('prod','')}")
        lines.append(f"  异常现象：{it.get('issue','')}")
        lines.append(f"  遏制措施：{it.get('contain','')}")
        lines.append(f"  责任人：{it.get('owner','')}")
        lines.append(f"  闭环时点：{it.get('due','')}")
        lines.append(f"  状态：{it.get('status','待补充')}")
        lines.append(f"  证据：{it.get('evidence','—')}")
        lines.append("-" * 48)
    lines.append("日清日结说明：")
    lines.append("  已闭环 = 当班内完成遏制+验证，证据齐备")
    lines.append("  跟踪中 = 需跨班交接，下一班次战情会复核")
    lines.append("  已升级 = 超当班能力/权限，已上报指定对象")
    lines.append("  待补充 = 缺责任人或闭环时点，需现场补全后再判定")
    lines.append("=" * 48)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="JSON 输入文件路径（缺省用内置小样本）")
    ap.add_argument("--out-dir", default="", help="输出目录，默认用户当前工作目录")
    a = ap.parse_args()

    if a.input:
        try:
            data = json.load(open(a.input, encoding="utf-8"))
        except Exception as e:
            print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
            sys.exit(1)
    else:
        data = SAMPLE

    md = build_md(data)
    txt = build_txt(data)

    # 输出目录：优先 --out-dir，否则用户当前工作目录
    if a.out_dir:
        out_dir = a.out_dir
    else:
        try:
            out_dir = os.getcwd()
        except Exception:
            out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)

    shift_tag = "".join(ch for ch in data.get("shift", "样例") if ch.isalnum())
    md_out = os.path.join(out_dir, f"QRQC战情板_{shift_tag}.md")
    txt_out = os.path.join(out_dir, f"QRQC战情板_{shift_tag}.txt")
    open(md_out, "w", encoding="utf-8").write(md)
    open(txt_out, "w", encoding="utf-8").write(txt)
    print(json.dumps({"status": "success", "txt": txt_out, "md": md_out}, ensure_ascii=False))


if __name__ == "__main__":
    main()
