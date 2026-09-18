# AlphaInsider skill catalog

Routable specialists and their canonical sources. The API skill is hosted by
Mintlify; Strategy Creator is published from this repository.

## alphainsider-api

- When to use: REST or WebSocket API behavior, request examples,
  authentication, orders, positions, bots, market data, billing, or streams.
- Read the [hosted API skill](https://api.alphainsider.com/skill.md) and its linked
  guides; no GitHub API package or persistent installation is required.
- Install only when requested:

  ```bash
  npx skills@latest add https://api.alphainsider.com --skill alphainsider-api
  ```

## alphainsider-strategy-creator

- When to use: define, backtest, implement, schedule, run, resume, recover,
  or update an AlphaInsider paper strategy with a persistent project plan.
- Read the [Strategy Creator skill](https://raw.githubusercontent.com/AlphaInsider/skills/master/skills/alphainsider-strategy-creator/SKILL.md) and its required references.
- Install:

  ```bash
  npx skills@latest add https://github.com/AlphaInsider/skills \
    --skill alphainsider-strategy-creator
  ```
