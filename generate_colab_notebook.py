import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚀 Google Colab Live AI Video API Server (Jupyter Thread Safe)\n",
    "Bu notebook, **Threading Safe Uvicorn** sunucusu ve Cloudflare Tunnel kullanır. Colab Jupyter event loop hatasını %100 engeller."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Gerekli Kütüphaneler ve Cloudflare Tunnel Kurulumu\n",
    "!pip install -q diffusers transformers accelerate torch torchvision imageio-ffmpeg fastapi uvicorn hf_transfer\n",
    "!wget -q -O cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb\n",
    "!dpkg -i cloudflared.deb\n",
    "import os, torch\n",
    "os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'\n",
    "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n",
    "print(f'✅ Kurulum Tamamlandı! Kullanılan Donanım: {device.upper()}')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Text-to-Video AI Modelinin Yüklenmesi\n",
    "from diffusers import DiffusionPipeline\n",
    "from diffusers.utils import export_to_video\n",
    "\n",
    "print(f'🚀 AI Video Modeli {device.upper()} Üzerinde Yükleniyor...')\n",
    "dtype = torch.float16 if device == 'cuda' else torch.float32\n",
    "pipe = DiffusionPipeline.from_pretrained(\n",
    "    'damo-vilab/text-to-video-ms-1.7b',\n",
    "    torch_dtype=dtype\n",
    ")\n",
    "pipe = pipe.to(device)\n",
    "if device == 'cuda':\n",
    "    pipe.enable_attention_slicing()\n",
    "print('✅ AI Video Modeli Başarıyla Yüklendi!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. Thread-Safe Canlı FastAPI + Cloudflare Sunucusu\n",
    "import subprocess, time, threading\n",
    "from fastapi import FastAPI, Response\n",
    "from pydantic import BaseModel\n",
    "import uvicorn\n",
    "\n",
    "app = FastAPI()\n",
    "\n",
    "class VideoRequest(BaseModel):\n",
    "    prompt: str\n",
    "    niche: str = 'minecraft'\n",
    "    width: int = 256\n",
    "    height: int = 448\n",
    "\n",
    "@app.get('/')\n",
    "def health_check():\n",
    "    return {'status': 'online', 'model': 'ModelScope 1.7B', 'device': device}\n",
    "\n",
    "@app.post('/generate_video')\n",
    "def generate_video(req: VideoRequest):\n",
    "    print(f'🎬 Otomasyondan canlı video isteği alındı: {req.prompt}')\n",
    "    video_frames = pipe(\n",
    "        prompt=req.prompt,\n",
    "        num_inference_steps=20,\n",
    "        height=448,\n",
    "        width=256,\n",
    "        num_frames=16\n",
    "    ).frames[0]\n",
    "    \n",
    "    out_path = '/content/colab_generated_video.mp4'\n",
    "    export_to_video(video_frames, out_path, fps=16)\n",
    "    \n",
    "    with open(out_path, 'rb') as f:\n",
    "        return Response(content=f.read(), media_type='video/mp4')\n",
    "\n",
    "# Start Uvicorn in a background thread to prevent Jupyter asyncio conflict\n",
    "def run_server():\n",
    "    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')\n",
    "\n",
    "thread = threading.Thread(target=run_server, daemon=True)\n",
    "thread.start()\n",
    "time.sleep(2)\n",
    "\n",
    "# Start Cloudflare Tunnel\n",
    "subprocess.Popen(['cloudflared', 'tunnel', '--url', 'http://localhost:8000', '--logfile', '/content/cloudflared.log'])\n",
    "time.sleep(5)\n",
    "\n",
    "print('====================================================')\n",
    "print('🚀 CANLI GOOGLE COLAB API URL ADRESİNİZ:')\n",
    "try:\n",
    "    with open('/content/cloudflared.log') as f:\n",
    "        for line in f:\n",
    "            if 'trycloudflare.com' in line:\n",
    "                urls = [x for x in line.split() if 'trycloudflare.com' in x]\n",
    "                if urls:\n",
    "                    clean_url = urls[0].strip()\n",
    "                    if not clean_url.startswith('http'):\n",
    "                        clean_url = 'https://' + clean_url\n",
    "                    print(clean_url)\n",
    "                    print(f'COLAB_API_URL={clean_url}')\n",
    "except Exception as e:\n",
    "    print('Cloudflare log read info:', e)\n",
    "print('====================================================')"
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

print("Thread-safe Uvicorn Colab notebook generated successfully!")
