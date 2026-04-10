"""
QA Agent 단독 실행

사용법:
  python command/run_qa.py --file outputs/output.py
"""

import argparse
import os
import yaml
from anthropic import Anthropic

HARNESS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(description="QA Agent 단독 실행")
    parser.add_argument("--file", required=True, help="검증할 Python 파일 경로")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        code = f.read()

    config_path = os.path.join(HARNESS_ROOT, "harness", "config", "models.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    qa_skill_path = os.path.join(HARNESS_ROOT, "harness", "skill", "qa_reviewer.md")
    with open(qa_skill_path, "r") as f:
        qa_skill = f.read()

    qa_agent_path = os.path.join(HARNESS_ROOT, "harness", "agent", "qa.md")
    with open(qa_agent_path, "r") as f:
        qa_system = f.read()

    client = Anthropic()
    response = client.messages.create(
        model=config["agents"]["qa"]["model"],
        max_tokens=8000,
        system=qa_system,
        messages=[{
            "role": "user",
            "content": f"""아래 코드를 검증해줘:

```python
{code}
```

{qa_skill}"""
        }],
    )

    result = response.content[0].text
    print(result)

    out_path = os.path.join(os.path.dirname(args.file), "qa_report.md")
    with open(out_path, "w") as f:
        f.write(result)
    print(f"\n📄 QA 리포트 저장: {out_path}")


if __name__ == "__main__":
    main()
