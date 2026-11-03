# Smart Tasks

אפליקציית ווב מקומית לניהול משימות עם עוזר AI (OpenAI Responses API).
האפיון המלא: [`docs/spec.docx`](docs/spec.docx) · פרוטוטייפ: [`docs/prototype/task-ai-prototype.html`](docs/prototype/task-ai-prototype.html)

## מבנה

```
backend/    FastAPI + SQLAlchemy (SQLite) + שירות AI + שכבת הסתרה
frontend/   React + TypeScript + Vite (RTL, פאנל צ'אט מחוץ לראוטר)
docs/       אפיון ופרוטוטייפ
```

## הרצה

```bash
make install            # venv + התקנת תלויות
cp .env.example .env    # למלא OPENAI_API_KEY והמודלים
```

```bash
make dev-backend        # שרת API על 127.0.0.1:8000
```

```bash
make dev-frontend       # Vite על :5173, עם proxy ל-/api
```

```bash
make run                # בנייה + שרת יחיד שמגיש גם את הקליינט
```

```bash
make test               # בדיקות backend
```

## סטטוס לפי שלבי האפיון

| שלב | סטטוס |
|---|---|
| 1. בסיס: DB, API משימות, ארבעה דפים, פריסת RTL | שלד: DB ו-API מלאים; הדפים הם placeholders |
| 2. פרטיות ותיעוד: הסתרה, `ai_actions`, הגדרות | `services/masking.py` ו-`/api/ai-actions` ממומשים; דף הגדרות טרם |
| 3. צ'אט ופעולות | לא התחיל (`routers/chat.py` מחזיר 501) |
| 4. `search_tasks` וסיכום יומי | לא התחיל (`services/ai.py` stub) |
| 5. הקשחה ובדיקות E2E | לא התחיל |

## סטיות מהאפיון

- נוספה טבלה חמישית, `app_settings` (key/value), לאחסון תבניות ההסתרה ופרופיל המשתמש שהאפיון לא הגדיר להם טבלה.
- ל-`PATCH /api/tasks/{id}` נוסף השדה האופציונלי `expected_updated_at` למימוש ה-409 כשהמשימה שונתה מאז ההצעה.
- פרמטרי OpenAI Responses API לא ממומשים עדיין; יש לאמתם מול התיעוד העדכני (כמצוין באפיון).
