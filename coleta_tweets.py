
# # Grupo: Alecssander, Fabrício e Tadeu
# # Imports


import tweepy
import pandas as pd


# # Autenticação


consumer_key="TSvkn4AbluvhcyMxoXa6kZadk"
consumer_secret="CAi74vgNKbV6fUHSWMkkUwXw3fzWoUodt1ZUBzrfB3wehI4ojk"

access_key="2390129466-uYg2avVy7MpsaqIOv0f21iivGHqf3xvXvL3dhnj"
access_secret="HeZyOC60OcRiA1uLPEu2w7w5If2qON9RI6RN4WRLFEqpE"

autenticacao = tweepy.OAuthHandler(consumer_key, consumer_secret)
autenticacao.set_access_token(access_key, access_secret)
coletor = tweepy.API(auth_handler=autenticacao)


# # Pesquisa

pesquisa = input("Digite o texto a ser pesquisado: ")
qtditems = int(input("Digite a quantidade de tweets: "))
int(qtditems/2)

usuarios = []
nomes = []
descricoes = []
qtdseguidores = []
textos = []
retweets = []
favorites = []

for item in tweepy.Cursor(coletor.search, q= pesquisa + " -filter:retweets", tweet_mode='extended', lang="pt", result_type='recent').items(int(qtditems/2)):
    json = item._json
    
    usuario = json['user']["screen_name"]
    nome = json['user']["name"]
    descricao = json['user']["description"]
    seguidores = json['user']["followers_count"]
    texto = json['full_text']
    texto = texto[json['display_text_range'][0]:json['display_text_range'][1]]
    retweet = json['retweet_count']
    favorite = json['favorite_count']
    
    usuarios.append(usuario)
    nomes.append(nome)
    descricoes.append(descricao)
    qtdseguidores.append(seguidores)
    textos.append(texto)
    retweets.append(retweet)
    favorites.append(favorite)
    
for item in tweepy.Cursor(coletor.search, q= pesquisa + " -filter:retweets", tweet_mode='extended', lang="pt", result_type='popular').items(int(qtditems/2)):
    json = item._json
    
    usuario = json['user']["screen_name"]
    nome = json['user']["name"]
    descricao = json['user']["description"]
    seguidores = json['user']["followers_count"]
    texto = json['full_text']
    texto = texto[json['display_text_range'][0]:json['display_text_range'][1]]
    retweet = json['retweet_count']
    favorite = json['favorite_count']
    
    usuarios.append(usuario)
    nomes.append(nome)
    descricoes.append(descricao)
    qtdseguidores.append(seguidores)
    textos.append(texto)
    retweets.append(retweet)
    favorites.append(favorite)

# # Resultados

dataframe = pd.DataFrame({'Usuario':usuarios, 'Nome':nomes, 'Descrição':descricoes, 'Seguidores':qtdseguidores, 'Texto':textos,
                          'Retweets':retweets, 'Favoritos':favorites})

dataframe['Buzz'] = dataframe.Retweets + dataframe.Favoritos
dataframe['Influencer'] = dataframe.Retweets * dataframe.Seguidores


def OrdenarBuzz(dataframe):
    novodf = dataframe.sort_values(by='Buzz', axis=0, ascending=False)[['Usuario', 'Buzz', 'Texto']].reset_index(drop=True)[:10]
    novodf = novodf.loc[novodf.Buzz > 0]
    print(novodf)
    
def OrdenarInfluencer(dataframe):
    novodf = dataframe.sort_values(by='Influencer', axis=0, ascending=False)[['Usuario', 'Influencer', 'Texto']].reset_index(drop=True)[:10]
    novodf = novodf.loc[novodf.Influencer > 0]
    print(novodf)
    
def OrdenarSeguidores(dataframe):
    novodf = dataframe.sort_values(by='Seguidores', axis=0, ascending=False)[['Usuario', 'Seguidores']].reset_index(drop=True)[:10]
    novodf = novodf.loc[novodf.Seguidores > 0]
    print(novodf)


print('\n\nTop 10 tweets ordenados por Buzz:')
OrdenarBuzz(dataframe)

print('\n\nTop 10 tweets ordenados por Influencer:')
OrdenarInfluencer(dataframe)

print('\n\nTop 10 usuários ordenados por Seguidores:')
OrdenarSeguidores(dataframe)

dataframe.to_csv("tweets.csv")


