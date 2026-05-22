---
title: Two-scheduler deadlock from asyncio.run inside Eventlet-patched Celery workers
date: 2026-05-21
source: claude-code
category: work
tags: [nebula, eventlet, asyncio, celery, concurrency, deadlock]
entities: ["asyncio.run", "Eventlet", "Celery worker", "eventlet.tpool", "get_concurrency_pool"]
status: resolved
related: []
---

## Problem / context

A Celery task in `nebula_license2` intermittently hangs. The worker is
monkey-patched by Eventlet, but the task internally calls `asyncio.run()` to run
async logic. Two event loops end up competing for OS threads, producing a
deadlock.

## Conclusion / solution

Root cause is calling `asyncio.run()` directly inside a monkey-patched
environment. Fix direction:

- Celery path: switch to `eventlet.tpool.execute()` to offload the sync call onto
  a real thread.
- ASGI path: keep `asyncio.to_thread()`.
- Converge both onto the existing `get_concurrency_pool()` abstraction instead of
  each call site doing its own thing.

## Key concepts

- Once monkey-patched, Eventlet intercepts socket / threading and is incompatible
  with a native asyncio event loop.
- General rule: the same logic running under two different runtimes must use
  different concurrency primitives for each.

## Follow-ups

- [ ] Confirm both call sites — `postpaid_v19.py` and `remove_device.py` — are
      converged.
- Eventlet retirement plan: align with Python 3.14.

## Source

(Skill fills in the session link or key excerpts here.)
