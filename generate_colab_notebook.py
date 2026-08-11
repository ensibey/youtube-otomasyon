import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚀 Google Colab Ultra-Fast AI Video API Server (LTX-Video / Wan 2.1)\n",
    "Bu notebook, **hf_transfer (Rust 100MB/s+ yüksek hızlı indirme motoru)** kullanarak modelleri saniyeler içinde indirir ve canlı FastAPI + ngrok API sunucusu olarak çalıştırır."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Yüksek Hızlı hf_transfer ve Kütüphane Kurulumu\n",
    "!pip install -q hf_transfer diffusers transformers accelerate torch torchvision imageio-ffmpeg fastapi uvicorn pyngrok nest_asyncio\n",
    "import os\n",
    "os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'\n",
    "print('✅ Ultra yüksek hızlı hf_transfer indirme motoru aktif edildi!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. LTX-Video / Wan 2.1 Modelinin Hızlı Yüklenmesi\n",
    "import torch\n",
    "from diffusers import LTXPipeline\n",
    "from diffusers.utils import export_to_video\n",
    "\n",
    "print('🚀 AI Video Modeli Yükleniyor (Yüksek Hızlı)...')\n",
    "pipe = LTXPipeline.from_pretrained('Lightricks/LTX-Video', torch_dtype=torch.bfloat16)\n",
    "pipe.to('cuda')\n",
    "print('✅ AI Video Modeli GPU üzerinde hazır!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3. FastAPI + ngrok Canlı Web Sunucusu\n",
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
    "@app.post('/generate_video')\n",
    "def generate_video(req: VideoRequest):\n",
    "    print(f'🎬 Canlı video isteği alındı: {req.prompt}')\n",
    "    frames = pipe(\n",
    "        prompt=req.prompt,\n",
    "        negative_prompt='low quality, blurry, distorted',\n",
    "        width=req.width,\n",
    "        height=req.height,\n",
    "        num_frames=121,\n",
    "        num_inference_steps=25\n",
    "    ).frames[0]\n",
    "    \n",
    "    out_path = '/content/colab_generated_video.mp4'\n",
    "    export_to_video(frames, out_path, fps=24)\n",
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

print("Fast hf_transfer Colab notebook updated successfully!")
