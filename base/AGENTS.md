# /base/ AGENTS.md

## OVERVIEW
Core Django domain logic.

## STRUCTURE
```
base/
├── models.py    # Data models (Profile, Post, Comment)
├── views.py     # Request handlers
├── forms.py     # Django form logic
└── urls.py      # App-level routing
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| Routing | base/urls.py | All primary app routes |
| Logic | base/views.py | Business logic |

## CONVENTIONS
- All domain logic here, not in `/rhixecompany/`.
- Greenfield testing: Use `base/tests.py` or `base/test_*.py` for new tests.

## ANTI-PATTERNS
- No logic in `models.py` that should be in a Service layer (though no Service layer exists yet).
