## Pré-requisitos e Observações Gerais
- **Adaptador Host-Only**: Configure a placa de rede VirtualBox `Host-Only Ethernet Adapter` com o IP `192.168.56.1/24` e **ative o servidor DHCP**.
- **Acesso SSH**: Para acessar as máquinas enquanto o firewall está ativo, utilize os seguintes comandos:
  - **Gateway**: `ssh -p 51000 aluno@192.168.56.2`
  - **DNS1**: `ssh -p 52000 aluno@192.168.56.2`
  - **DNS2**: `ssh -p 53000 aluno@192.168.56.2`
  - **Web**: `ssh -p 54000 aluno@192.168.56.2`

---
### **Prova de Redes I**

#### **Observação**
Caso haja erros ao iniciar uma VM utilizando o modo Host-Only, apague a configuração antiga e crie uma nova.

---

### **Configurações do VirtualBox**
1. **Configuração do Host-Only Ethernet Adapter:**
   - IP fixo: `192.168.56.1/24`
   - Desative o DHCP.

2. **Criar as 5 VMs:**
   - Criar o Gateway (Debian CLI).
   - Configurar a primeira placa de rede como primária, com DHCP ativo.
   - Defina o domínio como `prova.lan` (ou conforme o professor informar).

3. **Configuração de Rede:**
   - **Adaptador 1:** Modo NAT.
   - **Adaptador 2:** Modo Host-Only, nome: `VirtualBox Host-Only Ethernet Adapter`.
   - **Adaptador 3:** Modo Rede Interna, nome: `SRC1`.

4. **Configuração de IP em `/etc/network/interfaces`:**
   
   `su root`
   
   ```bash
   allow-hotplug enp0s8
   iface enp0s8 inet static
   address 192.168.100.1/24

   allow-hotplug enp0s9
   iface enp0s9 inet static
   address 192.168.56.2/24
   ```

   - Organize os repositorios:
     ```bash
     nano /etc/apt/sources.list
     ```
  
     ```bash
     deb http://security.debian.org/debian-security bullseye-security main contrib non-free
     deb-src http://security.debian.org/debian-security bullseye-security main contrib non-free

     deb http://deb.debian.org/debian bullseye main contrib non-free
     deb-src http://deb.debian.org/debian bullseye main contrib non-free

     deb http://deb.debian.org/debian bullseye-updates main contrib non-free
     deb-src http://deb.debian.org/debian bullseye-updates main contrib non-free

     deb http://deb.debian.org/debian bullseye-backports main contrib non-free
     deb-src http://deb.debian.org/debian bullseye-backports main contrib non-free
     ```
     
6. **Instalar `sudo`:**
   - `apt update && apt install sudo`
   - Edite o grupo com: `nano /etc/group`
   - Clique em: `Alt + shift + 3`
   - Altere a linha 21 para: `sudo:x:27:aluno`
   - Salve e saia.

7. **Desligar a máquina:**
   ```bash
   /sbin/shutdown -h now
   ```

8. **Ligar a máquina em modo headless e acessar via SSH:**
   - Acesse via SSH: `ssh aluno@192.168.56.2`.

---

### **Configuração do Firewall e Acesso via SSH**
1. **Atualize o sistema:**
   ```bash
   sudo apt update
   ```

2. **Configuração do DNS:**
   - Edite o arquivo `/etc/dhcp/dhclient.conf` e adicione:
   ```bash
   supersede domain-name-servers 192.168.100.2, 192.168.100.3, 8.8.8.8;
   ```

