# task-demo-highlights

Public highlights from DataMining's delivered task-data demos — the **model-visible parts** of real task packages, plus difficulty evidence from our acceptance runs.

We build original, expert-authored tasks for training and evaluating frontier models and agents: coding, complex reasoning, multimodal, and agent capability lines. Founded by PhD researchers from the School of Software, Peking University; delivered to leading technology companies including ByteDance, Alibaba, and Tencent.

> **What we publish vs. keep private.** Every commercial task package has a private side — hidden tests, rubrics, golden patches, ground-truth workspaces. Those are the evaluation assets and are never published (publishing them destroys the task). What you see here is the model-visible side: instructions, public workspaces, and measured model performance.

## Contents

| Folder | What it is | Difficulty evidence |
|---|---|---|
| `anyon_intelligence_demo_hle_vl_8.pdf` | 8 expert-written multimodal problems (math · physics · chemistry · biology) in HLE-VL style, each with answer and full derivation | L3 band: written to sit beyond HLE difficulty |
| `tbs-science-01/` | One accepted Terminal-Bench-Science-style task (statistical calibration of an 8-control phase experiment; integer least squares + exponential family) | A frontier vision model went **0/5 trials** on this task family |
| `apex-agents-01/` | Full public side of an APEX-Agents-style professional task: instruction + simulated corporate filesystem (financing transaction readiness) | Frontier model scores ranged 33%–58% across 3 sample solutions |
| `toolathlon-01/` | Task brief of a real Toolathlon-style tool-orchestration task (MCP servers, live workspace audit) | Long-rule tasks; models fail on constraint bookkeeping |
| `automationbench-01/` | 3 workflow-automation task prompts (Sheets/Gmail/Slack/Zendesk simulators), solution-free | Best attempt averaged 0.63 across runs |

## Full delivery statements

Measured under one uniform budget (GPT-5.6 Sol, xhigh reasoning, 4 valid attempts per task):

- **DeepSWE** — 5 delivered repository-level tasks: every task solved ≤ 2/4 attempts; **3 tasks solved 0 times**. See [`datamining-ai/eval-task-examples`](https://github.com/datamining-ai/eval-task-examples) for the public view of a real DeepSWE task.
- **Frontier SWE** — 4 delivered examples: every task solved ≤ 2/4 attempts; 1 task solved 0 times.
- **ProgramBench** — 3 examples, 515 hidden test inputs: every task solved ≤ 2/4 attempts.

Full numbers and caveats: [Frontier Task Difficulty Report 2026](https://www.datamining.cloud/en/reports/frontier-task-difficulty-2026.html) · [Delivery notes](https://github.com/datamining-ai/eval-task-examples/blob/main/docs/delivery-notes-code.md)

## Why "hard" is the product

A task the model can already solve contributes near-zero gradient signal in RL training and overstates capability in evaluation. Difficulty is the precondition for data usefulness — that is why we measure it, publish the measurements, and grade every item to a difficulty band (L1/L2/L3) before delivery.

## Contact

- Website: <https://www.datamining.cloud>
- Email: <contact@datamining.cloud>

## License

Task content in this repository is © DataMining, provided for evaluation of our work; do not redistribute the tasks themselves. Code files are MIT unless stated otherwise.
