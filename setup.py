#!/usr/bin/env python3
"""
Business Plan Generator v2.0 - Interactive Setup Script
대화형으로 API 키를 입력받아 .env 파일을 생성합니다.
"""

import os
import sys
import io
from pathlib import Path

# Windows 콘솔 UTF-8 설정
def init_console():
    """Windows 콘솔 설정 초기화"""
    if sys.platform == "win32":
        os.system("")  # Windows ANSI 색상 활성화
        # UTF-8 출력 설정
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

init_console()

# ANSI 색상
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_header():
    """헤더 출력"""
    print(f"""
{BOLD}{'='*50}
🚀 Business Plan Generator v2.0 Setup
{'='*50}{RESET}

이 스크립트는 필요한 API 키를 설정하고 .env 파일을 생성합니다.
""")


def print_step(step: int, total: int, title: str):
    """단계 출력"""
    print(f"\n{CYAN}[{step}/{total}] {title}{RESET}")


def get_input(prompt: str, required: bool = False, secret: bool = False) -> str:
    """사용자 입력 받기"""
    suffix = " (필수)" if required else " (선택, Enter로 건너뛰기)"
    try:
        value = input(f"  {prompt}{suffix}: ").strip()
        if required and not value:
            print(f"  {RED}⚠ 필수 항목입니다.{RESET}")
            return get_input(prompt, required, secret)
        return value
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}설정이 취소되었습니다.{RESET}")
        sys.exit(0)