3. **Criação do Script de Firewall:**
   - Crie o diretório `~/firewall` e entre nele.
   ```bash
     mkdir ~/firewall && cd ~/firewall
     nano firewall
     ```
   - Adicione o conteúdo do script `firewall`:

     ```bash
     #!/bin/bash
     ### BEGIN INIT INFO
     # Provides:		firewall
     # Required-Start:	$syslog
     # Required-Stop:	$syslog
     # Default-Start:	2 3 4 5
     # Default-Stop:
     # Short-Description:	Firewall da Dexter
     ### END INIT INFO

     # Script de Firewall
     # Vagner Schoaba
     clear
     ### CORES
     VERDE="\033[1;32m"
     AMARELO="\033[1;33m"
     AZUL="\033[1;34m"
     VERMELHO="\033[1;31m"
     END="\033[m"
     ###
     ProgressBar() {
       tput civis
       for X in $(seq 20)
       do
         for i in ..
         do
           echo -en "\033[1D$i"
           #sleep .1
         done
       done
       tput cnorm
     }


     case $1 in
     stop)


     	# Definindo Politica ACCEPT - ACEITA TUDO
     	iptables -P OUTPUT ACCEPT
     	iptables -P INPUT ACCEPT
     	iptables -P FORWARD ACCEPT

     	# Limpar as Regras de todas as tableas
     	iptables -F
     	iptables -t nat -F
     	iptables -t mangle -F

     	iptables -t raw -F
     	iptables -t security -F

     	# Bloquear a passagem de pacotes pelo kernel
     	echo 0 > /proc/sys/net/ipv4/ip_forward
     	echo -en "Stopping Security Firewall Schoaba ";ProgressBar; echo -e " [\033[0;32m ok\033[m ]"

     ;;


     start)
     	$0 stop
     	sleep 0.5
     	echo -en "Starting Security Firewall Schoaba ";ProgressBar; echo -e " [\033[0;32m ok\033[m ]"
     	# liberar a passagem de pacotes pelo kernel
     	echo 1 > /proc/sys/net/ipv4/ip_forward

     	# Iniciando as Regras
     	bash /home/aluno/firewall/regras

     ;;


     restart)
     	$0 start
     ;;




     *)
     	echo 'POR FAVOR USE "stop|start|restart"'

     ;;

     esac
     ```

   - Crie o arquivo de regras:
     ```bash
     nano regras
     ```
   - Adicione as regras de firewall:

     ```bash
     #!/bin/bash
     #INICIALIZACAO AUTOMATICA
     #ln -s /home/aluno/firewall.sh /etc/init.d
     #update-rc.d firewall defaults 3

     iptables -t nat -F
     iptables -F

     SSH=192.168.56.2
     SSH2=192.168.56.3
     GATEWAY=192.168.100.1
     DNS1=192.168.100.2
     DNS2=192.168.100.3
     WEB=192.168.100.4
     ARQUIVO=192.168.100.5
     AUTENTICACAO=192.168.100.6
     SAMBA=192.168.100.7
     EMAIL=192.168.100.8
     ALL=0/0

     LAN=192.168.100.0/24
     LOCAL=192.168.56.0/24

     echo "1" >/proc/sys/net/ipv4/ip_forward

     iptables -t nat -A POSTROUTING -s $LAN -j MASQUERADE

     ###### 1.0 - Gateway
     iptables -A FORWARD -p tcp -s $LOCAL -d $GATEWAY --dport 51000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $GATEWAY -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 51000 -j DNAT --to $GATEWAY:22

     ###### 2.0 - DNS1
     iptables -A FORWARD -p tcp -s $LOCAL -d $DNS1 --dport 52000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $DNS1 -d $LOCAL --sport 22 -j ACCEPT

     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 52000 -j DNAT --to $DNS1:22


     ###### 2.1 - DNS1
     iptables -A FORWARD -p udp -s $DNS1 -d $LOCAL --sport 53 -j ACCEPT
     iptables -A FORWARD -p udp -s $LOCAL -d $DNS1 --dport 53 -j ACCEPT
     iptables -t nat -A PREROUTING -p udp -s $LOCAL -d $SSH --dport 53 -j DNAT --to $DNS1:53

     ###### 3.0 - DNS2
     iptables -A FORWARD -p tcp -s $LOCAL -d $DNS2 --dport 53000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $DNS2 -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 53000 -j DNAT --to $DNS2:22

     ###### 3.1 - DNS2
     iptables -A FORWARD -p udp -s $DNS2 -d $LOCAL --sport 53 -j ACCEPT
     iptables -A FORWARD -p udp -s $LOCAL -d $DNS2 --dport 53 -j ACCEPT
     iptables -t nat -A PREROUTING -p udp -s $LOCAL -d $SSH2 --dport 53 -j DNAT --to $DNS2:53

     ###### 3.2 - EMAIL SMTP

     iptables -A FORWARD -p tcp -s $LAN -m multiport --dports 25,110,143,587,993,995 -j ACCEPT

     iptables -A FORWARD -p tcp -s $SSH2 -d $EMAIL -m multiport --dports 25,110,143,587,993,995 -j ACCEPT


     ###### 4.0 - WEB
     iptables -A FORWARD -p tcp -s $LOCAL -d $WEB --dport 54000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $WEB -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 54000 -j DNAT --to $WEB:22

     ###### 5.0 - ARQUIVO
     iptables -A FORWARD -p tcp -s $LOCAL -d $ARQUIVO --dport 55000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $ARQUIVO -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 55000 -j DNAT --to $ARQUIVO:22


     ###### 6.0 - AUTENTICACAO
     iptables -A FORWARD -p tcp -s $LOCAL -d $AUTENTICACAO --dport 56000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $AUTENTICACAO -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 56000 -j DNAT --to $AUTENTICACAO:22
     iptables -A OUTPUT -p tcp -s $GATEWAY -d $AUTENTICACAO --dport 389 -j ACCEPT

     ###### 7.0 - SAMBA
     iptables -A FORWARD -p tcp -s $LOCAL -d $SAMBA --dport 57000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $SAMBA -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 57000 -j DNAT --to $SAMBA:22

     ###### 8.0 - EMAIL
     iptables -A FORWARD -p tcp -s $LOCAL -d $EMAIL --dport 58000 -j ACCEPT
     iptables -A FORWARD -p tcp -s $EMAIL -d $LOCAL --sport 22 -j ACCEPT
     iptables -t nat -A PREROUTING -p tcp -s $LOCAL -d $SSH --dport 58000 -j DNAT --to $EMAIL:22

     ###EMail
     for MAIL in 25 110 143 587 993 995
     do
       iptables -t nat -A PREROUTING -p tcp -s $ALL -d $SSH2 --dport $MAIL -j DNAT --to $EMAIL:$MAIL
     done



     ```
     - Torne os arquivos executáveis:
     ```bash
     chmod +x firewall regras
     ```
        
4. **Instale o `iptables`:**
   ```bash
   sudo apt install iptables -y
   ```

5. **Automatize a execução do firewall:**
   ```bash
   sudo ln -s /home/aluno/firewall/firewall /etc/init.d
   sudo update-rc.d firewall defaults 3
   ```

6. **Execute o firewall:**
   ```bash
   sudo ./firewall start
   ```

7. **Verifique as regras do `iptables`:**
   ```bash
   sudo iptables -nL
   ```

8. **Teste a automação:**
   - Verifique se o firewall inicia automaticamente após reiniciar a máquina.
   
9. **Criação do Snapshot.**

---

### **Configuração do DHCP**
1. **Acesse via SSH o DNS1:**
   ```bash
   ssh -p 52000 aluno@192.168.56.2
   ```

2. **Instalar e configurar o servidor DHCP:**
   ```bash
   sudo apt update && sudo apt install isc-dhcp-server -y
   ```

3. **Configurar o arquivo `/etc/default/isc-dhcp-server`:**
   ```bash
   INTERFACESv4="enp0s8"
   ```

4. **Configuração do arquivo `/etc/dhcp/dhcpd.conf`:**
   Adicione a configuração de rede:
   ```bash
   subnet 192.168.100.0 netmask 255.255.255.0 {
     range 192.168.100.50 192.168.100.70;
     option domain-name-servers 8.8.8.8, 192.168.100.2, 192.168.100.3;
     option domain-name "prova.lan";
     option routers 192.168.100.1;
     option broadcast-address 192.168.100.255;
     default-lease-time 600;
     max-lease-time 7200;
   }
   ```

---

### **Configuração do Ubuntu**
1. **Adaptador 1:** Rede Interna `intnet`.

  - Instale o ubuntu normalmente sem internet.

2. **Configuração de IP via DHCP:**
   - Edite o arquivo `/etc/systemd/resolved.conf`:
   ```bash
   [Resolve]
   DNS=192.168.100.2 192.168.100.3 8.8.8.8
   Domains=prova.lan
   ```

3. **Remova a configuração existente:**
   ```bash
   sudo rm /etc/resolv.conf
   ```

4. **Reinicie a máquina:**
   ```bash
   sudo reboot
   ```
**Desligue e ligue novamente a placa de rede**

5. **Teste a conexão com a internet.**

6. **Desligue a máquina e crie o Snapshot da máquina Gateway e Ubuntu.**

---

### **Configuração do DNS1 (Servidor DNS)**
1. **Ubuntu Server CLI:**
   - **Adaptador 1:** Rede Interna (mesma do gateway).
   - **Configuração de IP fixo:**
     Edite o arquivo `/etc/netplan/50-cloud-init.yaml`:
     ```yaml
     network:
       version: 2
       ethernets:
         enp0s3:
           dhcp4: false
           addresses:
             - 192.168.100.2/24
           nameservers:
             addresses:
               - 8.8.8.8
             search:
               - prova.lan
           routes:
             - to: default
               via: 192.168.100.1
     ```
   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

   - Teste acesso via ssh:
   ```bash
   ssh -p 52000 aluno@192.168.56.2
   ```

   **Se funcionar faça Snapshot da configuração de rede concluída**

2. **Instale e configure o BIND9 (DNS):**
   ```bash
   sudo apt update && sudo apt install bind9 -y
   ```

