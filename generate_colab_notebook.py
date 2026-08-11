import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚀 YouTube Shorts AI Video Generator (Google Colab)\n",
    "Bu Colab notebook'u, açık kaynaklı **Wan 2.1 / LTX-Video** AI video modellerini kullanarak dikey (9:16) sinematik oyun klipleri üretir ve doğrudan Google Drive `/Pending` klasörünüze kaydeder."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Google Drive Bağlantısı ve Bağımlılıkların Kurulumu\n",
    "from google.colab import drive\n",
    "import os\n",
    "\n",
    "drive.mount('/content/drive')\n",
    "\n",
    "!pip install -q diffusers transformers accelerate torch torchvision imageio-ffmpeg\n",
    "\n",
    "drive_pending_dir = '/content/drive/MyDrive/YouTube_Automation/Pending'\n",
    "os.makedirs(drive_pending_dir, exist_ok=True)\n",
    "print('✅ Google Drive Pending klasörü hazır:', drive_pending_dir)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Wan 2.1 / LTX-Video Modelini Yükleme ve 9:16 Video Üretimi\n",
    "import torch\n",
    "from diffusers import LTXPipeline\n",
    "from diffusers.utils import export_to_video\n",
    "\n",
    "print('🚀 AI Video Modeli Yükleniyor (GPU)...')\n",
    "pipe = LTXPipeline.from_pretrained('Lightricks/LTX-Video', torch_dtype=torch.bfloat16)\n",
    "pipe.to('cuda')\n",
    "\n",
    "prompts = [\n",
    "    'Cinematic 4k vertical 9:16 footage of a mysterious glowing cavern in Minecraft at night, highly detailed',\n",
    "    'Photorealistic 9:16 vertical video of a player walking in an eerie empty Roblox city street at 3 AM, 60fps'\n",
    "]\n",
    "\n",
    "for idx, prompt in enumerate(prompts, 1):\n",
    "    print(f'🎬 Video {idx} üretiliyor: {prompt}...')\n",
    "    video = pipe(\n",
    "        prompt=prompt,\n",
    "        negative_prompt='low quality, blurry, distorted',\n",
    "        width=576,\n",
    "        height=1024,\n",
    "        num_frames=161,\n",
    "        num_inference_steps=30\n",
    "    ).frames[0]\n",
    "    \n",
    "    output_path = os.path.join(drive_pending_dir, f'colab_ai_video_{idx}.mp4')\n",
    "    export_to_video(video, output_path, fps=24)\n",
    "    print(f'✅ Video kaydedildi: {output_path}')\n",
    "\n",
    "print('🎉 Tüm videolar başarıyla Google Drive Pending klasörüne kaydedildi!')"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open(r"c:\Users\hp\Desktop\youtube otomasyon\Youtube_AI_Video_Generator.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=2, ensure_ascii=False)

print("Notebook generated successfully!")
