import pandas            as pd
import streamlit         as st
import seaborn           as sns
import matplotlib.pyplot as plt
from PIL                 import Image

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

def multiselect_filter(relatorio, col, selecionados):
    if 'Todos' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

def main():
    st.set_page_config(page_title = 'Telemarketing analisys', \
        page_icon = r'C:\Users\sann_\Documentos\curso\Projetos_CD\Git\Projeto-Telemarkerting\telmarketing_icon.png',
        layout="wide",
        initial_sidebar_state='expanded'
    )
    st.write('# Telemarketing analisys')
    st.markdown("---")
    st.markdown('## Entendendo os dados de telemarketing')
    st.markdown(" Os dados estão relacionados a campanhas de telemarketing ativo de uma instituição bancária portuguesa. Frequentemente, mais de um contato com o mesmo cliente foi necessário, a fim de verificar se o produto (depósito a prazo bancário/investimento de baixo risco) seria ou não contratado (sim ou não). ")
    st.markdown("###### Nosso objetivo com este estudo é gerar insights a partir da visualização dos dados.")
    st.markdown('É buscar entender qual o comportamento dos clientes que contrataram o serviço ofertado, após aplicação de filtros e comparar com o restante dos clientes do banco de dados.')
    st.markdown("---")
    
    
    
    
    st.sidebar.image('https://img.freepik.com/vetores-gratis/central-de-atendimento_24877-49049.jpg')

    bank_raw = pd.read_csv(r"https://raw.githubusercontent.com/sannlin9/Projeto-Telemarkerting/main/bank-additional-full.csv", sep=';')
    bank = bank_raw.copy()

    #st.write('## Antes dos filtros')
    #st.write(bank_raw.head())

    with st.sidebar.form(key='my_form'):
        
        # SELECIONA O TIPO DE GRÁFICO
        graph_type = st.radio('Tipo de gráfico:', ('Barras', 'Pizza'))
        
        # IDADES
        max_age = int(bank.age.max())
        min_age = int(bank.age.min())
        idades = st.slider(label='Idade', 
                                        min_value = min_age,
                                        max_value = max_age, 
                                        value = (min_age, max_age),
                                        step = 1)
    
        # PROFISSÕES
        jobs_list = bank.job.unique().tolist()
        jobs_list.append('Todos')
        jobs_selected =  st.multiselect("Profissão", jobs_list, ['Todos'])

        # ESTADO CIVIL
        marital_list = bank.marital.unique().tolist()
        marital_list.append('Todos')
        marital_selected =  st.multiselect("Estado civil", marital_list, ['Todos'])

        # DEFAULT?
        default_list = bank.default.unique().tolist()
        default_list.append('Todos')
        default_selected =  st.multiselect("Tem parcelas de emprestimo em atraso?", default_list, ['Todos'])

        
        # TEM FINANCIAMENTO IMOBILIÁRIO?
        housing_list = bank.housing.unique().tolist()
        housing_list.append('Todos')
        housing_selected =  st.multiselect("Tem financiamento imobilhario?", housing_list, ['Todos'])

        
        # TEM EMPRÉSTIMO?
        loan_list = bank.loan.unique().tolist()
        loan_list.append('Todos')
        loan_selected =  st.multiselect("Tem empréstimo?", loan_list, ['Todos'])

        
        # MEIO DE CONTATO?
        contact_list = bank.contact.unique().tolist()
        contact_list.append('Todos')
        contact_selected =  st.multiselect("Meio de contato", contact_list, ['Todos'])

        
        # MÊS DO CONTATO
        month_list = bank.month.unique().tolist()
        month_list.append('Todos')
        month_selected =  st.multiselect("Mês do contato", month_list, ['Todos'])

        
        # DIA DA SEMANA
        day_of_week_list = bank.day_of_week.unique().tolist()
        day_of_week_list.append('Todos')
        day_of_week_selected =  st.multiselect("Dia da semana do contato", day_of_week_list, ['Todos'])


        bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
                    .pipe(multiselect_filter, 'job', jobs_selected)
                    .pipe(multiselect_filter, 'marital', marital_selected)
                    .pipe(multiselect_filter, 'default', default_selected)
                    .pipe(multiselect_filter, 'housing', housing_selected)
                    .pipe(multiselect_filter, 'loan', loan_selected)
                    .pipe(multiselect_filter, 'contact', contact_selected)
                    .pipe(multiselect_filter, 'month', month_selected)
                    .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
        )
        submit_button = st.form_submit_button(label='Aplicar')
    
    st.write('## Após os filtros')
    st.write(bank.head())
    st.markdown("---")

    # PLOTS    
    # PLOTS    
    fig, ax = plt.subplots(1, 2, figsize = (5,3))

    bank_raw_target_perc = bank_raw.y.value_counts(normalize = True).to_frame()*100
    bank_raw_target_perc = bank_raw_target_perc.sort_index()
        
    try:
            bank_target_perc = bank.y.value_counts(normalize = True).to_frame()*100
            bank_target_perc = bank_target_perc.sort_index()
    except:
            st.error('Erro no filtro')
               
    st.write('## Proporção de aceite')
    
    if graph_type == 'Barras':
            sns.barplot(x = bank_raw_target_perc.index, 
                        y = 'y',
                        data = bank_raw_target_perc, 
                        ax = ax[0])
            ax[0].bar_label(ax[0].containers[0])
            ax[0].set_title('Dados brutos',
                            fontweight ="bold")
            
            sns.barplot(x = bank_target_perc.index, 
                        y = 'y', 
                        data = bank_target_perc, 
                        ax = ax[1])
            ax[1].bar_label(ax[1].containers[0])
            ax[1].set_title('Dados filtrados',
                            fontweight ="bold")
    else:
            bank_raw_target_perc.plot(kind='pie', autopct='%.2f', y='y', ax = ax[0])
            ax[0].set_title('Dados brutos',
                            fontweight ="bold")
            
            bank_target_perc.plot(kind='pie', autopct='%.2f', y='y', ax = ax[1])
            ax[1].set_title('Dados filtrados',
                            fontweight ="bold")

    st.pyplot(plt)


if __name__ == '__main__':
	main()