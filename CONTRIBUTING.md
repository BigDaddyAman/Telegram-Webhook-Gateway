# Contributing

Thanks for your interest in contributing.

Contributions are welcome in the form of bug reports, documentation improvements, and code changes.

---

## Reporting Issues

If you find a bug or unexpected behavior, please open an issue and include:
- what you expected to happen
- what actually happened
- steps to reproduce (if possible)
- relevant logs or error messages

---

## Pull Requests

If you want to contribute code:
- fork the repository
- create a feature branch
- keep changes small and focused
- follow the existing project structure

Please explain what your change does and why it is needed.

---

## Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Optional (for webhook testing):

```bash
ngrok http 8000
```

## Guidelines

- do not commit secrets
- do not introduce breaking changes without discussion
- prefer simple, readable solutions
- keep dependencies minimal

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.