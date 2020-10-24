# Core Pkgs
import streamlit as st 

# EDA Pkgs
import pandas as pd 
import numpy as np 


# Utils
import os
import joblib 
import hashlib
import sklearn
from sklearn.linear_model import LogisticRegression

import sys
reload(sys)
sys.setdefaultencoding("UTF-8")

# Data Viz Pkgs
import matplotlib
matplotlib.use('Agg')


# DB
from manage_db import *

# Password 
def generate_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()


def verify_hashes(password,hashed_text):
	if generate_hashes(str(password)) == hashed_text:
		return hashed_text
	return False

feature_names_toddlers = ['a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','age_mons','sex','jaundice','family_mem_with_asd']
feature_names_aq10 = ['a1_score', 'a2_score', 'a3_score', 'a4_score', 'a5_score', 'a6_score','a7_score', 'a8_score', 'a9_score', 'a10_score', 'age', 'gender','jundice', 'austim']
sex_dict = {"m": 0, "f":1}
feature_dict = {"Sim":0, "Não":1}
#Toddlers
answer_dict_frequencia =  {"Sempre":0, "Habitualmente":0, "As vezes":1, "Raramente":1, "Nunca":1}
answer_dict_facilidade = {"Muito Fácil":0, "Bastante Fácil":0, "Bastante Difícil":1, "Muito Difícil":1, "Impossivel":1}
answer_dict_semana = {"Muitas vezes por dia":0, "Algumas vezes por dia":0, "Algumas vezes por semana":1, "Menos de uma vez por semana":1, "Nunca":1}
answer_dict_semana_10 = {"Muitas vezes por dia":1, "Algumas vezes por dia":1, "Algumas vezes por semana":1, "Menos de uma vez por semana":0, "Nunca":0}
answer_dict_fala = {"Muito comuns":0, "Bastante comuns": 0, "Ligeiramente incomuns": 1,	"Muito incomuns":1, "Minha criança não fala":1}
answer_dict_AQ10_pt1 ={"Concordo Totalmente":1,"Concordo Levemente":1,"Discordo Levemente":0,"Discordo Totalmente":0}
answer_dict_AQ10_pt2 ={"Concordo Totalmente":0,"Concordo Levemente":0,"Discordo Levemente":1,"Discordo Totalmente":1}

def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value

def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return key

def get_fvalue(val):
    feature_dict = {"Sim":0, "Não":1}
    answer_dict_frequencia =  {"Sempre":0, "Habitualmente":0, "As vezes":1, "Raramente":1, "Nunca":1}
    answer_dict_facilidade = {"Muito Fácil":0, "Bastante Fácil":0, "Bastante Difícil":1, "Muito Difícil":1, "Impossivel":1}
    answer_dict_semana = {"Muitas vezes por dia":0, "Algumas vezes por dia":0, "Algumas vezes por semana":1, "Menos de uma vez por semana":1, "Nunca":1}
    answer_dict_semana_10 = {"Muitas vezes por dia":1, "Algumas vezes por dia":1, "Algumas vezes por semana":1, "Menos de uma vez por semana":0, "Nunca":0}
    answer_dict_fala = {"Muito comuns":0, "Bastante comuns": 0, "Ligeiramente incomuns": 1,	"Muito incomuns":1, "Minha criança não fala":1}
    answer_dict_AQ10_pt1 ={"Concordo Totalmente":1,"Concordo Levemente":1,"Discordo Levemente":0,"Discordo Totalmente":0}
    answer_dict_AQ10_pt2 ={"Concordo Totalmente":0,"Concordo Levemente":0,"Discordo Levemente":1,"Discordo Totalmente":1}
   
    for key, value in feature_dict.items():
        if val == key:
            return value

    for key, value in answer_dict_frequencia.items():
        if val == key:
            return value

    for key, value in answer_dict_facilidade.items():
        if val == key:
            return value

    for key, value in answer_dict_semana.items():
        if val == key:
            return value
   
    for key, value in answer_dict_semana_10.items():
        if val == key:
            return value

    for key, value in answer_dict_fala.items():
        if val == key:
            return value

    for key, value in answer_dict_AQ10_pt1.items():
        if val == key:
            return value
            
    for key, value in answer_dict_AQ10_pt2.items():
        if val == key:
            return value
    



