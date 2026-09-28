<!--
Thanks for contributing! Please read CONTRIBUTING.md before opening a pull request.
Keep each pull request to one logical change. Pull requests are squash-merged and the title becomes
the commit subject, so write the title as a Conventional Commit, for example
"fix: keep the query string when following next_page".
-->

### What changes and why

<!-- Link the issue or discussion this addresses (for example, "Fixes #123"). -->

### Compatibility

- [ ] No change to the public SDK surface (client options, resource methods, request or response types)
- [ ] Changes the public surface. The change is described below, with the spec `operationId` it follows.

<!-- New methods also go into the map in tests/test_contract.py.
     CHANGELOG.md is written by the release automation from the pull request title, so don't edit it
     by hand. Mark a breaking change with `!` in the title (for example, "feat!: ...") and a
     `BREAKING CHANGE:` footer. -->

### How I tested it

<!-- The tests you added or changed, and the commands you ran. -->

### AI assistance

<!-- Required when an AI tool generated or substantially rewrote code, tests, documentation or a design in
     this pull request. Autocomplete, spelling and grammar fixes, formatting and mechanical renames don't
     count. See AI_POLICY.md. Choose one: -->

- [ ] No AI assistance
- [ ] AI-assisted. Tool(s): ___ . What it did: ___ . How I verified the result: ___ .

### Checklist

- [ ] Every commit is signed off (`git commit -s`), as described in CONTRIBUTING.md
- [ ] Commits with meaningful AI assistance carry an `Assisted-by:` trailer
- [ ] The pull request title is a Conventional Commit
- [ ] `./scripts/lint` and `./scripts/test` pass locally
- [ ] `README.md`, `api.md` and the docstrings are updated if the public surface changed
