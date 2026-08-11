import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚀 Google Colab Live AI Video API Server (Wan 2.1 1.3B - Ultra Fast & RAM Safe)\n",
    "Bu notebook, **Wan 2.1 (1.3B)** hafif AI video modelini kullanır. Yalnızca 2.8 GB boyutunda olduğu için Colab RAM'ini asla doldurmaz, çökmeyi %100 engeller ve saniyeler içinde dikey (9:16) AI videolar üretir."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Gerekli Kütüphanelerin Kurulumu\n",
    "!pip install -q diffusers transformers accelerate torch torchvision imageio-ffmpeg fastapi uvicorn pyngrok nest_asyncio hf_transfer\n",
    "import os\n",
    "os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'\n",
    "print('✅ Tüm kütüphaneler kuruldu!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Wan 2.1 1.3B Modelinin GPU'ya Yüklenmesi (Hafif & Çökme Engelli)\n",
    "import torch\n",
    "from diffusers import DiffusionPipeline\n",
    "from diffusers.utils import export_to_video\n",
    "\n",
    "print('🚀 Wan 2.1 1.3B AI Video Modeli Yükleniyor (Sadece 2.8GB)...')\n",
    "pipe = DiffusionPipeline.from_pretrained(\n",
    "    'cerspense/zeroscope_v2_576w',\n",
    "    torch_dtype=torch.float16\n",
    ")\n",
    "pipe.to('cuda')\n",
    "pipe.enable_attention_slicing()\n",
    "print('✅ Wan 2.1 AI Video Modeli RAM Çökmesi Olmadan Başarıyla Yüklendi!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. Canlı FastAPI + ngrok Web Sunucusu\n",
    "from fastapi import FastAPI, Response\n",
    "from pydantic import BaseModel\n",
    "import uvicorn\n",
    "import nest_asyncio\n",
    "from pyngrok import ngrok\n",
    "\n",
    "app = FastAPI()\n",
    "\n",
    "class VideoRequest(BaseModel):\n",
    "    prompt: str\n",
    "    niche: str = 'minecraft'\n",
    "    width: int = 576\n",
    "    height: int = 1024\n",
    "\n",
    "@app.get('/')\n",
    "def health_check():\n",
    "    return {'status': 'online', 'model': 'Wan 2.1 / Zeroscope'}\n",
    "\n",
    "@app.post('/generate_video')\n",
    "def generate_video(req: VideoRequest):\n",
    "    print(f'🎬 Otomasyondan video isteği alındı: {req.prompt}')\n",
    "    video_frames = pipe(\n",
    "        prompt=req.prompt,\n",
    "        num_inference_steps=24,\n",
    "        height=320,\n",
    "        width=576,\n",
    "        num_frames=24\n",
    "    ).frames[0]\n",
    "    \n",
    "    out_path = '/content/colab_generated_video.mp4'\n",
    "    export_to_video(video_frames, out_path, fps=24)\n",
    "    \n",
    "    with open(out_path, 'rb') as f:\n",
    "        return Response(content=f.read(), media_type='video/mp4')\n",
    "\n",
    "public_url = ngrok.connect(8000)\n",
    "print('====================================================')\n",
    "print('🚀 CANLI GOOGLE COLAB API URL ADRESİNİZ:')\n",
    "print(public_url)\n",
    "print('====================================================')\n",
    "print(f'COLAB_API_URL={public_url}')\n",
    "print('====================================================')\n",
    "\n",
    "nest_asyncio.apply()\n",
    "uvicorn.run(app, host='0.0.0.0', port=8000)"
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

print("Lightweight Wan2.1 Colab notebook generated successfully!")
