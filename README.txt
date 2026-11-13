NEXOVERSE - FastAPI + Supabase enquiry form

IMPORTANT SECURITY
The backend requires a server-side Supabase secret key (sb_secret_...) or legacy service_role key. Do NOT put this key in HTML/JavaScript, commit it to GitHub, or share it in chat. The publishable/anon key is not used by this backend.

SETUP
1. Open the NEXOVERSE folder in VS Code.
2. In the project root, create a file named .env (same level as index.html).
3. Add these two lines using your own Supabase values:
   SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
   SUPABASE_SECRET_KEY=YOUR_SERVER_SIDE_SECRET_KEY
4. In Supabase Dashboard, get the server-side secret key from Project Settings > API Keys. Use a Secret key (sb_secret_...) or, if using legacy keys, service_role. Never use the publishable/anon key for this backend configuration.
5. In the VS Code terminal, from the NEXOVERSE folder, run:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r backend/requirements.txt
   uvicorn backend.main:app --reload
6. Open http://127.0.0.1:8000 (not index.html directly and not Live Server).
7. Submit a test enquiry. It should appear in Supabase Table Editor > public.enquiries.

DATABASE
Keep the existing public.enquiries table. Because the server-side secret/service_role key bypasses RLS, do not expose it to the browser. You may keep RLS enabled.

FORM
The existing HTML/CSS design is preserved. JavaScript submits to /api/enquiries without refreshing the page and shows success/error feedback.
