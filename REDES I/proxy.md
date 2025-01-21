Aqui está a mesclagem e organização dos dois tutoriais:

### 1. **Controle de Acesso com o Squid Proxy**

O Squid Proxy permite realizar uma série de bloqueios e permissões com base em regras específicas, como acesso a sites, IPs ou horários.

#### **Exemplo de Configurações de Controle de Acesso:**

- **Proibir usuários de acessar páginas que contenham uma palavra específica:**
    ```bash
    acl palavra_proibida url_regex PALAVRA
    http_access deny palavra_proibida
    ```

- **Bloquear uma faixa de IP para não baixar arquivos `.zip`:**
    ```bash
    acl arquivos_zip url_regex zip
    acl proibido_acesso src 192.168.0.0/24
    http_access deny proibido_acesso arquivos_zip
    ```

- **Bloquear um site para todos os usuários da rede:**
    ```bash
    acl site_proibido dstdomain .facebook.com
    http_access deny all site_proibido
    ```

- **Controlar o acesso por hora (exemplo: durante horário de aula):**
    ```bash
    acl fechado_para_aula time MTWHF 08:05-11:40
    acl hora_de_aula src 192.168.0.0/24
    http_access deny hora_de_aula fechado_para_aula
    ```

- **Liberando o acesso apenas em um determinado horário:**
    ```bash
    acl usuarios src 192.168.0.0/24
    acl libera_geral time MTWHF 11:40-13:05
    http_access allow usuarios libera_geral
    http_access deny usuarios
    ```

- **Usando um arquivo de texto para incluir diversos parâmetros de bloqueio:**
    ```bash
    acl usuarios src 192.168.0.0/24
    acl sites_proibidos url_regex "arquivo_sites.txt"
    http_access deny usuarios sites_proibidos
    ```

- **Permitir apenas redes expressamente liberadas e negar todas as outras:**
    ```bash
    acl MINHA_REDE src 192.168.0.0/23
    http_access allow MINHA_REDE
    http_access deny all
    ```

### 2. **Configuração do Squid Proxy para Acesso Restrito**

#### **Passo a Passo para Configuração do Squid:**

- **Atualize e instale o Squid:**
    ```bash
    sudo apt update
    sudo apt install squid
    ```

- **Crie um backup do arquivo de configuração:**
    ```bash
    cd /etc/squid
    sudo cp squid.conf squid.conf.original
    ```

- **Edite o arquivo de configuração:**
    ```bash
    sudo nano squid.conf
    ```

- **Faça as alterações necessárias no arquivo `squid.conf`:**

    - Defina as ACLs para permitir acesso a redes específicas:
      ```bash
      acl aula src 172.16.100.0/24
      acl redes src 200.50.100.0/24
      ```

    - Após a linha `http_access deny all`, adicione as ACLs:
      ```bash
      http_access allow aula
      http_access allow redes
      ```

#### **Reinicie o Squid para aplicar as alterações:**
```bash
sudo systemctl restart squid
```

#### **Configuração do Navegador Firefox:**

- Vá em **Configurações** > **Redes** > **Configurar Rede**.
- Marque a opção **Utilizar configuração manual de proxy** e defina:
    - **Endereço IP do Proxy**: 200.50.100.2
    - **Porta**: 3328
    - Marque **"Utilizar também em servidores https"**.

---

### **Observações:**

- **Princípio de permissão implícita:** Tudo o que não for explicitamente proibido será permitido.
  
Isso resume e organiza os dois tutoriais, criando um fluxo claro para o bloqueio e liberação de acessos via Squid Proxy, além de configurar o Firefox para usar o proxy.