def select_option(prompt: str, options: list) -> int:
    """옵션 선택"""
    print(f"\n  {prompt}")
    for i, opt in enumerate(options, 1):
        print(f"    {i}. {opt}")

    while True:
        try:
            choice = input(f"  선택 (1-{len(options)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return idx
            print(f"  {RED}1-{len(options)} 사이의 숫자를 입력하세요.{RESET}")
        except ValueError:
            print(f"  {RED}숫자를 입력하세요.{RESET}")
        except KeyboardInterrupt:
            print(f"\n\n{YELLOW}설정이 취소되었습니다.{RESET}")
            sys.exit(0)


def check_existing_env(env_path: Path) -> bool:
    """기존 .env 파일 확인"""
    if env_path.exists():
        print(f"{YELLOW}⚠ 기존 .env 파일이 발견되었습니다.{RESET}")
        choice = select_option("어떻게 하시겠습니까?", [
            "덮어쓰기 (기존 설정 삭제)",
            "백업 후 새로 생성",
            "취소"
        ])
        if choice == 0:
            return True
        elif choice == 1:
            backup_path = env_path.with_suffix('.env.backup')
            env_path.rename(backup_path)
            print(f"  {GREEN}✓ 백업 완료: {backup_path}{RESET}")
            return True
        else:
            return False
    return True


def setup_llm_provider() -> dict:
    """LLM Provider 설정 (Grok 또는 OpenRouter)"""
    print_step(1, 3, "LLM API 설정")

    print(f"""
  {BOLD}사용 가능한 옵션:{RESET}
  • Grok API: X(Twitter) 실시간 검색 가능, 트렌드 분석에 최적
  • OpenRouter: 다양한 모델 선택 가능, Grok API 없어도 사용 가능
""")

    choice = select_option("어떤 API를 사용하시겠습니까?", [
        "Grok API (xAI) - X/Twitter 검색 기능 포함",
        "OpenRouter - 다양한 모델 지원 (Grok API 대안)",
        "둘 다 설정 (Grok 우선, OpenRouter 백업)"
    ])

    config = {}

    if choice in [0, 2]:  # Grok API
        print(f"\n  {CYAN}Grok API 설정{RESET}")
        print(f"  → API 키 발급: {BOLD}https://console.x.ai/{RESET}")
        config['XAI_API_KEY'] = get_input("XAI_API_KEY", required=(choice == 0))
        config['XAI_API_URL'] = "https://api.x.ai/v1/chat/completions"
        config['XAI_MODEL'] = "grok-2-latest"

    if choice in [1, 2]:  # OpenRouter
        print(f"\n  {CYAN}OpenRouter 설정{RESET}")
        print(f"  → API 키 발급: {BOLD}https://openrouter.ai/keys{RESET}")
        config['OPENROUTER_API_KEY'] = get_input("OPENROUTER_API_KEY", required=(choice == 1))
        config['OPENROUTER_API_URL'] = "https://openrouter.ai/api/v1/chat/completions"

        # 모델 선택
        if config.get('OPENROUTER_API_KEY'):
            model_choice = select_option("OpenRouter에서 사용할 모델을 선택하세요:", [
                "x-ai/grok-2-1212 (Grok 2 - 추천)",
                "anthropic/claude-3.5-sonnet (Claude 3.5)",
                "openai/gpt-4o (GPT-4o)",
                "google/gemini-2.0-flash-exp:free (무료)",
                "직접 입력"
            ])

            models = [
                "x-ai/grok-2-1212",
                "anthropic/claude-3.5-sonnet",
                "openai/gpt-4o",
                "google/gemini-2.0-flash-exp:free"
            ]

            if model_choice < 4:
                config['OPENROUTER_MODEL'] = models[model_choice]
            else:
                config['OPENROUTER_MODEL'] = get_input("모델 ID 입력", required=True)

    # 기본 Provider 설정
    if choice == 0:
        config['LLM_PROVIDER'] = "grok"
    elif choice == 1:
        config['LLM_PROVIDER'] = "openrouter"
    else:
        config['LLM_PROVIDER'] = "auto"  # Grok 우선, 없으면 OpenRouter

    return config


def setup_infranodus() -> dict:
    """InfraNodus 설정"""
    print_step(2, 3, "InfraNodus 설정 (지식 그래프 분석)")

    print(f"""
  InfraNodus는 텍스트를 지식 그래프로 시각화하는 도구입니다.
  → API 키 발급: {BOLD}https://infranodus.com/account/api{RESET}
  → 없으면 건너뛰어도 기본 기능 사용 가능
""")

    config = {}
    api_key = get_input("INFRANODUS_API_KEY", required=False)
    if api_key:
        config['INFRANODUS_API_KEY'] = api_key

    return config


def setup_mcp() -> bool:
    """MCP 서버 설정 안내"""
    print_step(3, 3, "Claude Code MCP 설정")

    print(f"""
  {BOLD}MCP (Model Context Protocol) 설정:{RESET}

  이 프로젝트는 Claude Code에서 InfraNodus MCP 서버를 사용합니다.
  .mcp.json 파일이 이미 포함되어 있습니다.

  {CYAN}Claude Code에서 자동으로 인식됩니다.{RESET}
  (INFRANODUS_API_KEY를 설정했다면 바로 사용 가능)
""")

    return True


def generate_env_file(config: dict, env_path: Path):
    """환경 변수 파일 생성"""
    content = """# Business Plan Generator v2.0 - Environment Variables
# Generated by setup.py

# ===========================================
# LLM Provider Setting
# ===========================================
# Options: "grok", "openrouter", "auto" (tries grok first, then openrouter)
LLM_PROVIDER={LLM_PROVIDER}

# ===========================================
# Grok API (xAI) - X/Twitter 검색 기능 포함
# ===========================================
# Get your API key from: https://console.x.ai/
XAI_API_KEY={XAI_API_KEY}
XAI_API_URL={XAI_API_URL}
XAI_MODEL={XAI_MODEL}

# ===========================================
# OpenRouter API - 다양한 모델 지원
# ===========================================
# Get your API key from: https://openrouter.ai/keys
OPENROUTER_API_KEY={OPENROUTER_API_KEY}
OPENROUTER_API_URL={OPENROUTER_API_URL}
OPENROUTER_MODEL={OPENROUTER_MODEL}

# ===========================================
# InfraNodus (Optional - for knowledge graphs)
# ===========================================
# Get your API key from: https://infranodus.com/account/api
INFRANODUS_API_KEY={INFRANODUS_API_KEY}
"""

    # 기본값 설정
    defaults = {
        'LLM_PROVIDER': 'auto',
        'XAI_API_KEY': '',
        'XAI_API_URL': 'https://api.x.ai/v1/chat/completions',
        'XAI_MODEL': 'grok-2-latest',
        'OPENROUTER_API_KEY': '',
        'OPENROUTER_API_URL': 'https://openrouter.ai/api/v1/chat/completions',
        'OPENROUTER_MODEL': 'x-ai/grok-2-1212',
        'INFRANODUS_API_KEY': '',
    }

    # 설정값 병합
    final_config = {**defaults, **config}

    # 파일 생성
    env_content = content.format(**final_config)
    env_path.write_text(env_content, encoding='utf-8')


def print_success(config: dict):
    """성공 메시지 출력"""
    print(f"""
{GREEN}{'='*50}
✅ 설정 완료!
{'='*50}{RESET}

{BOLD}생성된 파일:{RESET}
  • .env (API 키 설정)

{BOLD}설정된 항목:{RESET}""")

    provider = config.get('LLM_PROVIDER', 'auto')
    if provider == 'grok':
        print(f"  • LLM Provider: Grok API")
    elif provider == 'openrouter':
        print(f"  • LLM Provider: OpenRouter ({config.get('OPENROUTER_MODEL', 'default')})")
    else:
        print(f"  • LLM Provider: Auto (Grok 우선)")

    if config.get('INFRANODUS_API_KEY'):
        print(f"  • InfraNodus: ✓ 설정됨")
    else:
        print(f"  • InfraNodus: ✗ 미설정 (선택 사항)")

    print(f"""
{BOLD}다음 단계:{RESET}
  1. 의존성 설치:
     {CYAN}pip install -r requirements.txt{RESET}

  2. 테스트 실행:
     {CYAN}python scripts/grok_api.py "K-beauty trends 2025"{RESET}

  3. Claude Code에서 사용:
     {CYAN}cd business_planner_v2{RESET}
     {CYAN}claude{RESET}

{YELLOW}💡 Tip: .env 파일은 git에 커밋되지 않습니다 (보안){RESET}
""")


def main():
    """메인 함수"""
    # 프로젝트 루트 경로
    project_root = Path(__file__).parent
    env_path = project_root / '.env'

    print_header()

    # 기존 .env 확인
    if not check_existing_env(env_path):
        print(f"\n{YELLOW}설정이 취소되었습니다.{RESET}")
        return

    # 설정 수집
    config = {}

    # 1. LLM Provider 설정
    llm_config = setup_llm_provider()
    config.update(llm_config)

    # 2. InfraNodus 설정
    infra_config = setup_infranodus()
    config.update(infra_config)

    # 3. MCP 설정 안내
    setup_mcp()

    # .env 파일 생성
    generate_env_file(config, env_path)

    # 성공 메시지
    print_success(config)


if __name__ == "__main__":
    main()
