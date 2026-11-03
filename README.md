# 模式识别与机器学习 · 编程作业 #2：决策树

在给定框架上实现 ID3（信息增益）、C4.5（增益率）决策树，以及预剪枝、后剪枝；CART（基尼指数）为选做，也一并实现。

| 路径 | 内容 |
|---|---|
| `assignment.pdf` | 作业要求 |
| `code/` | 代码与数据（`tree.py` 中的 TODO 已补全） |
| `code/results/` | 全部决策树可视化图片、运行日志、`summary.txt` 汇总 |
| `report/report.md` / `report/report.pdf` | 实验报告（PDF 由 `report/build_pdf.py` 生成） |
| `make_zip.sh` | 打包成 `学号+姓名.zip`（内含 `report.pdf` 和 `code/`） |

## 运行

```bash
pip install matplotlib
cd code
python tree.py melon 1 none     # 数据集(melon/celeba) 算法(1=ID3,2=C4.5,3=CART) 剪枝(none/pre/post)
./run_all.sh                    # 跑完全部 18 组实验
```

## 结果（测试准确率）

| 数据集 | 算法 | 不剪枝 | 预剪枝 | 后剪枝 |
|---|---|---|---|---|
| melon | ID3 | 42.86% | 71.43% | 71.43% |
| celeba | ID3 | 78% | 76% | **86%** |
| celeba | C4.5 | 72% | 68% | **84%** |
| celeba | CART（选做） | 80% | 76% | **84%** |

## 打包提交

```bash
./make_zip.sh 学号 姓名         # 生成 学号姓名.zip
```

提交前记得在 `report/report.md` 开头填上学号和姓名，再运行 `python report/build_pdf.py` 重新生成 PDF（需要 `pip install markdown` 和本机的 Chrome/Chromium）。
