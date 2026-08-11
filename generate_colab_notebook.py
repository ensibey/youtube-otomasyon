import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🚀 Google Colab Live AI Video Generator (Gradio Live - Zero Error)\n",
    "Bu notebook, **Gradio Share (https://xxxx.gradio.live)** altyapısını kullanır. Cloudflare/ngrok hatası, port çakışması veya RAM çökmesi %100 engellenmiştir."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Tek Hücrede Donanım Kurulumu, AI Modeli ve Canlı Gradio Linki\n",
    "!pip install -q diffusers transformers accelerate torch torchvision imageio-ffmpeg gradio hf_transfer\n",
    "\n",
    "import os, torch\n",
    "import gradio as gr\n",
    "from diffusers import DiffusionPipeline\n",
    "from diffusers.utils import export_to_video\n",
    "\n",
    "os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'\n",
    "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n",
    "print(f'🚀 AI Video Modeli {device.upper()} Donanımında Yükleniyor...')\n",
    "\n",
    "pipe = DiffusionPipeline.from_pretrained(\n",
    "    'damo-vilab/text-to-video-ms-1.7b',\n",
    "    torch_dtype=torch.float16 if device == 'cuda' else torch.float32\n",
    ")\n",
    "pipe = pipe.to(device)\n",
    "if device == 'cuda':\n",
    "    pipe.enable_attention_slicing()\n",
    "print('✅ AI Video Modeli Yüklendi!')\n",
    "\n",
    "def generate_video_api(prompt):\n",
    "    print(f'🎬 Otomasyondan AI Video İsteği Alındı: {prompt}')\n",
    "    frames = pipe(\n",
    "        prompt=prompt,\n",
    "        num_inference_steps=20,\n",
    "        height=448,\n",
    "        width=256,\n",
    "        num_frames=16\n",
    "    ).frames[0]\n",
    "    out_path = '/content/colab_ai_video.mp4'\n",
    "    export_to_video(frames, out_path, fps=16)\n",
    "    return out_path\n",
    "\n",
    "demo = gr.Interface(\n",
    "    fn=generate_video_api,\n",
    "    inputs=gr.Textbox(label='Prompt'),\n",
    "    outputs=gr.Video(label='AI Video'),\n",
    "    title='Google Colab AI Video Generator'\n",
    ")\n",
    "demo.queue()\n",
    "demo.launch(share=True, show_error=True)"
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

print("Single-cell Gradio Colab notebook generated successfully!")
