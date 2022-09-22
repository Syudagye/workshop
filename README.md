# Boite à Clés - Projet Workshop

## Mise en place

### Materiel

- Arduino Uno (avec cable usb)
- Moteur pas-à-pas
- Pad numérique
- Raspberry Pi 3 (avec batterie ou alimentation)
- Cable pour connecter le tout

### Montage

*todo*

### Software

Au niveau logiciel, il va vous falloir:
- sur votre ordinateur:
- - Arduino IDE
- - ssh
- sur la raspberry pi:
- - python 3
- - pip
- - git
- - ssh

#### Arduino

Ouvrez [workshop/workshop.ino](https://github.com/Syudagye/workshop/blob/master/workshop/workshop.ino) dans Arduino IDE, puis après avoir branché l'arduino, televerserle code dans la carte.

#### Raspberry

Installez Raspberry Pi OS sur le raspberry pi, puis créez un utilisateur avec le groupe `dialout`.
Ou ajouter le groupe à l'utilisateur courrant avec `sudo usermod -aG dialout $(whoami)` (un logout/login est requis pour que les changement s'appliquent)

Une fois ceci fait, il faut se connecter au raspberry pi via ssh pour la suite, car le port usb sera utilisé par l'Arduino.
Quand celà est fait, connectez l'arduino à la raspberry pi. 
Pour verifier qu'il soit bien détecté, verifiez si la commande `ls /dev/ttyACM*` affiche quelque chose.

Installez les dépendances nécessaires:
```bash
sudo apt update
sudo apt upgrade # Il est recommandé de mettre à jour le raspberry pi après l'installation de pi OS, mais ce n'est pas obligatoire
sudo apt install python3 python3-pip git openssh
pip install flask pyserial
```

Copiez le code:
```bash
git clone https://github.com/Syudagye/workshop
cd workshop
```

Puis lancez le script python:
```bash
python main.py
```

Une ip s'affichera dans les logs, vous pourrez l'utiliser pour vous connecter au system via un naviguateur et changer le code de la boite.
(Il est préferable d'utiliser le system sur un réseau local, car il n'a pas été testé via internet).
