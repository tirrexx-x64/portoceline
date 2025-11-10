## Deploying on Railway (GitHub Workflow)

### 1. Prerequisites
- Railway account + CLI (`npm i -g @railway/cli`) or just the dashboard.
- Repository pushed to GitHub (Railway pulls from GitHub). Ensure `Procfile`, `requirements.txt`, `manage.py`, and `portfolio/settings.py` are in root.
- Managed Postgres database (Railway plugin works great).

### 2. Configure Railway project
1. In Railway dashboard click **New Project → Deploy from GitHub Repo** and select this repository.
2. After first build finishes, add the **PostgreSQL** plugin and attach it to the same service. Railway injects `DATABASE_URL` automatically.
3. In the service → **Variables** tab, set:

| Variable | Example |
| --- | --- |
| `DJANGO_SECRET_KEY` | `python -c "import secrets; print(secrets.token_urlsafe(64))"` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `myapp.up.railway.app,mydomain.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://myapp.up.railway.app,https://mydomain.com` |
| `EMAIL_*` | Optional SMTP creds |
| `DATABASE_SSL_REQUIRE` | `True` (Railway Postgres is SSL-enabled) |

Railway also exposes `RAILWAY_PUBLIC_DOMAIN`; settings automatically allow it if you leave `DJANGO_ALLOWED_HOSTS` empty.

### 3. Build & run commands
- Railway auto-detects Python via `requirements.txt`.
- `Procfile` already sets the start command: `web: gunicorn portfolio.wsgi --log-file -`.
- Add a build command in the dashboard (Service → Deployments → Settings → Build → `python manage.py collectstatic --noinput`) so static assets are prepared before each release.

### 4. Database migrations
Once the service is running and `DATABASE_URL` is available:
```bash
railway link          # run locally once
railway variables     # confirm env vars
railway run python manage.py migrate
```
That executes migrations inside the remote container against the managed Postgres instance.

### 5. Custom domain
1. Under the service’s **Domains** tab, click **Add Domain** → type `yourdomain.com`.
2. Railway shows the required CNAME/A record. Create it at your registrar (Namecheap, Cloudflare, etc.).
3. After DNS propagates, Railway issues HTTPS certificates. Add the same hostname to `DJANGO_ALLOWED_HOSTS` & `DJANGO_CSRF_TRUSTED_ORIGINS`.

### 6. Local development parity
Create a `.env` (not committed) for local testing:
```
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
```
Run `python manage.py collectstatic --noinput` before pushing if you want to mirror production’s static workflow.

With these steps you only need to push to GitHub; Railway rebuilds & redeploys automatically, and your custom domain + Postgres stay wired up.
