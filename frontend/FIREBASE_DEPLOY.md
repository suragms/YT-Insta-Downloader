# Firebase deploy troubleshooting

## "Failed to make request to firebasehosting.googleapis.com" or "An unexpected error"

Do these in order:

### 1. Re-login to Firebase (fixes most auth/request errors)

In a terminal (prefer **Windows PowerShell** or **Command Prompt** opened normally, not inside Cursor):

```bash
firebase login --reauth
```

Sign in in the browser, then run:

```bash
cd frontend
npm run build
firebase deploy --only hosting
```

### 2. Fix Firebase CLI config folder (if you see "update check failed" / "get access to ... .config")

The CLI writes to `C:\Users\<You>\.config`. If that fails, deploy can error.

- **Option A:** Run `firebase deploy` from a **normal terminal** (e.g. Windows PowerShell) **outside Cursor**, so the CLI can write to your user folder.
- **Option B:** Give your user full control over the config folder:
  1. Open File Explorer → `C:\Users\Surag\.config`
  2. If it doesn’t exist, run `firebase login --reauth` once from a normal terminal so it gets created.
  3. Right-click `.config` → Properties → Security → Edit → select your user → check **Full control** → OK.

### 3. Enable Firebase Hosting API (if you get 403 / "resource not accessible")

1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Select project **yt-insta-downloader**.
3. **APIs & Services** → **Enable APIs and Services** → search **Firebase Hosting API** → **Enable**.

### 4. Network / firewall

- Ensure you can open: https://firebasehosting.googleapis.com in a browser (or that it’s not blocked).
- Try turning off VPN or using another network.

### Quick deploy (after the above is fixed)

From project root:

```bash
cd frontend
npm run deploy
```

Or: `npm run build` then `firebase deploy --only hosting`.