3. **Configure os arquivos do BIND9:**
   Edite `/etc/bind/named.conf.local` para adicionar as zonas:
   ```bash
   zone "prova.lan" {
           type master;
           file "/etc/bind/ifro/prova.db";
           allow-transfer { 192.168.100.3; };
   };

   zone "100.16.172.in-addr.arpa" {
           type master;
           file "/etc/bind/ifro/lab.rev";
           allow-transfer { 192.168.100.3; };
   };
   ```

4. **Criação e configuração das zonas e arquivos de DNS:**
   - Crie o diretório `ifro` e copie os arquivos necessários.
   ```bash
   cd /etc/bind
   ```
   ```bash
   sudo mkdir ifro
   ```
   ```bash
   sudo cp db.local ifro/prova.db
   ```
   ```bash
   sudo cp db.127 ifro/lab.rev
   ```
   - Edite os arquivos `prova.db` e `lab.rev` conforme as instruções fornecidas.

   ```bash
   cd ifro
   ```

   ```bash
   sudo nano prova.db
   ```

   ```bash
   ;
   ; BIND data file for local loopback interface
   ;
   $TTL    604800
   @       IN      SOA     prova.lan. root.prova.lan. (
                   1         ; Serial
                   604800    ; Refresh
                   86400     ; Retry
                   2419200   ; Expire
                   604800 )  ; Negative Cache TTL
   ;
   @       IN      NS      prova.lan.
   @       IN      A       192.168.100.2
   ns      IN      A       192.168.100.2
   web     IN      A       192.168.100.4
   www     IN      CNAME   web.prova.lan.
   dns1    IN      CNAME   ns.prova.lan.
   ```

   ```bash
   sudo nano lab.rev
   ```

   ```bash
   ;
   ; BIND reverse data file for local loopback interface
   ;
   $TTL    604800
   @       IN      SOA     prova.lan. root.prova.lan. (
                   1         ; Serial
                   604800    ; Refresh
                   86400     ; Retry
                   2419200   ; Expire
                   604800 )  ; Negative Cache TTL
   ;
   @       IN      NS      prova.lan.
   2       IN      PTR     prova.lan.
   4       IN      PTR     web.prova.lan.
   ```
  
5. **Verifique a configuração do BIND9:**
   ```bash
   sudo named-checkconf
   sudo named-checkzone prova.lan prova.db
   sudo named-checkzone 100.16.172.in-addr.arpa lab.rev
   ```

**Defina o DNS:**

```bash
sudo nano /etc/systemd/resolved.conf
```
```bash
[Resolve]
DNS=192.168.100.2 192.168.100.3 8.8.8.8
Domains=prova.lan
```
```bash
sudo rm /etc/resolv.conf
```

6. **Configurar o named.conf.options**
   ```bash
   sudo nano /etc/bind/named.conf.options
   ```
   ```bash
   options {
           directory "/var/cache/bind";
           forwarders {
                   8.8.8.8;
           };
           dnssec-validation auto;
           listen-on-v6 { any; };
   };
      ```

7. **Reinicie o serviço do BIND9:**
   ```bash
   sudo systemctl restart bind9
   sudo systemctl status bind9
   ```

8. **Teste o DNS com o comando `ping prova.lan`.**

**Salve o SNAPSHOT do DNS**

---

### **Configuração do DNS2**

1. **Criar Clone Linkado:**
   - Gere novos endereços MAC para todas as placas de rede.
   - Acesse a máquina via VirtualBox (não via SSH).
   
2. **Definir o Hostname:**
   ```bash
   sudo hostnamectl set-hostname dns2
   ```

**Definir o /etc/hosts:**
   ```bash
   sudo nano /etc/hosts
   ```
   ```bash
   127.0.0.1 localhost
   127.0.1.1 dns2
   192.168.100.3    dns2    dns2.prova.lan
   192.168.100.2    dns1    dns1.prova.lan
   192.168.100.1    gateway gateway.prova.lan

   # The following lines are desirable for IPv6 capable hosts
   ::1     ip6-localhost ip6-loopback
   fe00::0 ip6-localnet
   ff00::0 ip6-mcastprefix
   ff02::1 ip6-allnodes
   ff02::2 ip6-allrouters
   ```

3. **Configuração de IP Fixo:**
   - Edite o arquivo `/etc/netplan/50-cloud-init.yaml` com o seguinte conteúdo:
   ```yaml
   network:
     version: 2
     ethernets:
       enp0s3:
         dhcp4: false
         addresses:
           - 192.168.100.3/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - prova.lan
         routes:
           - to: default
             via: 192.168.100.1
   ```

   ```bash
   sudo rm /etc/resolv.conf
   ```

   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

**Configurar o Resolvedor Local**
1. Certifique-se de que o DNS2 também aponta para o DNS1. Edite o arquivo do resolvedor:
   ```bash
   sudo nano /etc/systemd/resolved.conf
   ```
2. Adicione ou edite as seguintes linhas:
   ```plaintext
   [Resolve]
   DNS=192.168.100.2 8.8.8.8
   Domains=prova.lan
   ```

3. Reinicie o resolvedor para aplicar as mudanças:
   ```bash
   sudo systemctl restart systemd-resolved
   ```
   
3. **Reiniciar e Verificar Conexão:**
   - Reinicie a máquina:
   ```bash
   sudo reboot
   ```
   - Teste o IP, ping para `prova.lan` e o gateway.
   - Desligue a máquina e crie um snapshot.

### Configuração do DNS2 como Slave no Bind9

#### **Passo 1: Instalar o Bind9 no DNS2**
1. Instale o Bind9:
   ```bash
   sudo apt update && sudo apt install bind9 -y
   ```

---

#### **Passo 2: Configurar as Zonas no DNS2**
1. Edite o arquivo de zonas padrão do Bind:
   ```bash
   sudo nano /etc/bind/named.conf.local
   ```
2. Adicione as configurações abaixo para criar as zonas **prova.lan** e a zona reversa **100.16.172.in-addr.arpa**:
   ```bash
   // Zona direta para prova.lan
   zone "prova.lan" {
       type slave;
       file "/etc/bind/ifro/prova.db"; // Caminho do arquivo de zona
       masters { 192.168.100.2; };    // IP do servidor master
   };

   // Zona reversa para 192.168.100.0/24
   zone "100.16.172.in-addr.arpa" {
       type slave;
       file "/etc/bind/ifro/lab.rev"; // Caminho do arquivo de zona reversa
       masters { 192.168.100.2; };     // IP do servidor master
   };
   ```

---

#### **Passo 3: Criar Diretório para os Arquivos de Zona**
1. Crie o diretório onde os arquivos de zona serão armazenados:
   ```bash
   sudo mkdir -p /etc/bind/ifro
   ```

---