def load_model(model_file):
   
    loaded_model = joblib.load(open(os.path.join(model_file), "rb"))
    return loaded_model

def main():
    st.title("Sistema para Detecção do Transtorno de Espectro Autista")


    menu = ["Home", "Login", "SignUp"]
    submenu = ["Crianças Pequenas", "Crianças", "Adolescentes", "Adultos"]

    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        st.image("Autismo-fita3.jpg", width=100)
        st.text("O que é Autismo?")

        st.write("O transtorno do espectro do autismo (TEA), é caracterizado por uma desordem no desenvolvimento neurológico definida por três déficits principais: comunicação prejudicada, interação social recíproca prejudicada e padrões restritos, repetitivos e estereotipados de comportamentos ou interesses. A apresentação dessas deficiências é variável em alcance e gravidade e frequentemente muda com a aquisição de outras habilidades de desenvolvimento")
        st.write("O objetivo deste sistema é devolver um resultado utilizando técnicas de inteligência artificial para detecção de traços autisticos com o intuito de obter um diagnóstico cedo e preciso para melhor tratamento.")
        st.write("Faça o login no menu lateral para iniciar")


    elif choice == "Login":
        username = st.sidebar.text_input("Usuário")
        password = st.sidebar.text_input("Senha", type='password')
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = generate_hashes(str(password))
            result = login_user(username,verify_hashes(str(password), hashed_pswd))

            if result:
                st.success("Bem Vindo {}".format(username))
            
                activity = st.selectbox("Formulário", submenu)
                
                if activity == "Crianças Pequenas":
                    st.subheader("Ánalise e Classificação para crianças a partir dos 18 meses")
                    st.write("Checklist for Autism in Toddlers (CHAT)")
                    st.write("As perguntas são quantificadas da seguinte maneira: As perguntas de 1 a 9, caso a resposta esteja nas colunas C, D ou E, 1 ponto é contado. Para a pergunta 10, caso a resposta esteja nas colunas A, B ou C, 1 ponto é contato. Ao somar os pontos e ver que a criança obteve mais do que 3 das 10 perguntas, deve se considerar levá-la para uma avaliação multidisciplinar com um profissional da saúde.")
                   
                    
                    a1 = st.radio("1. A sua criança olha para si quando chama o nome dela?", tuple(answer_dict_frequencia.keys()))
                    a2 = st.radio("2. Quão fácil para si é conseguir contato ocular com sua criança?",tuple(answer_dict_facilidade.keys()))
                    a3 = st.radio("3. A sua criança aponta para indicar alguma coisa? (Ex. um brinquedo que está fora do alcance)", tuple(answer_dict_semana.keys()))
                    a4 = st.radio("4. A sua criança aponta para compartilhar um interesse consigo? (Ex. aponta para algum lugar interessante)", tuple(answer_dict_semana.keys()))
                    a5 = st.radio("5. A sua criança brinca de 'faz de conta?'", tuple(answer_dict_semana.keys()))
                    a6 = st.radio("6. A sua criança segue seu olhar?", tuple(answer_dict_semana.keys()))
                    a7 = st.radio("7. Se você ou alguém da sua família estiver visivelmente aborrecido, sua criança mostra sinais de querer confortá-lo?", tuple(answer_dict_frequencia.keys()))
                    a8 = st.radio("8. Descreveria as primeiras palavras da sua criança como:", tuple(answer_dict_fala.keys()))
                    a9 = st.radio("9. A sua criança usa gestos simples? (Ex. dar tchau com a mão)", tuple(answer_dict_semana.keys()))
                    a10 = st.radio("10. A sua criança olha fixamente para o nada sem nenhuma razão?", tuple(answer_dict_semana_10.keys()))
                    age_mons = st.number_input("Idade em meses",18,40)
                    sex = st.radio("Sexo", tuple(sex_dict.keys()))
                    jaundice = st.radio("Já notou algum aspecto de icterícia? (Condição que deixa os olhos amarelaados)", tuple(feature_dict.keys()))
                    st.image("jaundice.jpeg", width=100)
                    family_mem_with_asd = st.radio("Algum mebro da família já apresentou o Transtorno de Espectro Autista?", tuple(feature_dict.keys()))
                    who_completed_the_test = st.text_input("Quem está respondendo o teste?")

                
   
                
                elif activity == "Crianças":
                    st.subheader("Ánalise e Classificação para crianças a partir ")
                    st.write("Vale lembrar que esse questionário deve ser respondido pelos pais com base na observação do desenvolvimento da criança.")
                    st.write("AQ -10 (AUTISM SPECTRUM QUOTIENT)") 
                    st.write("O cálculo é realizado da seguinte maneira: 1 ponto é contado por cada resposta “Concordo totalmente” ou “Concordo levemente” em cada um dos seguintes itens: 1, 5, 8 e 10. Conte 1 ponto por cada resposta “Discordo totalmente” ou “Discordo levemente” em cada um dos seguintes itens: 2, 3, 4, 6, 7 e 9. Se o resultado total corresponder a uma pontuação superior a 6 pontos, deve ser ponderado um encaminhamento para uma avaliação diagnóstica especializada.")

                    a1_score = st.radio("1. Ele(a) nota muitas vezes pequenos ruídos que passam despercebidos às outras pessoas.", tuple(answer_dict_AQ10_pt1.keys()))
                    a2_score = st.radio("2. Habitualmente, ele(a) concentra-se mais na imagem ou situação no seu todo, do que nos seus pequenos detalhes.",tuple(answer_dict_AQ10_pt2.keys()))
                    a3_score = st.radio("3. Quando está num grupo social, ele(a) consegue facilmente seguir conversas de várias pessoas.", tuple(answer_dict_AQ10_pt2.keys()))
                    a4_score = st.radio("4. Ele(a) consegue facilmente fazer mais do que uma coisa ao mesmo tempo.", tuple(answer_dict_AQ10_pt2.keys()))
                    a5_score = st.radio("5. Frequentemente, ele(a) nota que não sabe como manter uma conversa.", tuple(answer_dict_AQ10_pt1.keys()))
                    a6_score = st.radio("6. Socialmente, ele(a) é bom/boa conversador(a).", tuple(answer_dict_AQ10_pt2.keys()))
                    a7_score = st.radio("7. Durante a leitura de uma história, ele(a) tem dificuldades em perceber as intenções e as emoções das personagens.", tuple(answer_dict_AQ10_pt2.keys()))
                    a8_score = st.radio("8. Na pré-escola, ele(a) gostava de brincar a jogos de faz-de-conta com as outras crianças.", tuple(answer_dict_AQ10_pt1.keys()))
                    a9_score= st.radio("9. Ele(a) percebe facilmente o que alguém está pensando ou a sentindo, apenas olhando para a sua cara.", tuple(answer_dict_AQ10_pt2.keys()))
                    a10_score = st.radio("10. Ele(a) tem dificuldades em fazer novos amigos.", tuple(answer_dict_AQ10_pt1.keys()))
                    age = st.number_input("Idade",4,11)
                    gender = st.radio("Sexo", tuple(sex_dict.keys()))
                    jundice = st.radio("Já notou algum aspecto de icterícia? (Condição que deixa os olhos amarelaados)", tuple(feature_dict.keys()))
                    st.image("jaundice.jpeg", width=100)
                    austim = st.radio("Algum mebro da família já apresentou o Transtorno de Espectro Autista?", tuple(feature_dict.keys()))
                    who_completed_the_test = st.text_input("Quem está respondendo o teste?")

    
                elif activity == "Adolescentes":
                    st.subheader("Ánalise e Classificação para adolescentes de 11 a 15 anos")
                    st.write("Vale lembrar que esse questionário deve ser respondido pelos pais com base no observado durante o dia-a-dia")
                    st.write("AQ -10 (AUTISM SPECTRUM QUOTIENT)") 
                    st.write("O cálculo é realizado da seguinte maneira: 1 ponto é contado por cada resposta “Concordo totalmente” ou “Concordo levemente” em cada um dos seguintes itens: 1, 5, 8 e 10. Conte 1 ponto por cada resposta “Discordo totalmente” ou “Discordo levemente” em cada um dos seguintes itens: 2, 3, 4, 6, 7 e 9. Se o resultado total corresponder a uma pontuação superior a 6 pontos, deve ser ponderado um encaminhamento para uma avaliação diagnóstica especializada.")


                    a1_score = st.radio("1. Ele(a) repara sempre em padrões/categorias nas coisas.", tuple(answer_dict_AQ10_pt1.keys()))
                    a2_score = st.radio("2. Habitualmente, ele(a) concentra-se mais na imagem ou situação no seu todo, do que nos seus pequenos detalhes.",tuple(answer_dict_AQ10_pt2.keys()))
                    a3_score = st.radio("3. Quando está num grupo social, ele(a) consegue facilmente seguir conversas de várias pessoas.", tuple(answer_dict_AQ10_pt2.keys()))
                    a4_score = st.radio("4. Em caso de interrupção, ele(a) consegue muito rapidamente voltar ao que estava a fazer.", tuple(answer_dict_AQ10_pt2.keys()))
                    a5_score = st.radio("5. Frequentemente, ele(a) nota que não sabe como manter uma conversa.", tuple(answer_dict_AQ10_pt1.keys()))
                    a6_score = st.radio("6. Socialmente, ele(a) é bom/boa conversador(a).", tuple(answer_dict_AQ10_pt2.keys()))
                    a7_score = st.radio("7. Quando era mais novo(a), ele(a) gostava de brincar a jogos de faz-de-conta com as outras crianças.", tuple(answer_dict_AQ10_pt2.keys()))
                    a8_score = st.radio("8. Ele(a) tem dificuldades em imaginar como seria ser outra pessoa.", tuple(answer_dict_AQ10_pt1.keys()))
                    a9_score= st.radio("9. Ele(a) acha as situações sociais fáceis.", tuple(answer_dict_AQ10_pt2.keys()))
                    a10_score = st.radio("10. Ele(a) tem dificuldades em fazer novos amigos.", tuple(answer_dict_AQ10_pt1.keys()))
                    age = st.number_input("Idade",12,15)
                    gender = st.radio("Sexo", tuple(sex_dict.keys()))
                    jundice = st.radio("Já notou algum aspecto de icterícia? (Condição que deixa os olhos amarelaados)", tuple(feature_dict.keys()))
                    st.image("jaundice.jpeg", width=100)
                    austim = st.radio("Algum mebro da família já apresentou o Transtorno de Espectro Autista?", tuple(feature_dict.keys()))
                    who_completed_the_test = st.text_input("Quem está respondendo o teste?")
 



                    
                elif activity == "Adultos":
                    st.subheader("Ánalise e Classificação para adultos a partir dos 16 anos")
                    st.write("Quando o questionário é respondido pelo próprio indivíduo, é importante ser preciso na resposta e não deixar coagir por fatores sociais, como pressão ou medo.")
                    st.write("AQ -10 (AUTISM SPECTRUM QUOTIENT)") 
                    st.write("O cálculo é realizado da seguinte maneira: 1 ponto é contado por cada resposta “Concordo totalmente” ou “Concordo levemente” em cada um dos seguintes itens: 1, 5, 8 e 10. Conte 1 ponto por cada resposta “Discordo totalmente” ou “Discordo levemente” em cada um dos seguintes itens: 2, 3, 4, 6, 7 e 9. Se o resultado total corresponder a uma pontuação superior a 6 pontos, deve ser ponderado um encaminhamento para uma avaliação diagnóstica especializada.")

                    a1_score = st.radio("1. Eu costumo notar pequenos sons quando outros não conseguem notar.", tuple(answer_dict_AQ10_pt1.keys()))
                    a2_score = st.radio("2. Eu costumo me concentrar mais em todo o cenário do que em pequenos detalhes.",tuple(answer_dict_AQ10_pt2.keys()))
                    a3_score = st.radio("3. Eu acho fácil fazer mais de uma coisa ao mesmo tempo.", tuple(answer_dict_AQ10_pt2.keys()))
                    a4_score = st.radio("4. Se houver uma interrupção enquanto estou fazendo algo, posso voltar para o que eu estava fazendo muito rapidamente.", tuple(answer_dict_AQ10_pt2.keys()))
                    a5_score = st.radio("5. Eu acho fácil 'ler nas entrelinhas' quando alguém está falando comigo.", tuple(answer_dict_AQ10_pt1.keys()))
                    a6_score = st.radio("6. Eu sei como saber se alguém me ouvindo está ficando entediado.", tuple(answer_dict_AQ10_pt2.keys()))
                    a7_score = st.radio("7. Quando estou lendo uma história, acho difícil descobrir as intenções dos personagens.", tuple(answer_dict_AQ10_pt2.keys()))
                    a8_score = st.radio("8. Eu gosto de coletar informações sobre categorias de coisas (Ex. tipos de carro, tipos de plantas etc.).", tuple(answer_dict_AQ10_pt1.keys()))
                    a9_score= st.radio("9. Eu acho fácil descobrir o que alguém está pensando ou sentindo apenas olhando para o rosto deles.", tuple(answer_dict_AQ10_pt2.keys()))
                    a10_score = st.radio("10. Eu acho difícil descobrir as intenções das pessoas.", tuple(answer_dict_AQ10_pt1.keys()))
                    age = st.number_input("Idade",16,50)
                    gender = st.radio("Sexo", tuple(sex_dict.keys()))
                    jundice = st.radio("Já notou algum aspecto de icterícia? (Condição que deixa os olhos amarelaados)", tuple(feature_dict.keys()))
                    st.image("jaundice.jpeg", width=100)
                    austim = st.radio("Algum mebro da família já apresentou o Transtorno de Espectro Autista?", tuple(feature_dict.keys()))
                    who_completed_the_test = st.text_input("Quem está respondendo o teste?")





            #ML
                model_choice = st.selectbox("Modelo", ["LR"])
                if st.button("Analisar"):
                    if model_choice == "LR":
                            if activity == "Crianças Pequenas":
                                loaded_model = load_model("models/Toddlers_Prediction_LR_Model.joblib")
                                prediction = loaded_model.predict(single_sample)
                                pred_prob=loaded_model.predict_proba(single_sample)
                                st.write(prediction)
                            elif activity == "Crianças":
                                loaded_model = load_model("models/Children_Prediction_LR_Model.joblib")
                                prediction = loaded_model.predict(single_sample)
                                pred_prob=loaded_model.predict_proba(single_sample)
                                st.write(prediction)
                            elif activity == "Adolescentes":
                                loaded_model = load_model("models/Adolescent_Prediction_LR_Model.joblib")
                                prediction = loaded_model.predict(single_sample)
                                pred_prob=loaded_model.predict_proba(single_sample)
                                st.write(prediction)
                            elif activity == "Adultos":
                                loaded_model = load_model("models/Adult_Prediction_LR_Model.joblib")
                                prediction = loaded_model.predict(single_sample)
                                pred_prob=loaded_model.predict_proba(single_sample)
                                st.write(prediction)

                
                    if prediction == 1:
                        st.warning("O paciente pode apresentar Transtorno de Espectro Autista, aconselhamos buscar ajuda de profissional especializado")
                        pred_probability_score = {"Chances de Apresentar":pred_prob[0][1]*100,"Chances de não apresentar":pred_prob[0][0]*100}
                        st.json(pred_probability_score)
                        
                    else:
                        st.success("O paciente poussui pouca ou quase nenhuma chance de apresentar Transtorno de Espectro Autista")
                        pred_probability_score = {"Chances de Apresentar":pred_prob[0][1]*100,"Chances de Não Apresentar":pred_prob[0][0]*100}
                        st.subheader("Probabilidade usando {}".format(model_choice))
                        st.json(pred_probability_score)
             
            else:
                st.warning("O usuário/senha está incorreto")

    elif choice == "SignUp":
        new_username = st.text_input("Usuário")
        new_password = st.text_input("Senha", type='password')

        confirm_password = st.text_input("Confirmação da senha", type='password')
        if new_password == confirm_password:
            st.success("As senhas conferem")
        else:
            st.warning("Verifique sua senha e confirmação")

        if st.button("Confirmar"):
            create_usertable()
            hashed_new_password = generate_hashes(str(new_password))
            add_userdata(new_username,hashed_new_password)
            st.success("Seu cadastro foi concluído com sucesso")
            st.info("Entre na sua conta para começar a explorar")



if __name__ == '__main__':
    main()