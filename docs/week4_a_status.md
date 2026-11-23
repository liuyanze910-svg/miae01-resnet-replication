# Week 4 Member A Progress

SuSiying (2260032041), 23 November 2026. Evidence snapshot: [`39c480f`](https://github.com/liuyanze910-svg/miae01-resnet-replication/tree/39c480f39e15bfde3b61f474207acc567f43a8b3).

## Scope and deliverables

The confirmed team plan assigns A the Week 4 English introduction, reproduction scope, setup, an in-body deviation table, background/methods slides, and baseline evidence. B owns Paper vs. Ours, main figures, results analysis, and the main-experiment slides. C owns the extension and overall conclusion. B/C logs were read for setup verification and remain unchanged. No new standalone statistics or plotting scripts, duplicate setup tables, or full training runs are part of this update.

- [English Member A report section](week4_a_report.md): introduction, scope, methods, the deviation table, contributions, AI statement, and references.
- [English background and methods slides](slides/week4_a_background_methods.pptx) and [Chinese version](slides/week4_a_background_methods_cn.pptx): ten detailed slides per language matching the user's supplied white/pastel Art template previews, with editable foreground text and architecture/baseline tables, speaker notes in each deck's language, and source references. The decorative backgrounds are reconstructed raster assets, not the original editable template file.
- Both covers list the full team: SuSiying / 苏思颖 (2260032041), Liu Yanze / 刘彦泽 (2260031728), and Liang Linlin / 梁琳琳 (2260032082). The group-member strip follows the user-supplied Mure(4).pptx cover reference, while retaining ResNet content and the existing Art design. The Chinese version translates foreground text, table labels, and speaker notes.
- [Detailed speaker notes](week4_a_speaker_notes.md): the ten English scripts, Chinese preparation notes, source links, and questions for presentation preparation.
- [Baseline evidence](week3_status.md): the original Week 2/3 logs remain the source of the baseline scores.

## Week 1-3 verification

| Stage | Evidence and check | Status |
| --- | --- | --- |
| Week 1 | Real-data and synthetic summaries both record eight ResNet-20 updates. [Real-data record](week1_status.md). Initial code and English documentation are in the repository history. | Complete |
| Week 2 | Seed 42, 16,000 updates, 10,000 test images, test error 10.23%, accuracy 89.77%. Summary agrees with the final CSV row. | Complete |
| Week 3 | Seeds 43/44, 16,000 updates each, test errors 10.58%/10.36%. All three seeds yield mean error 10.39% and sample SD 0.18 pp. | Complete |
| Local A archive | Read `D:\编程工具\小组pre\ResNet_Week3_A_GitHub_Update`. Its 12 baseline log/config/revision files agree with GitHub under parsed-content comparison. | Verified |
| Shared experiment records | Nine A/B/C summaries agree with final CSV rows. Each has 16 training intervals, four validation rows, and one test row. Declared split, budget, optimizer, and schedule match. | Verified as archived |

The review does not independently establish model-prediction accuracy or recreate a runtime environment. A used Windows and B/C used macOS. Same seed labels do not ensure identical random draws across depth/augmentation settings. These limitations are described in the report setup for the result authors to retain.

The detailed follow-up explains the 20-layer count and feature-map sizes, exact post-addition ReLU, learning-rate boundaries, split versus training seeds, and sample-SD interpretation. It also makes clear that `train.py` saves logs but no model weights. The archived logs support consistency checks, not loading the original trained model for independent re-evaluation.

## Member A baseline handoff

| Seed | Test error (%) | Test accuracy (%) | Original archive |
| --- | ---: | ---: | --- |
| 42 | 10.23 | 89.77 | [Week 2 seed 42](results/week2/resnet20-flip-seed42/) |
| 43 | 10.58 | 89.42 | [Week 3 seed 43](results/week3/resnet20-flip-seed43/) |
| 44 | 10.36 | 89.64 | [Week 3 seed 44](results/week3/resnet20-flip-seed44/) |

Mean error is **10.39%**, with **sample SD 0.18 pp** across n = 3 seeds. The existing [baseline workbook](results/week3/baseline_results.xlsx) remains available for B's Excel calculations/figures. No replacement workbook or duplicate raw logs were added.

## GitHub and course requirements

The course checks meaningful pushed commits every Sunday at 23:59. The current week's check is **29 November 2026, 23:59 Hong Kong time**, following the user's time context. The course lists **12 December 2026** as the tentative presentation date. The final report must be English PDF with source traceability, contributions, and an AI usage statement. The final repository needs a `v1.0` tag when the team finalizes it, not at this Week 4 draft stage.

The current authenticated GitHub account is `hu907958184-source`, which also authored A's Week 3 upload commit. The Week 3 commit [`48ac26f`](https://github.com/liuyanze910-svg/miae01-resnet-replication/commit/48ac26faffd0851fc2922bb9c8be341c0ba10348) contains A's two new seeds but uses `Add files via upload`, without the required ID and full name. This update does not rewrite that shared history. The new commit message must include `2260032041 SuSiying` and describe the work.

Git commit timestamps and archived files establish the visible history but cannot establish the push time of every historical commit. This review therefore does not certify every past weekly deadline. A new compliant commit does not repair an earlier missed week or deficient message.

The README already provides pinned training dependencies, data download, smoke/full-run commands, expected logs, and runtime examples. This update adds the Week 4 A handoff and submission rules. `docs/sources.md` still identifies the independently implemented project's license as a team decision. Before final release, the team should settle that decision and preserve any upstream license if it incorporates upstream code. No new license is assigned in this A-only update.

## Files in this update

- `README.md`: current Week 4 A links and submission requirements.
- `docs/week2_report_draft.md`: historical-draft notice pointing to the new A sections.
- `docs/week4_a_report.md`: current A section draft, with the only full setup-deviation table.
- `docs/week4_a_status.md`: this verification and handoff record.
- `docs/slides/week4_a_background_methods.pptx`: A's English background/methods slides with the full team cover.
- `docs/slides/week4_a_background_methods_cn.pptx`: Chinese slides and speaker notes, with the same team cover.
- `docs/week4_a_speaker_notes.md`: detailed English speaker scripts and Chinese preparation notes.

Week 5 remains for revising A's sections and merging the three authors' report sections, checking citations and figure numbering, and preparing the combined English PDF. The main results and extension text remain with B and C.
