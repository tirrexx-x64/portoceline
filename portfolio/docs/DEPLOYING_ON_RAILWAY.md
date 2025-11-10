## Deploying This Django App on Railway

Below is a practical checklist of everything you need to prepare before pointing Railway at this repo, followed by the exact steps inside the Railway dashboard.

### 0. Project preparation (do these in the repo)
1. **Dependencies**  
   - Ensure `gunicorn`, `dj-database-url`, and (optionally) `whitenoise` are listed in `requirements.txt`.  
   - Install them locally and confirm `pip freeze` matches the file.
2. **Settings adjustments**  
   - Update `portfolio/settings.py` so `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `DATABASES` read from environment variables using `dj_database_url`.  
   - If you added WhiteNoise, include `WhiteNoiseMiddleware`, `STATIC_ROOT`, and `STATICFILES_STORAGE`.
3. **Procfile**  
   - Create a `Procfile` in the repo root with `web: gunicorn portfolio.wsgi --log-file -`. Railway will pick this up automatically.
4. **Static assets**  
   - Run `python manage.py collectstatic --noinput` locally to make sure the configuration works before letting Railway execute it.
5. **Secrets & env template**  
   - Optionally add a `.env.example` with all the environment keys you plan to create on Railway (no real secrets).

Once the repo has those pieces committed and pushed to GitHub, move on to the platform.

### 1. Prerequisites
- Railway account + optional CLI (`npm i -g @railway/cli`).
- GitHub repo containing this project.
- A Postgres database (Railway plugin is easiest).

### 2. Configure Railway project
1. In the dashboard choose **New Project → Deploy from GitHub Repo** and pick this repository.
2. After the first build, add the **PostgreSQL** plugin and attach it to the same service. Railway injects `DATABASE_URL`.
3. Under **Variables**, create:

| Variable | Example |
| --- | --- |
| `DJANGO_SECRET_KEY` | Output of `python -c "import secrets; print(secrets.token_urlsafe(64))"` |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `myapp.up.railway.app,mydomain.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://myapp.up.railway.app,https://mydomain.com` |
| `DATABASE_SSL_REQUIRE` | `True` (for Railway Postgres) |
| `EMAIL_*` | Only if the contact form should send email |

Railway sets `RAILWAY_PUBLIC_DOMAIN` automatically; you can include it inside `DJANGO_ALLOWED_HOSTS` if desired.

### 3. Build & run commands
- Railway reads `requirements.txt` to install dependencies.
- The `Procfile` tells Railway to start Gunicorn.
- Configure the build command under **Deployments → Settings → Build Command**:  
  `python manage.py collectstatic --noinput`

### 4. Database migrations
After the service is up and `DATABASE_URL` exists:
```bash
railway link               # one-time link between CLI and project
railway run python manage.py migrate
```
This executes migrations inside Railway’s environment against the hosted Postgres.

### 5. Custom domain (optional)
1. Open the service → **Domains** → **Add Domain** → enter `yourdomain.com`.
2. Railway reveals the DNS record (CNAME/A). Add it at your registrar (Cloudflare, Namecheap, etc.).
3. Once DNS propagates, Railway issues HTTPS certificates. Remember to include the domain inside `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`.

### 6. Local parity tips
- Maintain a `.env` locally:
  ```
  DJANGO_DEBUG=True
  DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
  DATABASE_URL=sqlite:///db.sqlite3
  ```
- Run `python manage.py collectstatic --noinput` and `python manage.py migrate` locally before pushing to avoid surprises.

When these preparations are finished, you can simply push to GitHub; Railway will rebuild and redeploy automatically using the exact configuration described above.
