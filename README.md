# 📸 Boturinsta - Bot de Pets 🇧🇷

Sistema automatizado para postar fotos diárias de pets no Instagram.

## 🛠 Tecnologias
- Python
- Instagrapi (API não oficial do Instagram)
- The Cat API e Dog API
- Google Gemini API (para legendas)

## 🐾 Fontes de Conteúdo
- **Gatos**: [The Cat API](https://thecatapi.com)
- **Cachorros**: [Dog API](https://dog.ceo/dog-api)
- **Gatos AI**: [These Cats Do Not Exist](https://thesecatsdonotexist.com)

## ⚙️ Funcionamento
1. Baixa imagem da API de pets
2. Gera legenda com Gemini
3. Posta no Instagram
4. Interage com posts relevantes (com limites)

## ⚠️ Desafios
- Limites rigorosos do Instagram
- Necessidade de autenticação manual periódica
- Risco de bloqueio por automação

## 🏃‍♂️ Como Executar
1. Configure credenciais no `auth.py`
2. Instale dependências:
```
pip install -r requirements.txt
```
ou
```
pip install instagrapi google-generativeai requests
```
3. Execute:
```
python botgram.py # Para gatos
python doglufi.py # Para cachorros
```

## 📫 Contato
- Criado por Yuri Abuchaim
- [Instagram @boturinsta](https://instagram.com/boturinsta)
- yuri.abuchaim@gmail.com

===========================================

# 📸 Boturinsta - Pet Bot 🇺🇸

Automated system to post daily pet photos on Instagram.

## 🛠 Technologies
- Python
- Instagrapi (Instagram unofficial API)
- The Cat API and Dog API
- Google Gemini API (for captions)

## 🐾 Content Sources
- **Cats**: [The Cat API](https://thecatapi.com)
- **Dogs**: [Dog API](https://dog.ceo/dog-api)
- **AI Cats**: [These Cats Do Not Exist](https://thesecatsdonotexist.com)

## ⚙️ How It Works
1. Downloads image from pet API
2. Generates caption with Gemini
3. Posts to Instagram
4. Interacts with relevant posts (with limits)

## ⚠️ Challenges
- Instagram strict limits
- Periodic manual authentication required
- Risk of automation bans

## 🏃‍♂️ How to Run
1. Configure credentials in `auth.py`
2. Install dependencies:
```
pip install -r requirements.txt
```
or
```
pip install instagrapi google-generativeai requests
```
3. Run:
```
python botgram.py # For cats
python doglufi.py # For dogs
```

## 📫 Contact
- Created by Yuri Abuchaim
- [Instagram @boturinsta](https://instagram.com/boturinsta)
- yuri.abuchaim@gmail.com