#### **Passo 5: Reiniciar o Serviço Bind9**
1. Reinicie o serviço Bind9 para carregar as novas configurações:
   ```bash
   sudo systemctl restart bind9
   ```

2. Verifique se o serviço está ativo:
   ```bash
   sudo systemctl status bind9
   ```
   Certifique-se de que o serviço está **"active (running)"**.

---

#### **Passo 6: Testar as Configurações**
1. Teste a resolução de nomes usando o **dig**:
   ```bash
   dig @192.168.100.3 prova.lan
   dig @192.168.100.3 -x 192.168.100.2
   ```

2. Se tudo estiver configurado corretamente, você verá as respostas das consultas apontando para o DNS1 como servidor mestre.

---

- Use o comando abaixo para identificar problemas:
  ```bash
  sudo named-checkconf
  ```
- Para validar arquivos de zona:
  ```bash
  sudo named-checkzone prova.lan /etc/bind/ifro/prova.db
  sudo named-checkzone 100.16.172.in-addr.arpa /etc/bind/ifro/lab.rev
  ```
- **CRIE UM SNAPSHOT**
---

### **Configuração do WEB**

1. **Configuração de IP Fixo:**
   - Edite o arquivo `/etc/netplan/50-cloud-init.yaml` com o seguinte conteúdo:
   ```yaml
   network:
     version: 2
     ethernets:
       enp0s3:
         dhcp4: false
         addresses:
           - 192.168.100.4/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - prova.lan
         routes:
           - to: default
             via: 192.168.100.1
   ```

   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

2. **Configuração de DNS:**
   - Edite `/etc/systemd/resolved.conf`:
   ```ini
   [Resolve]
   DNS=192.168.100.2 192.168.100.3 8.8.8.8
   Domains=prova.lan
   ```
   ```bash
   sudo rm /etc/resolv.conf
   ```
   - Reinicie a máquina e verifique o IP, teste internet com `ping prova.lan` e `ping` para o gateway.
   - Desligue a máquina e crie um snapshot.


#### 3.1. Configurar o Apache na máquina WEB

- `ssh -p 54000 aluno@192.168.56.2`
  
1. **Instalar o Apache2**:
    ```bash
    sudo apt update && sudo apt install apache2 -y
    ```

3. **Ativar o módulo SSL**:
    ```bash
    sudo a2enmod ssl
    ```

4. **Ativar o módulo Rewrite**:
    ```bash
    sudo a2enmod rewrite
    ```

5. **Reiniciar o Apache**:
    ```bash
    sudo systemctl restart apache2
    ```

6. **Instalar o PHP**:
    ```bash
    sudo apt install php -y
    ```

7. **Criar o arquivo de teste PHP**:
    ```bash
    sudo nano /var/www/html/index.php
    ```
    - Adicionar o conteúdo:
      ```php
      <?php phpinfo(); ?>
      ```

8. **Configurar o arquivo de configuração do Apache**:
    ```bash
    sudo nano /etc/apache2/apache2.conf
    ```
    - Adicionar a seguinte configuração:
      ```apache
      <Directory /srv/>
          Options Indexes FollowSymLinks
          AllowOverride None
          Require all granted
      </Directory>
      ```

9. **Acessar o diretório de sites disponíveis**:
    ```bash
    cd /etc/apache2/sites-available/
    ```

10. **Criar o arquivo de configuração do site**:
    ```bash
    sudo nano web.lab.conf
    ```
    - Adicionar o seguinte conteúdo:
      ```apache
      <VirtualHost *:80>
          ServerAdmin meuemail@email.com
          ServerName web.prova.lan
          ServerAlias web.prova.lan
          DocumentRoot /srv/lab/web
          ErrorLog ${APACHE_LOG_DIR}/web_error.log
          CustomLog ${APACHE_LOG_DIR}/web_access.log combined
      </VirtualHost>
      ```

11. **Criar o diretório do site**:
    ```bash
    sudo mkdir -p /srv/lab/web
    ```

12. **Criar o arquivo de teste do site**:
    ```bash
    sudo nano /srv/lab/web/index.php
    ```
    - Adicionar o seguinte conteúdo:
      ```php
      <?php
          echo getcwd() . "\n";
          chdir('cvs');
      ?>
      ```

13. **Ativar o site**:
    ```bash
    sudo a2ensite web.lab.conf
    ```

14. **Recarregar o Apache**:
    ```bash
    sudo systemctl reload apache2
    ```
    
**Teste e salve SNAPSHOT**
---

### 2. **Instalação e Configuração de SSL**
1. Instale os pacotes necessários:
   ```bash
   sudo apt install openssl ssl-cert
   ```

2. Crie o diretório para armazenar os certificados:
   ```bash
   sudo mkdir -p /etc/apache2/ssl
   ```

3. Gere a chave privada e o CSR (Certificate Signing Request):
   ```bash
   sudo openssl genrsa -out /etc/apache2/ssl/web.key 2048
   sudo openssl req -new -key /etc/apache2/ssl/web.key -out /etc/apache2/ssl/web.csr
   ```

   ```bash
   Country Name (2 letter code) [AU]:BR
   State or Province Name (full name) [Some-State]:Rondonia
   Locality Name (eg, city) []:Ariquemes
   Organization Name (eg, company) [Internet Widgits Pty td]:Laboratório
   Organizational Unit Name (eg, section) []:TI
   Common Name (e.g. server FQDN or YOUR name) []:web.prova.lan
   Email Address []:suporte@prova.lan

   Please enter the following 'extra' attributes
   to be sent with your certificate request
   A challenge password []:aluno
   An optional company name []:aluno
   ```

5. Crie o certificado autoassinado:
   ```bash
   sudo openssl x509 -req -days 365 -in /etc/apache2/ssl/web.csr -signkey /etc/apache2/ssl/web.key -out /etc/apache2/ssl/web.crt
   ```

6. Ajuste as permissões dos arquivos:
   ```bash
   sudo chmod 600 /etc/apache2/ssl/web.key
   sudo chmod 600 /etc/apache2/ssl/web.csr
   ```

---

### 3. **Configuração do VirtualHost SSL e Redirecionamento**
1. Edite o arquivo `sudo nano /etc/apache2/sites-available/web-ssl.conf` com o seguinte conteúdo:
   ```apache
   <VirtualHost *:443>
       ServerAdmin suporte@prova.lan
       ServerName web.prova.lan:443
       DocumentRoot /srv/lab/web
       ErrorLog ${APACHE_LOG_DIR}/web-error.log
       CustomLog ${APACHE_LOG_DIR}/web.log combined

       SSLEngine on
       SSLCertificateFile /etc/apache2/ssl/web.crt
       SSLCertificateKeyFile /etc/apache2/ssl/web.key
   </VirtualHost>

   <VirtualHost *:80>
       RewriteEngine on
       ServerName web.prova.lan
       Options FollowSymLinks
       RewriteCond %{SERVER_PORT} 80
       RewriteRule ^(.*)$ https://web.prova.lan/ [R,L]
   </VirtualHost>
   ```

