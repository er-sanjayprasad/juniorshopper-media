# User preferences (override the defaults in the daily task)
- Language: Hindi for all videos.
- Lengths: U Toon episodes and Bizarre Brain explainers must be 5-8 minutes or more. Shorts 30-45 s.
- Bizarre Brain narrator: ElevenLabs voice "Brian" nPczCjzI2devNBz1zQrb (stability 0.5, style 0.3) until the user picks another; update this line when they do.
- U Toon: Indian school-cartoon style (toolkit/toon.py) with walking/blinking/gestures; ElevenLabs character voices per README.
- Junior Shopper Shorts style: the user wants Pixar-like 3D animation.
  - If the GitHub secret FAL_KEY exists (check fal_out/log.txt after pushing a fal_jobs/*.json; "FAL_KEY secret is missing" means not set), make the Short from 6-8 AI clips: write fal_jobs/<date>-<name>.json (see tools/fal_video.py docstring; same character description in every image_prompt for consistency; aspect 9:16; 5 s clips), push, poll fal_out/<name>/, then cut the clips together with the ElevenLabs voice-over, Hindi captions and the juniorshopper.com end card.
  - If FAL_KEY is not set, use the stickman style (toolkit/example_short_rain_alarm.py) and say so in the message.
- WhatsApp: write a daily Hindi WhatsApp channel post for Junior Shopper (user pastes it).
- Save every day's files to D:\recording\claudevideo\YYYY-MM-DD\ when the computer is reachable, and to daily/YYYY-MM-DD/ in this repo.
