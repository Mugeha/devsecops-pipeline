# DevSecOps Security Pipeline

An automated security testing pipeline that integrates security scanning into the CI/CD workflow, catching vulnerabilities before they reach production.

![Pipeline Status](https://github.com/YOUR-USERNAME/devsecops-pipeline/workflows/Security%20Pipeline/badge.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## Overview

This project demonstrates a complete **DevSecOps pipeline** that automatically:
- Performs static code analysis (SAST)
- Scans for hardcoded secrets and credentials
- Checks dependencies for known vulnerabilities (CVEs)
- Blocks deployment if critical issues are found
- Generates detailed security reports

**Built with GitHub Actions** - runs on every commit and pull request.

---

## 🏗️ Pipeline Architecture
```
┌─────────────┐
│  Code Push  │
└──────┬──────┘
       │
       ├──────────────────────────────────────┐
       │                                      │
       ▼                                      ▼
┌─────────────┐                      ┌──────────────┐
│ SAST Scan   │                      │Secret Scan   │
│ (Semgrep)   │                      │(TruffleHog)  │
└──────┬──────┘                      └──────┬───────┘
       │                                      │
       │      ┌──────────────┐               │
       └─────►│ Dependency   │◄──────────────┘
              │ Scan (Trivy) │
              └──────┬───────┘
                     │
                     ▼
              ┌─────────────┐
              │Security Gate│
              │   PASS/FAIL │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │   Deploy    │
              └─────────────┘
```

---

## 🛠️ Security Tools Used

### 1. **Semgrep** - Static Application Security Testing (SAST)
**What it does:** Analyzes source code for security vulnerabilities without running it.

**Detects:**
- SQL Injection
- Cross-Site Scripting (XSS)
- Command Injection
- Path Traversal
- Insecure Deserialization
- Hardcoded Secrets
- And more...

**Why it's good:**
- ✅ Fast (scans in seconds)
- ✅ Custom rules
- ✅ Low false positives
- ✅ Supports multiple languages

---

### 2. **TruffleHog + Gitleaks** - Secret Scanning
**What they do:** Scan git history for accidentally committed secrets.

**Detects:**
- API Keys
- AWS credentials
- Private keys
- Passwords
- Tokens
- Database credentials

**Why it's important:**
- 🔑 Prevents credential leaks
- 📜 Scans entire git history
- 🚨 Catches secrets before they're exposed

---

### 3. **Trivy + Safety** - Dependency Scanning
**What they do:** Check dependencies for known vulnerabilities (CVEs).

**Detects:**
- Known CVEs in libraries
- Outdated packages
- Vulnerable versions
- License issues

**Why it's critical:**
- 📦 Most vulnerabilities come from dependencies
- 🔄 New CVEs discovered daily
- ⚡ Automated updates recommendations

---

## 📊 What the Pipeline Catches

### Example Vulnerabilities Detected in Sample App:

| Type | Severity | Example | Tool |
|------|----------|---------|------|
| SQL Injection | 🔴 CRITICAL | `f"SELECT * FROM users WHERE username = '{username}'"` | Semgrep |
| Hardcoded Secret | 🟡 HIGH | `SECRET_KEY = "super_secret_key_12345"` | Semgrep, TruffleHog |
| XSS | 🟡 HIGH | `render_template_string(f"<h1>{query}</h1>")` | Semgrep |
| Command Injection | 🔴 CRITICAL | `os.popen(f'ping {host}')` | Semgrep |
| Path Traversal | 🔴 CRITICAL | `open(os.path.join('/var/data/', filename))` | Semgrep |
| Insecure Deserialization | 🔴 CRITICAL | `pickle.loads(data)` | Semgrep |
| Vulnerable Dependency | 🟡 HIGH | `requests==2.25.0` (CVE-2023-32681) | Trivy |
| Debug Mode | 🟠 MEDIUM | `app.run(debug=True)` | Semgrep |

---

## 🚀 How to Use

### 1. Fork or Clone This Repository
```bash
git clone https://github.com/YOUR-USERNAME/devsecops-pipeline.git
cd devsecops-pipeline
```

### 2. Enable GitHub Actions
- Go to repository Settings → Actions
- Enable "Allow all actions and reusable workflows"

### 3. Make a Change and Push
```bash
# Edit any file
git add .
git commit -m "Test security pipeline"
git push
```

### 4. Watch the Pipeline Run
- Go to the "Actions" tab
- See the security pipeline run automatically
- Check the results

---

## 📁 Project Structure
```
devsecops-pipeline/
├── .github/workflows/
│   └── security-scan.yml        # Main CI/CD pipeline
├── sample-app/
│   ├── app.py                   # Vulnerable demo app
│   ├── requirements.txt         # Dependencies (with CVEs)
│   └── tests/
│       └── test_app.py         # Basic tests
├── security-configs/
│   └── semgrep-rules.yml       # Custom SAST rules
├── scripts/                     # Automation scripts (coming soon)
├── docs/                        # Documentation (coming soon)
└── README.md                    # This file
```

---

## 🎓 What This Demonstrates

### DevSecOps Principles
✅ **Shift Left** - Security testing early in development  
✅ **Automation** - No manual security reviews needed  
✅ **Continuous** - Runs on every code change  
✅ **Fast Feedback** - Results in minutes, not days  
✅ **Developer-Friendly** - Clear, actionable findings  

### Industry Best Practices
✅ **Defense in Depth** - Multiple scanning tools  
✅ **Security Gate** - Block insecure code from deployment  
✅ **Artifact Storage** - Reports saved for auditing  
✅ **PR Integration** - Security feedback on pull requests  

---

## 📈 Pipeline Results

### Sample Run Statistics:
- ⏱️ **Duration:** ~3 minutes
- 🔍 **Files Scanned:** 3
- 🐛 **Vulnerabilities Found:** 8 critical, 3 high, 2 medium
- 📦 **Dependencies Checked:** 4
- 🔑 **Secrets Detected:** 2

---

## 🔧 Customization

### Add Custom Semgrep Rules
Edit `security-configs/semgrep-rules.yml`:
```yaml
rules:
  - id: my-custom-rule
    pattern: dangerous_function($X)
    message: Avoid using dangerous_function
    severity: ERROR
```

### Configure Security Gate Thresholds
Edit `.github/workflows/security-scan.yml`:
```yaml
# Block deployment if critical vulnerabilities found
- name: Security Gate
  run: |
    if [ $CRITICAL_COUNT -gt 0 ]; then
      exit 1  # Fail the build
    fi
```

---

## 📚 Learning Resources

### Tools Documentation
- [Semgrep Rules](https://semgrep.dev/docs/rules/)
- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [TruffleHog Usage](https://github.com/trufflesecurity/trufflehog)
- [GitHub Actions](https://docs.github.com/en/actions)

### Security Standards
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST DevSecOps](https://csrc.nist.gov/projects/devsecops)

---

## 🎯 Real-World Impact

**This pipeline prevents:**
- 🔴 SQL injection attacks
- 🔴 Credential leaks to public repos
- 🔴 Using libraries with known exploits
- 🔴 XSS attacks
- 🔴 Command injection vulnerabilities

**Saves companies:**
- 💰 Average data breach cost: $4.45M (IBM 2023)
- ⏰ Fixing bugs in production: 30x more expensive than in development
- 🛡️ Reputation damage from security incidents

---

## 🚧 Roadmap

Future enhancements:
- [ ] Add DAST (Dynamic Application Security Testing)
- [ ] Integrate container security scanning
- [ ] Add infrastructure-as-code scanning
- [ ] Implement security score tracking
- [ ] Create Slack/email notifications
- [ ] Add license compliance checking
- [ ] Deploy to staging for live testing

---

## ⚠️ Disclaimer

The sample application is **intentionally vulnerable** for demonstration purposes.  
**DO NOT** deploy it to production or expose it to the internet.

---

## 👤 Author

**[Your Name]**
- Portfolio: [your-portfolio.com](https://your-portfolio.com)
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your Profile](https://linkedin.com/in/your-profile)

---

## 🙏 Acknowledgments

- OWASP for security standards
- Semgrep team for amazing SAST tool
- Aqua Security for Trivy
- TruffleHog for secret scanning

---

**⭐ If this helped you learn DevSecOps, consider giving it a star!**

---

*Part of an Application Security portfolio demonstrating modern DevSecOps practices*