2. Ative o site e os módulos necessários:
   ```bash
   sudo a2ensite web-ssl.conf
   sudo a2enmod ssl
   sudo a2enmod rewrite
   ```

3. Reinicie o Apache:
   ```bash
   sudo systemctl restart apache2
   ```
**TESTE E CRIE SNAPSHOT**
---

## 5. Configuração do FTP

### 5.1 Configurações na máquina DNS1

1. **Editar o arquivo de zona do BIND**  
   Abra o arquivo de configuração do BIND para editar a zona do domínio `prova.lan`:
   ```bash
   sudo nano /etc/bind/ifro/prova.db
   ```

2. **Adicionar as configurações de DNS**  
   Adicione ou edite as seguintes linhas no arquivo de zona:

   ```txt
   web     IN      A       192.168.100.4
   ftp     IN      A       192.168.100.4
   ```

3. **Reiniciar o serviço BIND**  
   Após editar o arquivo, reinicie o serviço BIND para aplicar as mudanças:
   ```bash
   sudo systemctl restart bind9
   ```

4. **Verificar a resolução DNS**  
   Use o comando `dig` para verificar se o servidor FTP (`ftp.prova.lan`) resolve corretamente para o IP `192.168.100.4`:
   ```bash
   dig ftp.prova.lan
   ```
   O retorno esperado deve ser:
   ```txt
   ;; ANSWER SECTION:
   ftp.prova.lan.       604800  IN  A  192.168.100.4
   ```

---

### 5.2 Configurações na máquina WEB

1. **Instalar o ProFTPD**  
   Para instalar o servidor FTP ProFTPD, execute o seguinte comando:
   ```bash
   sudo apt install proftpd -y
   ```

2. **Criar o diretório FTP**  
   Crie o diretório onde os arquivos do FTP serão armazenados:
   ```bash
   sudo mkdir -p /srv/lab/ftp
   ```

3. **Alterar a propriedade do diretório**  
   Modifique a propriedade do diretório para o usuário e grupo `aluno`:
   ```bash
   sudo chown aluno:aluno /srv/lab/ftp
   ```

4. **Ajustar as permissões do diretório**  
   Defina as permissões adequadas para o diretório FTP:
   ```bash
   sudo chmod 755 /srv/lab/ftp
   ```

5. **Configurar o ProFTPD**  
   Abra o arquivo de configuração do ProFTPD para definir o nome do servidor e o diretório raiz:
   ```bash
   sudo nano /etc/proftpd/proftpd.conf
   ```

   Adicione ou edite as seguintes linhas:
   ```txt
   ServerName "Laboratorio"
   # Use this to jail all users in their homes
   DefaultRoot /srv/lab/ftp
   ```

6. **Reiniciar o ProFTPD**  
   Após as configurações, reinicie o serviço ProFTPD para aplicar as mudanças:
   ```bash
   sudo systemctl restart proftpd
   ```

---

### 5.3 Teste no Ubuntu

1. **Testar a conexão FTP**  
   No Ubuntu, execute o comando FTP para testar a conexão com o servidor FTP configurado:
   ```bash
   ftp ftp.prova.lan
   ```
**TESTE E SALVE SNAPSHOT, NO DNS1, WEB, E UBUNTU**
---

## 6. Configuração do NFS

### 6.1 Configurar o Servidor NFS na Máquina WEB

1. **Atualizar o sistema**  
   Antes de instalar o NFS, é importante atualizar o sistema:
   ```bash
   sudo apt update
   ```

2. **Instalar o NFS Kernel Server**  
   Instale o pacote necessário para configurar o servidor NFS:
   ```bash
   sudo apt install nfs-kernel-server -y
   ```

3. **Criar o diretório compartilhado**  
   Crie o diretório que será compartilhado via NFS:
   ```bash
   sudo mkdir -p /srv/lab/nfs
   ```

4. **Alterar a propriedade do diretório**  
   Defina a propriedade do diretório para o usuário `nobody` e grupo `nogroup`, que são comuns para compartilhamentos NFS:
   ```bash
   sudo chown nobody:nogroup /srv/lab/nfs
   ```

5. **Ajustar as permissões do diretório**  
   Altere as permissões do diretório para permitir o acesso necessário:
   ```bash
   sudo chmod 755 /srv/lab/nfs
   ```

6. **Configurar o arquivo de exportação**  
   Edite o arquivo `/etc/exports` para definir quais diretórios serão compartilhados e suas permissões. Abra o arquivo para edição:
   ```bash
   sudo nano /etc/exports
   ```

   Adicione a seguinte linha para permitir o acesso ao diretório `/srv/lab/nfs` da rede `192.168.100.0/24` com permissões de leitura e gravação:
   ```txt
   /srv/lab/nfs 192.168.100.0/24(rw,no_root_squash,sync)
   ```

7. **Reiniciar o serviço NFS**  
   Após a configuração, reinicie o serviço NFS para aplicar as mudanças:
   ```bash
   sudo systemctl restart nfs-kernel-server
   ```

8. **Verificar os compartilhamentos NFS**  
   Use o comando `exportfs -v` para verificar se o diretório foi corretamente exportado:
   ```bash
   sudo exportfs -v
   ```


---

### 6.2 Configurar o Cliente NFS na Máquina Ubuntu

1. **Atualizar o sistema**  
   Assim como no servidor, é importante atualizar o sistema do cliente NFS:
   ```bash
   sudo apt update
   ```

2. **Instalar o NFS Common**  
   Instale o pacote necessário para montar os compartilhamentos NFS:
   ```bash
   sudo apt install nfs-common -y
   ```

3. **Criar o diretório de montagem**  
   Crie o diretório onde o compartilhamento NFS será montado:
   ```bash
   sudo mkdir -p /mnt/nfs_docs
   ```

4. **Montar o compartilhamento NFS**  
   Monte o diretório compartilhado do servidor NFS no diretório de montagem local:
   ```bash
   sudo mount 192.168.100.4:/srv/lab/nfs /mnt/nfs_docs
   ```

5. **Verificar a montagem**  
   Verifique se o compartilhamento foi montado corretamente, utilizando o comando `df -h`:
   ```bash
   df -h
   ```

6. **Realizar um teste**  
   Teste o acesso ao compartilhamento, por exemplo, criando um arquivo no diretório montado:
   ```bash
   sudo touch /mnt/nsf_docs/teste.txt
   ```

7. **Adicionar ao fstab para montagem automática**  
   Para que o compartilhamento NFS seja montado automaticamente ao iniciar o sistema, edite o arquivo `/etc/fstab`:
   ```bash
   sudo nano /etc/fstab
   ```

   Adicione a seguinte linha ao final do arquivo:
   ```txt
   192.168.100.4:/srv/lab/nfs /mnt/nfs_docs nfs defaults 0 0
   ```

