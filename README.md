# QRQC 快速响应（qrqc-quick-response）

面向生产现场班组长、制造/质量主管的 QRQC（Quick Response Quality Control）快速响应技能。当日异常即时上板、班次内闭环、日清日结。

## 适用岗位
- 班组长 / 拉长：战情板主责填写人。
- 制造现场主管 / 车间主任：主持班次战情会、升级决策。
- 现场质量工程师（QE）：协助根因分析与措施验证。
- 生产 / 质量经理：通过战情板掌握当日质量态势。

## 解决的核心痛点
- 异常响应慢、信息散落，错过当班解决窗口。
- 责任不清、无唯一责任人与时点承诺。
- 缺乏日清日结，问题跨班次漂移、反复发生。
- 临时遏制做了，根因验证与永久对策被遗漏。

## 产出物
- `QRQC战情板_YYYYMMDD.txt`：纯文字版战情板，便于打印或粘贴流转。
- `QRQC战情板_YYYYMMDD.md`：Markdown 版战情板，保留明细表格。

## 快速开始
```bash
# 直接运行，使用内置小样本产出样例 TXT+MD（写到当前工作目录）
python scripts/build_report.py

# 或基于自有 JSON 数据生成
python scripts/build_report.py --input 你的数据.json --out-dir 目标目录
```

## 战情板字段
序号 / 时间 / 产品-工序 / 异常现象 / 遏制措施 / 责任人 / 闭环时点 / 状态 / 证据。
状态取值：已闭环 ｜ 跟踪中 ｜ 已升级 ｜ 待补充。

## 联动技能（纯提示）
- 深挖根因：`5why-analysis` / `8d-report-assistant`
- 变化点引发：`change-point-management`
- 防错杜绝再发：`poka-yoke-design`
- 不合格品返工返修：`rework-repair-plan`

## 说明
- 所有文档为简体中文；不确定项标注「待补充」，不编造标准号与数据。
- 本技能只记录与升级，深度根因分析由相邻技能承接。
