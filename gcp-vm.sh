# Create instance
gcloud compute instances create ai-train-gpu-spot \
    --project=biba-bop \
    --zone=asia-east1-c \
    --machine-type=n1-standard-4 \
    --network-interface=network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=default \
    --no-restart-on-failure \
    --maintenance-policy=TERMINATE \
    --provisioning-model=SPOT \
    --instance-termination-action=STOP \
    --service-account=biba-bop@biba-bop.iam.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --accelerator=count=1,type=nvidia-tesla-t4 \
    --tags=http-server,https-server \
    --create-disk=auto-delete=yes,boot=yes,device-name=ai-train-gpu-spot,image=projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20241219,mode=rw,size=200,type=pd-balanced \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud \
    --reservation-affinity=any

# Inside instance
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  wget \
  curl \
  llvm \
  libncurses5-dev \
  libncursesw5-dev \
  xz-utils \
  tk-dev \
  libffi-dev \
  liblzma-dev \
  python3-openssl \
  git \
  make \
  libbz2-dev

# PyEnv
curl https://pyenv.run | bash

# Ajoutez ces lignes à la fin de votre fichier ~/.bashrc
cat << 'EOF' >> ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"
EOF

source ~/.bashrc
pyenv install 3.10.6
pyenv global 3.10.6

# GPU
# guide: https://cloud.google.com/compute/docs/gpus/install-drivers-gpu#install-script
# if sudo doesn't work:
# sudo nano /etc/sudoers.d/google-sudoers
# add:
# %google-sudoers ALL=(ALL:ALL) NOPASSWD:ALL
curl -L https://github.com/GoogleCloudPlatform/compute-gpu-installation/releases/download/cuda-installer-v1.2.0/cuda_installer.pyz --output cuda_installer.pyz
sudo python3 cuda_installer.pyz install_driver # it will restart the VM
# Après vérifie l'installation avec :
nvidia-smi

# Display pics
sudo apt update
sudo apt install catimg

# Set up the project
git clone https://github.com/GaParmar/img2img-turbo.git
cd img2img-turbo

pyenv virtualenv 3.10.6 img2img
echo "img2img" > .python-version
pyenv activate img2img

pip install -r requirements.txt
# Downgrade
pip install huggingface-hub==0.25.0
pip install peft==0.13.2
pip install torchvision==0.15.2 # for Kaggle

# To test that CUDA is available in Python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
