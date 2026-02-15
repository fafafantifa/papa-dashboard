# Papa Dashboard

Starter monorepo scaffold for a dashboard app.

## What is included

- `apps/web`: Next.js app with a basic home page and first `Overview` page scaffold
- `packages/*`: shared workspace packages (`config`, `types`, `sdk`, `utils`, `ui`)
- `docs/*`: architecture, onboarding, and product notes placeholders
- `infra/*`: placeholder directories for docker/terraform/scripts
- `.github/workflows`: CI and preview placeholder workflows

## Quick start

```bash
npm install
cp .env.example .env.local
npm run dev
```

Then open:

- `http://localhost:3000/` (home)
- `http://localhost:3000/overview` (first dashboard slice)
- `http://localhost:3000/api/overview` (sample API response)

## Repo structure

```txt
apps/
  web/
packages/
  config/
  sdk/
  types/
  ui/
  utils/
infra/
  docker/
  terraform/
  scripts/
docs/
  architecture/
  onboarding/
  product/
.github/
  workflows/
```

## Next implementation steps

1. Add Prisma schema + migration and replace mocked overview metrics.
2. Add Auth.js/NextAuth and role checks for protected routes.
3. Add component tests and Playwright smoke tests for Overview.
4. Replace inline styles with Tailwind or shared `@papa/ui` components.
