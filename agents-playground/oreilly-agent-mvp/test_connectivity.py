"""Quick connectivity test for all configured providers - no caching."""
import json
import urllib.request
from pathlib import Path


def load_env_direct():
    """Load .env directly from file, bypassing any caching."""
    env = {}
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env[key.strip()] = value.strip()
    return env


def test_azure_openai(env):
    """Test Azure OpenAI connectivity."""
    print("\n[1/3] Testing Azure OpenAI...")
    endpoint = env.get("AZURE_OPENAI_ENDPOINT", "").rstrip('/')
    api_key = env.get("AZURE_OPENAI_API_KEY", "")
    deployment = env.get("AZURE_OPENAI_DEPLOYMENT", "")
    api_version = env.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

    if not all([endpoint, api_key, deployment]):
        print("  - Azure OpenAI not configured (missing env vars)")
        return False

    url = f'{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}'
    
    req = urllib.request.Request(
        url,
        data=json.dumps({
            'messages': [{'role': 'user', 'content': 'Say connected'}],
            'max_completion_tokens': 10
        }).encode('utf-8'),
        headers={
            'api-key': api_key,
            'Content-Type': 'application/json'
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            print(f"  + Azure OpenAI connected! Model: {deployment}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ''
        print(f"  x Azure OpenAI FAILED: HTTP {e.code} - {body[:100]}")
        return False
    except Exception as e:
        print(f"  x Azure OpenAI FAILED: {e}")
        return False


def test_deepseek(env):
    """Test DeepSeek connectivity."""
    print("\n[2/3] Testing DeepSeek...")
    api_key = env.get("OPENAI_API_KEY", "")

    if not api_key:
        print("  - DeepSeek not configured (OPENAI_API_KEY not set)")
        return False

    url = 'https://api.deepseek.com/chat/completions'
    req = urllib.request.Request(
        url,
        data=json.dumps({
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': 'Say connected'}],
            'max_tokens': 10
        }).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            content = data['choices'][0]['message']['content']
            print(f"  + DeepSeek connected! Response: {content[:30]}")
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ''
        print(f"  x DeepSeek FAILED: HTTP {e.code} - {body[:100]}")
        return False
    except Exception as e:
        print(f"  x DeepSeek FAILED: {e}")
        return False


def test_github(env):
    """Test GitHub API connectivity."""
    print("\n[3/3] Testing GitHub...")
    token = env.get("GITHUB_TOKEN", "")

    if not token:
        print("  - GitHub not configured (GITHUB_TOKEN not set)")
        return False

    req = urllib.request.Request(
        "https://api.github.com/user",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "agent-mvp-test"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            print(f"  + GitHub connected! User: {data.get('login', 'unknown')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"  x GitHub FAILED: HTTP {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"  x GitHub FAILED: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Connectivity Test for Agent MVP")
    print("=" * 50)

    env = load_env_direct()

    results = {
        "Azure OpenAI": test_azure_openai(env),
        "DeepSeek": test_deepseek(env),
        "GitHub": test_github(env),
    }

    print("\n" + "=" * 50)
    print("Summary:")
    for name, success in results.items():
        status = "+ OK" if success else "x FAILED"
        print(f"  {name}: {status}")
    print("=" * 50)
