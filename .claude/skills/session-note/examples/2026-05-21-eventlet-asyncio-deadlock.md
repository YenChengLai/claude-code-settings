---
title: Two-scheduler deadlock from asyncio.run inside Eventlet-patched Celery workers
date: 2026-05-21
source: claude-code
category: work
tags: [eventlet, asyncio, celery, concurrency, deadlock, python]
entities: ["asyncio.run", "Eventlet", "Celery worker", "eventlet.tpool", "asyncio.to_thread"]
status: resolved
related: []
---

## Problem / context

A Celery task intermittently hangs. The worker is monkey-patched by Eventlet,
but the task internally calls `asyncio.run()` to run async logic. Two event
loops end up competing for OS threads, producing a deadlock.

## Conclusion / solution

Root cause is calling `asyncio.run()` directly inside a monkey-patched
environment. Fix direction:

- Celery path (Eventlet workers): switch to `eventlet.tpool.execute()` to
  offload the sync call onto a real thread.
- ASGI path (asyncio): keep `asyncio.to_thread()`.
- Converge both call sites onto a single concurrency helper instead of each
  one rolling its own dispatch.

## Key concepts

- Once monkey-patched, Eventlet intercepts socket / threading and is incompatible
  with a native asyncio event loop.
- General rule: the same logic running under two different runtimes must use
  different concurrency primitives for each.

## Follow-ups

- [ ] Audit other call sites for the same anti-pattern.
- [ ] Eventlet retirement plan: align with Python 3.14 deprecations.

## Source

(Skill fills in the session link or key excerpts here.)