8. **Testar a montagem automática**  
   Após editar o `fstab`, faça um teste reiniciando a máquina e verificando se o compartilhamento foi montado automaticamente:
   ```bash
   sudo reboot
   df -h
   ```

**Criar snapshot da máquina UBUNTU e WEB**

---

Aqui está a versão melhorada e complementada do seu texto:

---

## 7. Configurar o PROXY

## 7.1 Configurar o PROXY na máquina GATEWAY

### 1. **Instalar o Squid (Proxy Server)**
   Para instalar o Squid, um dos servidores proxy mais populares, execute o seguinte comando:
   ```bash
   sudo apt update && sudo apt install squid -y
   ```

### 2. **Acessar o diretório de configuração do Squid**
   O arquivo de configuração do Squid está localizado no diretório `/etc/squid`. Acesse o diretório com o comando:
   ```bash
   cd /etc/squid
   ```

### 3. **Criar um backup do arquivo de configuração original**
   Antes de fazer qualquer alteração no arquivo de configuração, é recomendado criar um backup do arquivo original para garantir que você possa restaurá-lo em caso de problemas:
   ```bash
   sudo cp squid.conf squid.conf.backup
   ```

### 4. **Limpar e formatar o arquivo de configuração**
   O arquivo de configuração do Squid pode conter comentários e linhas em branco que não são necessários. Use o comando `sed` para limpar o arquivo, removendo:
   - Comentários (linhas que começam com `#`).
   - Linhas em branco.
   - Múltiplas quebras de linha consecutivas, que serão substituídas por apenas uma.
   
   Para fazer isso, execute:
   ```bash
   sudo sed -i '/^\s*#/d; /^\s*$/d' squid.conf
   ```

### 5. **Editar o arquivo de configuração do Squid**
   Agora, edite o arquivo `squid.conf` para configurar o proxy conforme necessário. Use o seguinte comando para abrir o arquivo em um editor de texto:
   ```bash
   sudo nano squid.conf
   ```

   **ATENÇÃO:** O Squid segue uma ordem de prioridade nas regras. Aqui está uma sequência recomendada para a organização das regras:

#### 5.1. **Definir Permissões Explícitas**
   Primeiramente, defina regras que permitam acessos específicos, que devem ter prioridade sobre as outras configurações.
   
   Exemplo:
   ```bash
   acl usuarios src 192.168.0.0/24  # Definindo a rede de usuários permitidos
   acl libera_geral time MTWHF 11:40-13:05  # Definindo o horário de acesso liberado
   http_access allow usuarios libera_geral  # Permitindo acesso durante o horário especificado
   ```

#### 5.2. **Estabelecer Restrições Explícitas**
   Em seguida, defina as regras que bloqueiam acessos indesejados, como bloqueios por URL ou palavras-chave específicas.
   
   Exemplo:
   ```bash
   # Bloqueando URL que contém a palavra 'ifro'
   acl blocked_urls url_regex -i ifro
   http_access deny aula blocked_urls  # Negando acesso para usuários da rede 'aula'
   ```

#### 5.3. **Permitir Acesso para a Rede Local**
   Agora, permita o acesso à rede local ou a outros grupos amplos de usuários sem restrições específicas.
   
   Exemplo:
   ```bash
   # Permitindo o acesso à rede interna (sub-rede 192.168.100.0/24)
   acl aula src 192.168.100.0/24
   http_access allow aula  # Permitindo acesso à rede interna
   ```

#### 5.4. **Definir Bloqueio Geral**
   Por fim, adicione uma regra que negue todo o tráfego que não corresponda a nenhuma das regras anteriores. Essa é a última linha de defesa, que bloqueia todas as conexões não autorizadas.
   
   Exemplo:
   ```bash
   # Bloqueando todo o tráfego não autorizado
   http_access deny all
   ```

### 6. **Salvar e Aplicar as Configurações**
   Após editar o arquivo de configuração, salve as alterações e saia do editor. Para que as novas configurações entrem em vigor, reinicie o serviço do Squid com o seguinte comando:
   ```bash
   sudo systemctl restart squid
   ```

### 7. **Verificar o Status do Squid**
   Verifique se o Squid está funcionando corretamente após reiniciar o serviço:
   ```bash
   sudo systemctl status squid
   ```

   O serviço deve estar ativo e funcionando. Se houver algum erro, verifique os logs para mais informações:
   ```bash
   sudo tail -f /var/log/squid/access.log
   ```

---

Aqui está a versão organizada e complementada da parte 2 do texto:

---

# 7.2 Configuração do PROXY na Máquina Ubuntu

### 1. **Configurar Proxy no Navegador Firefox**

1. **Abrir o Firefox**:
   - Acesse as configurações do navegador através de **Configurações** > **Rede** > **Configurar Rede**.

2. **Escolher Configuração Manual de Proxy**:
   - Selecione a opção **Configuração manual de proxy**.

3. **Inserir os Dados do Proxy**:
   - **Endereço do Proxy**: Insira o IP do Gateway (por exemplo, `192.168.100.1`).
   - **Porta**: Insira a porta do Squid (geralmente, `3128`).

4. **Configuração para HTTPS**:
   - Marque a opção **Usar também para HTTPS** para garantir que o proxy seja utilizado também para conexões HTTPS.

5. **Salvar Configurações**:
   - Após inserir os dados corretamente, clique em **OK** ou **Salvar** para aplicar as configurações de proxy.

---

# 7.3 Teste da Configuração do Proxy

### 1. **Realizar o Teste de Navegação**

   Após configurar o proxy, abra o navegador (Firefox) e tente acessar alguns sites para garantir que a navegação está sendo feita corretamente através do proxy.

### 2. **Verificar o Uso do Proxy**

   Para confirmar que a máquina Ubuntu está utilizando o proxy corretamente, verifique os logs do Squid na máquina GATEWAY. O log padrão do Squid pode ser encontrado em:
   ```bash
   /var/log/squid/access.log
   ```

### 3. **Testar a Conexão com o Proxy Usando `curl`**

   Você pode usar o comando `curl` para testar a conectividade com o proxy:
   ```bash
   curl --proxy http://192.168.100.1:3128 http://example.com
   ```
   Isso deve retornar a página solicitada, confirmando que o proxy está funcionando corretamente.

---

# 7.4 Criar Snapshot da Máquina Ubuntu

Após a configuração e os testes, crie um snapshot da máquina Ubuntu para garantir um ponto de recuperação caso necessário.

---

# 7.5 Bloquear URLs Usando `url_regex` no Squid

Agora que o Squid está funcionando como proxy, podemos adicionar regras para bloquear acessos a URLs específicas usando expressões regulares (`url_regex`). Vamos configurar isso no arquivo de configuração do Squid (`squid.conf`).

## 7.5.1 Editar o Arquivo `squid.conf`

