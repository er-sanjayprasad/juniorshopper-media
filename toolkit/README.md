# U Toon / JuniorShopper video toolkit

Everything a fresh session needs to make videos the same way as before.

## Files
- `toon.py` – Indian school-cartoon character rig (`Char`, `draw`) used for U Toon. Cast: Golu (wide=1.35, hair neat), Pinky (girl, ponytail), Bunty (spiky, skin 236,192,150), Chintu (small 0.82, glasses, skin 214,168,122), Sharma Ma'am (adult, saree, bun, glasses).
- `stick_ui.py` – shared UI helpers: Hindi font `hfont` (Baloo 2), `pop_text`, `tag`, `subscribe_banner` (mid-roll like/subscribe), `end_bg`, `thumbs`, `bell`. Originally also a stickman rig (older style, not used now).
- `example_episode_golu_tiffin.py` + `example_script_golu_tiffin.py` – full episode engine example (scenes, camera zoom, props, end card, rendering one mp4 per segment, then concat).
- `example_short_rain_alarm.py` – vertical 1080x1920 JuniorShopper Short example.
- `utoon_intro_30fps.mp4` – the channel intro (1920x1080, 30 fps, AAC 48k stereo); concat it before every U Toon long video with `-c copy`.

## Setup in a fresh workspace
- Font: `curl -sL -o Baloo2.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/baloo2/Baloo2%5Bwght%5D.ttf"` and point `BALOO` in stick_ui.py to it.
- Fallback offline voices (robotic): kokoro-onnx (`pip install kokoro-onnx soundfile`, models from github.com/thewh1teagle/kokoro-onnx releases model-files-v1.0), Hindi voices hf_alpha/hf_beta/hm_omega/hm_psi with lang="hi"; kid voices pitched up with ffmpeg asetrate.

## Natural voices (ElevenLabs via GitHub Actions)
The workspace cannot reach ElevenLabs. Write `jobs/<name>.json` (see `jobs/test-voices.json`), commit and push; the "Make voices" workflow writes `audio/<name>/<id>.mp3` and `audio/log.txt`, then commits. Poll raw.githubusercontent.com or `git pull` until the files exist (1–3 min). Read `audio/log.txt` for errors.

## Rules
- U Toon: Hindi, Made for Kids, no product promotion, intro at start, like/subscribe mid-roll + end card. Comedy with the recurring cast first; also kid-safe spooky (funny/harmless reveal), mystery, village, festival stories. Target 6–8 min.
- JuniorShopper: entertaining mini-stories/experiments in the SAME toon.py cartoon style as U Toon (vertical), no prices in videos, end with juniorshopper.com + free delivery. See toolkit/preferences.md (it overrides everything).
- Post JuniorShopper Reels to Instagram via Windsor.ai (account 17841473474758835) using a public raw.githubusercontent.com URL of the mp4 pushed to this repo. YouTube: user uploads manually until advanced features are approved (Junior Shopper account 119188, U Toon account 119206 in Windsor).

## ElevenLabs voices in use (paid Starter plan, model eleven_multilingual_v2)
The API key lacks the voices_read permission, so voices are picked by known premade IDs:
- U Toon narrator: Rachel 21m00Tcm4TlvDq8ikWAM
- Golu: Josh TxGEqnHWrfWFTfGW9XjX, pitched up x1.15 with ffmpeg
- Pinky: Elli MF3mGyEYCl7XYWbV9V6O
- Bunty: Antoni ErXwobaYiN019PkySvjV, pitched up x1.15
- Chintu: Gigi jBpfuIE2acCO8z3wKNLl
- Kids chorus: Mimi zrHiDhphv9ZnVXBqCLjz
- Nani / teacher: Matilda XrExE9yKIg1WjnnlVkGX
- Village boy Raju: Adam pNInz6obpgDQGcFmaJgB pitched x1.2; owl/sfx Adam pitched x0.85
- Bizarre Brain narrator: see toolkit/preferences.md (user-chosen voices P1bg08DkjqiVEzOn76yG / JlfM9BOUS7FcsHfTqsAy)
- U Toon kids settings: stability 0.35, style 0.45

## Animation rules (user asked: characters must walk, blink, move — never slide)
- `toon.draw(..., walk=phase)` gives a stepping walk with arm swing and body bob; pass a phase that grows with distance moved (see PREV/PHASE logic in example_episode_bargad_bhoot.py: phase += |dx| / (190 * scale)).
- Idle breathing, head nod while talking and an automatic hand gesture while talking are built into `draw` (needs `t`).
- Blink with the `blink()` helper in the episode example (natural timing, occasional double blink).
- Characters turn their eyes toward whoever is speaking.
- Any character that changes position on screen must walk in, not slide.
