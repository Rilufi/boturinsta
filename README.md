# Boturinsta

Posting daily pets on Instagram.

## Requirements
We employ here the unnoficial Instagram private API [instagrapi](https://subzeroid.github.io/instagrapi/)

### How this works?
Both "botgram.py" (cats) and "doglufi.py" (dogs) files consists in the scripts for getting and posting the pets. Everything automated from the GitHub Actions.

#### Where does the pets come from?
The cats come from [The Cat API](https://thecatapi.com/) while the dogs com from [Dog API](https://dog.ceo/dog-api/)

#### Other function(s)
I'm trying to deploy a function for following accounts and liking pictures that post hashtags about cats and dogs, the only problem is to found a way to evade Instagram's request limit. Currently the function that like the most recent post the contains one random hashtag (from the 10 available) per hour, following the account that posted is not working. If it works, I can try to increase the amount, albeit it's risk.

# Agora em português porque nois é BR

Publicando pets todo dia no Instagram.

## Requisitos
Aqui usamos a API privada não oficial do Instagram chamada [instagrapi](https://subzeroid.github.io/instagrapi/).

### Como funciona isso?
Os arquivos `botgram.py` (gatos) e `doglufi.py` (cães) consistem nos scripts para obter e postar os pets. Tudo automatizado através das GitHub Actions.

#### De onde vêm os pets?
Os gatos vêm da [The Cat API](https://thecatapi.com/), enquanto os cães vêm da [Dog API](https://dog.ceo/dog-api/).

#### Outra(s) função(ões)
Estou tentando implementar uma função para seguir contas e curtir fotos que usem hashtags relacionadas a gatos e cães. O único problema é encontrar uma maneira de evitar o limite de solicitações do Instagram. Atualmente, a função que curte a postagem mais recente que contém uma hashtag aleatória (de 10 disponíveis) por hora, seguindo a conta que fez a postagem não está funcionando. Se funcionar, posso tentar aumentar a quantidade, apesar de ser arriscado.
