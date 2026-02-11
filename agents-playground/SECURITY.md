# Security Policy

## Supported Versions

This is an educational project for O'Reilly Live Learning courses. We maintain security updates for the current version only.

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| older   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

**For security issues:**
- **Email:** tim@techtrainertim.com
- **Subject:** [SECURITY] agents2 vulnerability report
- **Include:** Description, steps to reproduce, potential impact

**Response timeline:**
- Initial response: Within 48 hours
- Status update: Within 5 business days
- Resolution target: 30 days for critical issues

## Security Best Practices for Users

This project demonstrates AI agent patterns and requires API keys. Please follow these guidelines:

### API Key Management
- ✅ **DO** use environment variables (`.env` file)
- ✅ **DO** add `.env` to `.gitignore` (already configured)
- ✅ **DO** rotate keys regularly
- ❌ **DON'T** commit API keys to version control
- ❌ **DON'T** share keys in screenshots or logs
- ❌ **DON'T** use production keys for demos

### Recommended Practices
1. **Use separate API keys** for development and production
2. **Enable rate limiting** on your LLM provider accounts
3. **Monitor API usage** to detect unauthorized access
4. **Review logs** for sensitive data before sharing
5. **Keep dependencies updated** (`pip install --upgrade`)

## Known Security Considerations

### LLM API Calls
- Issue data is sent to third-party LLM providers (Anthropic, OpenAI, Azure)
- Ensure compliance with your organization's data policies
- Consider using Azure OpenAI for enterprise compliance requirements

### GitHub Token Permissions
- The `GITHUB_TOKEN` in `.env` requires only `repo:read` scope
- Never use tokens with `write` or `admin` permissions for demos
- Revoke tokens immediately if compromised

### Dependencies
- We regularly update dependencies for security patches
- Run `pip list --outdated` to check for updates
- Review the `pyproject.toml` for current versions

## Disclosure Policy

- Security issues are addressed promptly
- Fixes are released as soon as possible
- Credit is given to reporters (unless anonymity is requested)
- CVEs will be filed for critical vulnerabilities

## Contact

**Tim Warner**
Email: tim@techtrainertim.com
Website: [TechTrainerTim.com](https://TechTrainerTim.com)

For general questions, use [GitHub Issues](https://github.com/timothywarner-org/agents2/issues).
For security concerns, use email (see above).

---

*This project is for educational purposes. Use in production environments at your own risk.*