### 1. **Abrir o Arquivo de Configuração do Squid**

   No diretório `/etc/squid`, abra o arquivo de configuração `squid.conf` para edição:
   ```bash
   sudo nano /etc/squid/squid.conf
   ```

### 2. **Definir as Regras de Bloqueio de URLs**

   O `url_regex` permite bloquear URLs com base em expressões regulares. A seguir, um exemplo para bloquear URLs que contenham a palavra "forbidden":

   - **Exemplo de Bloqueio de URLs**:
     Adicione a seguinte linha para bloquear URLs com a palavra "forbidden":
     ```bash
     acl blocked_urls url_regex -i forbidden
     ```
     A opção `-i` torna a expressão regular case-insensitive (ignorando maiúsculas e minúsculas), ou seja, bloqueará "forbidden", "Forbidden", "FORBIDDEN", etc.

### 3. **Aplicar a Regra de Bloqueio**

   Para aplicar a regra de bloqueio no Squid, adicione a seguinte linha após a configuração da rede interna (`http_access allow aula`):
   ```bash
   http_access deny blocked_urls
   ```

   Após editar o arquivo, reconfigure o Squid:
   ```bash
   sudo squid -k reconfigure
   sudo systemctl restart squid
   sudo systemctl status squid
   ```

### 4. **Revisar o Fluxo das Regras de Acesso**

   Certifique-se de que as regras de bloqueio estejam posicionadas corretamente, antes da regra geral de negação. O fluxo de regras deve ser similar a este:

   ```bash
   http_access allow aula
   http_access deny blocked_urls
   http_access deny all
   ```

---

# Exemplos de Configuração de Bloqueios Específicos

### 1. **Bloquear uma Faixa de IP para Não Baixar Arquivos ZIP**

   Para bloquear o download de arquivos com a extensão `.zip` para uma faixa de IP específica:

   **Passos**:
   1. Crie uma ACL para identificar arquivos `.zip`:
      ```bash
      acl arquivos_zip url_regex zip
      ```
   2. Defina a faixa de IP a ser bloqueada (por exemplo, `192.168.0.0/24`):
      ```bash
      acl proibido_acesso src 192.168.0.0/24
      ```
   3. Bloqueie o acesso aos arquivos ZIP para essa faixa de IP:
      ```bash
      http_access deny proibido_acesso arquivos_zip
      ```

   **Exemplo de configuração**:
   ```bash
   acl arquivos_zip url_regex zip
   acl proibido_acesso src 192.168.0.0/24
   http_access deny proibido_acesso arquivos_zip
   ```

---

### 2. **Bloquear um Site para Todos os Usuários da Rede**

   Para bloquear um site (exemplo: Facebook) para todos os usuários da rede:

   **Passos**:
   1. Crie uma ACL para identificar o site a ser bloqueado:
      ```bash
      acl site_proibido dstdomain .facebook.com
      ```
   2. Bloqueie o acesso a esse site para todos os usuários:
      ```bash
      http_access deny all site_proibido
      ```

   **Exemplo de configuração**:
   ```bash
   acl site_proibido dstdomain .facebook.com
   http_access deny all site_proibido
   ```

---

### 3. **Controlar o Acesso por Hora**

   Para bloquear o acesso durante determinados horários para usuários de uma faixa de IP específica (por exemplo, `192.168.0.0/24`):

   **Passos**:
   1. Defina a ACL para o horário (exemplo: segunda a sexta-feira, das 08:05 às 11:40):
      ```bash
      acl fechado_para_aula time MTWHF 08:05-11:40
      ```
   2. Defina a ACL para a faixa de IP (exemplo: `192.168.0.0/24`):
      ```bash
      acl hora_de_aula src 192.168.0.0/24
      ```
   3. Bloqueie o acesso durante esse horário:
      ```bash
      http_access deny hora_de_aula fechado_para_aula
      ```

   **Exemplo de configuração**:
   ```bash
   acl fechado_para_aula time MTWHF 08:05-11:40
   acl hora_de_aula src 192.168.0.0/24
   http_access deny hora_de_aula fechado_para_aula
   ```

---

### 4. **Liberar o Acesso Somente em um Determinado Horário**

   Para permitir o acesso a uma faixa de IP específica (exemplo: `192.168.0.0/24`) apenas em um horário específico (exemplo: segunda a sexta-feira, das 11:40 às 13:05):

   **Passos**:
   1. Defina a ACL para a faixa de IP:
      ```bash
      acl usuarios src 192.168.0.0/24
      ```
   2. Defina a ACL para o horário (exemplo: das 11:40 às 13:05):
      ```bash
      acl libera_geral time MTWHF 11:40-13:05
      ```
   3. Permita o acesso para os usuários nesse horário:
      ```bash
      http_access allow usuarios libera_geral
      ```
   4. Bloqueie o acesso fora desse horário:
      ```bash
      http_access deny usuarios
      ```

   **Exemplo de configuração**:
   ```bash
   acl usuarios src 192.168.0.0/24
   acl libera_geral time MTWHF 11:40-13:05
   http_access allow usuarios libera_geral
   http_access deny usuarios
   ```

---

### 5. **Usar um Arquivo de Texto para Bloquear Diversos Sites**

   Se a lista de sites ou usuários a serem bloqueados for longa, você pode usar um arquivo externo com os sites a serem bloqueados.

   **Passos**:
   1. Defina uma ACL para a faixa de IP:
      ```bash
      acl usuarios src 192.168.0.0/24
      ```
   2. Crie uma ACL para carregar a lista de sites bloqueados de um arquivo:
      ```bash
      acl sites_proibidos url_regex "/caminho/para/arquivo_sites.txt"
      ```
   3. Bloqueie o acesso a esses sites para a faixa de IP:
      ```bash
      http_access deny usuarios sites_proibidos
      ```

   **Exemplo de configuração**:
   ```bash
   acl usuarios src 192.168.0.0/24
   acl sites_proibidos url_regex "/etc/squid/arquivo_sites.txt"
   http_access deny usuarios sites_proibidos
   ```

---

### Considerações Finais

- **Testar as Configurações**: Sempre teste as configurações após realizar alterações:
  ```bash
  sudo squid -k reconfigure
  ```

- **Backup**: Antes de realizar qualquer modificação, é recomendável fazer um backup:
  ```bash
  sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.backup
  ```

- **Logs**: Para diagnóstico de problemas ou verificação das regras, consulte os logs do Squid, geralmente encontrados em:
  ```bash
  /var/log/squid/access.log
  ```



Para instalar o **phpMyAdmin** em um **Ubuntu Server**, você pode seguir os seguintes passos. O phpMyAdmin é uma ferramenta web popular para gerenciar bancos de dados MySQL/MariaDB e oferece uma interface gráfica para facilitar a administração dos bancos de dados. O processo de instalação é bem simples. Vou te guiar em como fazer isso.

