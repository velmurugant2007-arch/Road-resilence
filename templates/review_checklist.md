# Self-Review Checklist

## Before Submitting Any Deliverable

Use this checklist before creating a pull request, presenting results, or marking a task as complete.

---

### Scientific Correctness
- [ ] All claims are supported by evidence or references
- [ ] No metrics are hallucinated or estimated without disclosure
- [ ] Statistical methods are appropriate for the data
- [ ] Baseline comparisons are fair and documented

### Technical Correctness
- [ ] Code runs without errors
- [ ] Edge cases are handled
- [ ] Error messages are informative
- [ ] No hardcoded values without justification
- [ ] Dependencies are documented

### Documentation
- [ ] Relevant docs/ files are updated
- [ ] Memory files are updated (decisions, progress, daily log)
- [ ] Wiki pages are updated if domain knowledge changed
- [ ] Code comments explain "why", not "what"
- [ ] README is current

### Traceability
- [ ] Changes trace to a requirement (REQ-XXXX) or innovation (IDEA-XXXX)
- [ ] Design decision is recorded in memory/decisions.md
- [ ] Architecture changes are recorded in memory/architecture_history.md

### Testing
- [ ] Relevant tests are written or updated
- [ ] All tests pass
- [ ] Test coverage is adequate for the change

### Reproducibility
- [ ] Another engineer could reproduce these results
- [ ] Environment/dependencies are documented
- [ ] Random seeds are set (for ML experiments)
- [ ] Data sources are documented

### Quality
- [ ] Code follows coding standards
- [ ] No unnecessary complexity
- [ ] Performance implications are considered
- [ ] Security implications are considered (if applicable)

### Final Question
- [ ] **Would an ISRO scientist approve this work?**
