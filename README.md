# vLLM-HUST 引擎 MOD 模板

《大模型推理系统与实践》个人必做项目 · 基础分 100 分。

第 4 讲完成 BidKV 实操后，从本模板创建个人仓库。这里用抢占策略讲解打包与注册。选择其他扩展点时，按该宿主版本核对接口并相应修改清单。

## CPU 冒烟测试

使用 Python 3.10 或更新版本。在仓库根目录运行以下命令。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install .
python -m unittest discover -s tests -v
```

Windows PowerShell 可用 `py -m venv .venv` 建环境，后续用 `.\.venv\Scripts\python.exe` 执行相同命令。

测试从安装包发现 Bundle、读取清单、加载策略，并核对空实现会把决定交回宿主。动手后，把该断言改成与自己策略相符的验收用例，补上停用或回退用例。

## 实现自己的 MOD

1. 修改 `src/course_vllm_hust_mod/policy.py`。抢占接口读取不可变上下文，只返回本次候选中的请求 ID 或 `None`。
2. 为发行包、扩展 ID 和模块使用独立命名。同步修改 `pyproject.toml`、Bundle 清单和测试，保持引用一致。
3. 在兼容引擎里验证加载、触发与停用。该清单对应 vLLM-HUST 提交 [`f7bc2a5e`](https://github.com/vLLM-HUST/vllm-hust/commit/f7bc2a5eebc505f28abfbf318734225e4c30c64c) 的发布版本 `0.31.1.post1.dev19` 和抢占 API 1.0。换宿主版本时重新核对声明及行为。

在已安装兼容引擎的专用虚拟环境，安装自己的 wheel 和固定版本的 Extension Manager。以下命令使用模板的初始扩展 ID。

```bash
python -m pip install build
python -m build --wheel
python -m pip install dist/course_vllm_hust_mod-0.1.0-py3-none-any.whl
python -m pip install 'vllm-hust-ext @ git+https://github.com/vLLM-HUST/extension-manager.git@6a26ae88acc14591817df9069b7c884dd1a4f86d'
export VLLM_HUST_EXT_CONFIG="$PWD/.venv/mod-manager.json"
vllm-hust-ext extension inspect edu.hust.course.preemption-starter
vllm-hust-ext extension validate edu.hust.course.preemption-starter
vllm-hust-ext extension enable edu.hust.course.preemption-starter
vllm-hust-ext run -- vllm serve "$MODEL"
```

先将 `MODEL` 设为本环境可用的模型。用能形成 KV 压力的负载检查策略调用。停止服务后，运行 `vllm-hust-ext extension disable edu.hust.course.preemption-starter`，使用相同命令与负载重跑基线。

按 [实验记录](EXPERIMENT.md) 准备第 4、6、8 讲提交，在教学平台填写相应的仓库链接和提交 SHA。完整要求见[课程评分标准](https://courses.sage.org.ai/tutorials/assessment/#project-score)。
