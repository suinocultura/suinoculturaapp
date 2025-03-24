import streamlit as st
import base64
import os
import sys

# Adicionar diretório raiz ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import check_developer_access, check_permission

# Configuração da página
st.set_page_config(
    page_title="Download do Aplicativo",
    page_icon="📥",
    layout="centered"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Verificar se o usuário está autenticado
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("Você precisa estar autenticado para acessar esta página.")
    st.stop()

# Verificar se o usuário tem permissão para acessar esta página
if not check_permission(st.session_state.current_user, 'developer_tools'):
    st.error("Você não tem permissão para acessar esta página.")
    st.stop()


# Verificar se o usuário está autenticado e tem permissão para baixar o aplicativo
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("Você precisa estar autenticado para acessar esta página.")
    st.stop()

if "current_user" not in st.session_state or not check_permission(st.session_state.current_user, 'developer_tools'):
    st.error("Você não tem permissão para acessar esta página. Apenas desenvolvedores têm acesso.")
    st.stop()

# Estilo CSS personalizado
st.markdown("""
<style>
    .download-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .header-style {
        color: #4527A0;
        text-align: center;
    }
    .subheader-style {
        color: #5E35B1;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="header-style">Download - Sistema de Gestão Suinocultura</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subheader-style">Faça o download do aplicativo completo para uso offline ou criação de APK</h3>', unsafe_allow_html=True)

st.markdown("---")

with st.container():
    st.markdown('<div class="download-container">', unsafe_allow_html=True)
    
    st.markdown("""
    ### Conteúdo do Pacote
    Este arquivo ZIP contém o código-fonte completo do Sistema de Gestão Suinocultura, incluindo:
    - Todos os arquivos Python
    - Todas as páginas da aplicação
    - Arquivos de dados (CSVs)
    - Arquivos de configuração
    - Guia para criação do APK
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Função para gerar o link de download
def get_download_link(file_path, link_text):
    if not os.path.exists(file_path):
        st.error(f"Arquivo {file_path} não encontrado!")
        return ""
    
    with open(file_path, "rb") as f:
        data = f.read()
    
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/zip;base64,{b64}" download="{os.path.basename(file_path)}" style="text-decoration:none;">'\
           f'<div style="background-color:#4CAF50; color:white; padding:12px 20px; border-radius:8px; '\
           f'cursor:pointer; text-align:center; font-weight:bold; margin:20px 0px;">{link_text}</div></a>'
    
    return href

# Sempre criar um novo arquivo ZIP com a data atual
import datetime
current_date = datetime.datetime.now().strftime("%Y%m%d")
zip_path = f"suinocultura_{current_date}.zip"

# Forçar a criação de um novo arquivo para garantir que esteja atualizado
st.info("Preparando o arquivo para download... Por favor, aguarde.")
import sys
import importlib.util

# Carregar e executar o script create_download_package.py
spec = importlib.util.spec_from_file_location("create_download_package", "create_download_package.py")
module = importlib.util.module_from_spec(spec)
sys.modules["create_download_package"] = module
spec.loader.exec_module(module)

# Executar a função
module.create_download_package()

# Verificar se o arquivo foi criado
if not os.path.exists(zip_path):
    st.error("Não foi possível criar o arquivo para download. Por favor, tente novamente mais tarde.")

# Mostrar o botão de download
if os.path.exists(zip_path):
    st.markdown(get_download_link(zip_path, "CLIQUE AQUI PARA BAIXAR O PACOTE COMPLETO"), unsafe_allow_html=True)
    
    file_size = round(os.path.getsize(zip_path) / (1024), 2)
    st.caption(f"Tamanho do arquivo: {file_size} KB")

# Instruções adicionais
with st.expander("Instruções para usar o arquivo baixado", expanded=True):
    st.markdown("""
    ### Como usar o arquivo baixado:
    
    1. Descompacte o arquivo ZIP em seu computador
    2. Certifique-se de ter o Python e as bibliotecas necessárias instaladas:
       ```
       pip install streamlit pandas numpy matplotlib plotly
       ```
    3. Execute a aplicação com o comando:
       ```
       streamlit run app.py
       ```
    
    ### Para criar um APK Android:
    Siga as instruções detalhadas no arquivo `guia_criacao_apk.md` incluído no pacote.
    
    A pasta `android_app_base` contém os arquivos base necessários para criar o aplicativo Android usando Android Studio. 
    Esta implementação usa WebView para carregar a versão hospedada do Sistema Suinocultura.
    """)

with st.expander("Problemas ao baixar?"):
    st.markdown("""
    Se você estiver enfrentando problemas para baixar o arquivo, tente estas alternativas:
    
    1. Use um navegador diferente (Chrome, Firefox, Edge)
    2. Desabilite temporariamente bloqueadores de pop-up ou extensões
    3. Entre em contato com o desenvolvedor para receber o arquivo por e-mail
    """)

# Rodapé
st.markdown("---")
st.caption("Sistema de Gestão Suinocultura © 2025 - Todos os direitos reservados")