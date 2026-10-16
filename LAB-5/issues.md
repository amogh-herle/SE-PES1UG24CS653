# Issues Found — Static Analysis

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Use of `eval()` on deduction expression | Security (Bandit B307, Medium) | 42 | `eval(deduction_expr)` executes arbitrary code built from input, code injection risk | Replace with safe arithmetic (e.g. parse with `ast.literal_eval` or manual whitelist of operators); never eval raw strings |
| Shell command built from filename | Security (Bandit B605, High) | 58 | `os.system("echo ..." + filename)` passes unsanitized filename to shell, command injection risk | Use `print()` or `subprocess.run([...])` without `shell=True` |
| Weak MD5 hash | Security (Bandit B324, High) | 47 | `hashlib.md5()` is cryptographically weak | Use `hashlib.sha256()`, or pass `usedforsecurity=False` since it's not used for security here |
| Bare `except: pass` | Reliability (Pylint W0702 / Bandit B110) | 26-27 | Catches and silently swallows every exception, hides real bugs (e.g. missing emp_id) | Catch the specific exception (`KeyError`) and handle/log it |
| Mutable default argument `[]` | Bug risk (Pylint W0102) | 15 | Default list is shared across all calls, stale/leaked state between unrelated calls | Default to `None`, create a new list inside the function body |
| Non-cryptographic RNG for token | Security (Bandit B311, Low) | 51 | `random.randint` is not suitable if token is security-sensitive | Use `secrets.randbelow()` / `secrets.token_hex()` |
| `== None` singleton comparison | Correctness/Style (Pylint C0121) | 32 | Should use identity check, not equality | Replace `== None` with `is None` |
| Unused import/variables | Code quality (Pylint W0611, W0612) | 6, 31, 41 | `math` import and `statutory_buffer`, `base` variables never used, dead code clutter | Remove unused import and variables |
