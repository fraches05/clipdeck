# ClipForge release guide

## Local verification

Run the following from the repository root:

```powershell
.venv\Scripts\python -m pytest tests -q
.venv\Scripts\python -m compileall -q src tiktok_uploader main.py
$env:QT_QPA_PLATFORM='offscreen'; .venv\Scripts\python tests\smoke_gui.py
$env:QT_QPA_PLATFORM='offscreen'; .venv\Scripts\python tests\shots_clipforge.py
.venv\Scripts\python main.py --selftest
```

The self-test writes `selftest.log` beside the application data and reports Python packages, the Node signer, Node.js, Chrome, FFmpeg and the local database.

Screenshots for the README are rendered with the native platform plugin so text is real:
`.venv\Scripts\python tests\shots_readme.py` writes `docs/screenshots/*.png`. Re-run it after any UI change and commit the updated images.

## Version

The product version lives in `src/ui/copy.py` (`PRODUCT_VERSION`) and is shown in the sidebar. Bump it before tagging a release and keep the badge in `README.md` in sync.

## FFmpeg

The executable is not bundled. Video randomization is available when `ffmpeg.exe` is in `PATH`, in `ffmpeg\bin\` next to `ClipForge.exe`, or is pointed to by `CLIPFORGE_FFMPEG`. Without it the application still runs and the diagnostics in «Настройки» report the missing binary.

## Windows executable

The supported artifact is a PyInstaller onedir build named `ClipForge`, produced from `ClipForge.spec`:

```powershell
.venv\Scripts\python -m PyInstaller --noconfirm --clean ClipForge.spec
```

Keep the signer data and `fake_useragent`/`undetected_chromedriver` collection options from the README. The generated directory must retain `data/`, `CookiesDir/`, `.env`, and `selftest.log` behavior.

## Before publishing

- Review `git diff --check` and run the complete test suite.
- Do not include `data/`, `CookiesDir/`, `.env`, cookies, or self-test logs in a release archive.
- Test login and a controlled publication only with accounts authorized by the operator.
- Keep `LICENSE` and `docs/THIRD_PARTY.md` in every source distribution.