### 1. Atualizar o sistema
Primeiro, sempre é bom garantir que os pacotes do seu servidor estão atualizados:

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar o PHP e outras dependências
O **phpMyAdmin** requer o PHP para funcionar. Caso não tenha o PHP instalado ainda, execute:

```bash
sudo apt install php php-mbstring php-zip php-gd php-json php-curl php-mysqli libapache2-mod-php -y
```

Se você já tiver o PHP instalado, pode pular essa etapa.

### 3. Instalar o phpMyAdmin
Agora você pode instalar o **phpMyAdmin**:

```bash
sudo apt install phpmyadmin -y
```

Durante a instalação, você será solicitado a escolher o servidor web. Se estiver usando o **Apache**, selecione o Apache2. Se não aparecer a opção, você pode configurar manualmente depois.

### 4. Configurar o Apache (se necessário)
Se o Apache não foi configurado automaticamente, você precisa ativar o phpMyAdmin. Faça isso criando um link simbólico para o diretório do phpMyAdmin dentro do diretório do Apache:

```bash
sudo ln -s /usr/share/phpmyadmin /var/www/html/phpmyadmin
```

### 5. Configurar o acesso ao phpMyAdmin
Verifique se o phpMyAdmin está acessível diretamente pelo navegador. Vá até `http://<seu-servidor>/phpmyadmin` e você deverá ver a interface de login.

Se não conseguir acessar, pode ser necessário ajustar as permissões ou configurações no Apache. Para isso, adicione as seguintes configurações ao arquivo de configuração do Apache:

```bash
sudo nano /etc/apache2/conf-available/phpmyadmin.conf
```

Adicione ou verifique as configurações de segurança e permissões adequadas.

Após isso, reinicie o Apache:

```bash
sudo systemctl restart apache2
```

### 6. Configurar a segurança (opcional)
É altamente recomendável garantir a segurança da instalação do phpMyAdmin. Você pode adicionar uma camada de autenticação ao acessar a interface, configurando um `.htpasswd` ou restringindo o acesso a partir de certos IPs.

---

### Função do phpMyAdmin em relação ao pacote PHP

O **phpMyAdmin** é uma aplicação web baseada em PHP que permite gerenciar bancos de dados MySQL ou MariaDB de forma visual, com facilidade. Ele substitui a necessidade de usar a linha de comando para realizar tarefas como:

- Criar, editar e excluir bancos de dados e tabelas
- Executar consultas SQL
- Gerenciar usuários e permissões
- Importar e exportar dados

Já o **PHP** é uma linguagem de programação que serve para criar aplicações web. O **phpMyAdmin** é um exemplo de aplicação feita com PHP. Assim, o phpMyAdmin usa o PHP para interagir com o servidor de banco de dados MySQL/MariaDB por meio de uma interface gráfica, enquanto o PHP sozinho é usado para desenvolver qualquer tipo de aplicação web.

Se você estava se referindo a algo mais específico em relação ao "pacote PHP", me avise que posso esclarecer mais!








Aqui está um passo a passo detalhado para configurar uma instância do Moodle em um servidor Ubuntu que já possui Apache e PHPMyAdmin instalados:

---

### **Passo 1: Verifique os requisitos do Moodle**
Antes de começar, confirme que seu servidor atende aos requisitos de sistema do Moodle:
- **PHP:** Verifique a versão necessária para o Moodle que você está instalando.
- **MySQL/MariaDB ou PostgreSQL:** O Moodle requer um banco de dados suportado.
- **Extensões PHP:** Moodle exige várias extensões PHP como `gd`, `intl`, `mysqli`, `soap`, entre outras.

---

### **Passo 2: Atualize o sistema**
Certifique-se de que o sistema está atualizado:
```bash
sudo apt update && sudo apt upgrade -y
```

---

### **Passo 3: Instale dependências necessárias**
Instale os pacotes essenciais para o Moodle:
```bash
sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql php-xml php-mbstring php-curl php-zip php-intl php-soap php-gd php-xmlrpc unzip -y
```

Reinicie o Apache para carregar as extensões PHP:
```bash
sudo systemctl restart apache2
```

---

### **Passo 4: Baixe o Moodle**
Baixe a versão mais recente do Moodle diretamente do site oficial:
```bash
wget https://download.moodle.org/releases/latest/moodle-latest.tgz
```

Extraia o pacote e mova os arquivos para o diretório do servidor web:
```bash
tar -xvzf moodle-latest.tgz
sudo mv moodle /var/www/html/
```

---

### **Passo 5: Configure o diretório de dados**
O Moodle precisa de um diretório para armazenar dados, que não deve estar acessível publicamente. Crie-o fora do diretório raiz do Apache:
```bash
sudo mkdir /var/moodledata
sudo chown -R www-data:www-data /var/moodledata
sudo chmod -R 770 /var/moodledata
```

---

### **Passo 6: Configure permissões**
Certifique-se de que o diretório do Moodle no Apache também tenha permissões apropriadas:
```bash
sudo chown -R www-data:www-data /var/www/html/moodle
sudo chmod -R 755 /var/www/html/moodle
```

---

### **Passo 7: Configure o banco de dados**
1. Acesse o MySQL:
```bash
sudo mysql -u root -p
```
2. Crie um banco de dados e um usuário:
```sql
CREATE DATABASE moodle DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'moodleuser'@'localhost' IDENTIFIED BY 'senha_segura';
GRANT ALL PRIVILEGES ON moodle.* TO 'moodleuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

### **Passo 8: Configure o Apache para o Moodle**
Crie um arquivo de configuração para o Moodle:
```bash
sudo nano /etc/apache2/sites-available/moodle.conf
```

Adicione o seguinte conteúdo:
```apache
<VirtualHost *:80>
    ServerAdmin admin@seusite.com
    DocumentRoot /var/www/html/moodle
    ServerName seusite.com

    <Directory /var/www/html/moodle>
        Options FollowSymlinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/moodle_error.log
    CustomLog ${APACHE_LOG_DIR}/moodle_access.log combined
</VirtualHost>
```

Ative a configuração e os módulos necessários:
```bash
sudo a2ensite moodle
sudo a2enmod rewrite
sudo systemctl reload apache2
```

---

### **Passo 9: Finalize a instalação**
1. Acesse o Moodle no navegador: `http://seu-ip-ou-dominio/moodle`.
2. Siga as instruções da página para completar a instalação:
   - Escolha o banco de dados MySQL e forneça as credenciais configuradas no **Passo 7**.
   - Configure o administrador com o nome de usuário padrão e a senha: `Ifro@2025`.

---

### **Passo 10: Teste a instalação**
Acesse o Moodle e verifique se está funcionando corretamente. Você pode criar cursos e usuários adicionais para validar a funcionalidade.

Se precisar de mais assistência, estou à disposição! 😊
