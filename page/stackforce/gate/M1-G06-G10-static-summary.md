# M1-G06–G10 静态审计历史快照

> 本页保存 2026-09-08 实机 session 之前的静态审计边界。当前状态以 [[M1-Hardware-Ground-Truth]]、[[M1-现场产物归档]] 和各 Gate 页面为准。

## 当时的静态结论

- G06/G07 已定义 timing 与 latency 路径，但尚无真机测量。
- G08/G09 只有 nominal geometry 与 mass prior。
- G10 在旧 source snapshot 中发现 `flat=1`、PPM/CAN freshness 和 last-command persistence 风险。

## 后续验证后的变化

2026-09-10 的 current-source 与架空实机 session 已更新这些结论：

| Gate | 当前状态 | 新增证据 |
|---|---|---|
| [[M1-G06-控制测频]] | PASS WITH EVIDENCE DEBT | IMU update-call 175.3 Hz；mean 5.704 ms；jitter 0.790 ms |
| [[M1-G07-延迟测量]] | PASS WITH EVIDENCE DEBT | 代表性路径在 500 ms command window 内响应；501.535–502.498 ms 自动 STOP |
| [[M1-G08-尺寸测量]] | PASS WITH EVIDENCE DEBT | 实物 five-bar graph 与共同 wheel closure 已确认；精密 metrology 仍欠缺 |
| [[M1-G09-质量测量]] | PASS WITH EVIDENCE DEBT | prior/unknown 分类足够首版 kinematic model；真实 dynamics 仍待标定 |
| [[M1-G10-停机验证]] | BLOCKED | current source 已关闭旧 `flat=1`/freshness 风险，但 ch7 在 firmware return/STOP 后物理回中失败 |

## 安全边界

ch7/ch8 隔离、修复并通过无负载与装配状态回中验证前，actuator rail 必须保持断电。不得把 current firmware 的 STOP/timeout 成功解释为 ch7 已安全回中。

## 下一步

- 上一页：[[M1-G05-指令定性]]
- 下一页：[[M1-G06-控制测频]]
- 返回：[[Home]]

## 更新日志

- 2026-09-11：将本页明确标记为历史快照，并增加 current-source/physical-session 后续结论。
- 2026-09-08：完成 G06–G10 初始静态审计。
