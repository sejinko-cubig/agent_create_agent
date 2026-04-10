"""
리포트만 재생성

사용법:
  python command/generate_report.py --file outputs/output.py
"""

import argparse
import os
import yaml
from anthropic import Anthropic

HARNESS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(description="리포트 재생성")
    parser.add_argument("--file", required=True, help="LangGraph 코드 파일 경로")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        code = f.read()

    config_path = os.path.join(HARNESS_ROOT, "harness", "config", "models.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    report_skill_path = os.path.join(HARNESS_ROOT, "harness", "skill", "report_designer.md")
    with open(report_skill_path, "r") as f:
        report_skill = f.read()

    client = Anthropic()
    response = client.messages.create(
        model=config["agents"]["coder"]["model"],
        max_tokens=8000,
        temperature=0.2,
        system="You are a report generation specialist. Extract the analysis results from the given LangGraph code and generate a comprehensive Korean markdown report.",
        messages=[{
            "role": "user",
            "content": f"""아래 LangGraph 코드의 통계 분석 로직과 샘플 데이터를 분석하여
리포트를 직접 생성해줘.

```python
{code}
```

리포트 구조:
{report_skill}"""
        }],
    )

    result = response.content[0].text
    out_path = os.path.join(os.path.dirname(args.file), "report.md")
    with open(out_path, "w") as f:
        f.write(result)
    print(f"📄 리포트 저장: {out_path}")
    print(result[:500] + "...")


if __name__ == "__main__":
    main()
