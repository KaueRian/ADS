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
   - Defina o domínio como `laboratorio.lan` (ou conforme o professor informar).

3. **Configuração de Rede:**
   - **Adaptador 1:** Modo NAT.
   - **Adaptador 2:** Modo Host-Only, nome: `VirtualBox Host-Only Ethernet Adapter`.
   - **Adaptador 3:** Modo Rede Interna, nome: `SRC1`.

4. **Configuração de IP em `/etc/network/interfaces`:**
   
   `su root`
   
   ```bash
   allow-hotplug enp0s8
   iface enp0s8 inet static
   address 172.16.100.1/24

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
   supersede domain-name-servers 172.16.100.2, 172.16.100.3, 8.8.8.8;
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
     GATEWAY=172.16.100.1
     DNS1=172.16.100.2
     DNS2=172.16.100.3
     WEB=172.16.100.4
     ARQUIVO=172.16.100.5
     AUTENTICACAO=172.16.100.6
     SAMBA=172.16.100.7
     EMAIL=172.16.100.8
     ALL=0/0

     LAN=172.16.100.0/24
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
1. **Acesse via SSH:**
   ```bash
   ssh -p 51000 aluno@192.168.56.2
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
   subnet 172.16.100.0 netmask 255.255.255.0 {
     range 172.16.100.50 172.16.100.250;
     option domain-name-servers 8.8.8.8, 172.16.100.2, 172.16.100.3;
     option domain-name "laboratorio.lan";
     option routers 172.16.100.1;
     option broadcast-address 172.16.100.255;
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
   DNS=172.16.100.2 172.16.100.3 8.8.8.8
   Domains=laboratorio.lan
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
             - 172.16.100.2/24
           nameservers:
             addresses:
               - 8.8.8.8
             search:
               - laboratorio.lan
           routes:
             - to: default
               via: 172.16.100.1
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
   zone "laboratorio.lan" {
           type master;
           file "/etc/bind/ifro/lab.db";
           allow-transfer { 172.16.100.3; };
   };

   zone "100.16.172.in-addr.arpa" {
           type master;
           file "/etc/bind/ifro/lab.rev";
           allow-transfer { 172.16.100.3; };
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
   sudo cp db.local ifro/lab.db
   ```
   ```bash
   sudo cp db.127 ifro/lab.rev
   ```
   - Edite os arquivos `lab.db` e `lab.rev` conforme as instruções fornecidas.

   ```bash
   sudo nano lab.db
   ```

   ```bash
   ;
   ; BIND data file for local loopback interface
   ;
   $TTL    604800
   @       IN      SOA     laboratorio.lan. root.laboratorio.lan. (
                   1         ; Serial
                   604800    ; Refresh
                   86400     ; Retry
                   2419200   ; Expire
                   604800 )  ; Negative Cache TTL
   ;
   @       IN      NS      laboratorio.lan.
   @       IN      A       172.16.100.2
   ns      IN      A       172.16.100.2
   web     IN      A       172.16.100.4
   www     IN      CNAME   web.laboratorio.lan.
   dns1    IN      CNAME   ns.laboratorio.lan.
   ```

   ```bash
   sudo nano lab.rev
   ```

   ```bash
   ;
   ; BIND reverse data file for local loopback interface
   ;
   $TTL    604800
   @       IN      SOA     laboratorio.lan. root.laboratorio.lan. (
                   1         ; Serial
                   604800    ; Refresh
                   86400     ; Retry
                   2419200   ; Expire
                   604800 )  ; Negative Cache TTL
   ;
   @       IN      NS      laboratorio.lan.
   2       IN      PTR     laboratorio.lan.
   4       IN      PTR     web.laboratorio.lan.
   ```
  
5. **Verifique a configuração do BIND9:**
   ```bash
   sudo named-checkconf
   sudo named-checkzone laboratorio.lan lab.db
   sudo named-checkzone 100.16.172.in-addr.arpa lab.rev
   ```

**Defina o DNS:**

```bash
sudo nano /etc/systemd/resolved.conf
```
```bash
[Resolve]
DNS=172.16.100.2 172.16.100.3 8.8.8.8
Domains=laboratorio.lan
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

8. **Teste o DNS com o comando `ping laboratorio.lan`.**

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
   172.16.100.3    dns2    dns2.laboratorio.lan
   172.16.100.2    dns1    dns1.laboratorio.lan
   172.16.100.1    gateway gateway.laboratorio.lan

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
           - 172.16.100.3/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - laboratorio.lan
         routes:
           - to: default
             via: 172.16.100.1
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
   DNS=172.16.100.2 8.8.8.8
   Domains=laboratorio.lan
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
   - Teste o IP, ping para `laboratorio.lan` e o gateway.
   - Desligue a máquina e crie um snapshot.

### Configuração do DNS2 como Slave no Bind9

#### **Passo 1: Instalar o Bind9 no DNS2**
1. Atualize o sistema:
   ```bash
   sudo apt update
   ```
2. Instale o Bind9:
   ```bash
   sudo apt update && sudo apt install bind9 -y
   ```

---

#### **Passo 2: Configurar as Zonas no DNS2**
1. Edite o arquivo de zonas padrão do Bind:
   ```bash
   sudo nano /etc/bind/named.conf.local
   ```
2. Adicione as configurações abaixo para criar as zonas **laboratorio.lan** e a zona reversa **100.16.172.in-addr.arpa**:
   ```bash
   // Zona direta para laboratorio.lan
   zone "laboratorio.lan" {
       type slave;
       file "/etc/bind/ifro/lab.db"; // Caminho do arquivo de zona
       masters { 172.16.100.2; };    // IP do servidor master
   };

   // Zona reversa para 172.16.100.0/24
   zone "100.16.172.in-addr.arpa" {
       type slave;
       file "/etc/bind/ifro/lab.rev"; // Caminho do arquivo de zona reversa
       masters { 172.16.100.2; };     // IP do servidor master
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
   dig @172.16.100.3 laboratorio.lan
   dig @172.16.100.3 -x 172.16.100.2
   ```

2. Se tudo estiver configurado corretamente, você verá as respostas das consultas apontando para o DNS1 como servidor mestre.

---

- Use o comando abaixo para identificar problemas:
  ```bash
  sudo named-checkconf
  ```
- Para validar arquivos de zona:
  ```bash
  sudo named-checkzone laboratorio.lan /etc/bind/ifro/lab.db
  sudo named-checkzone 100.16.172.in-addr.arpa /etc/bind/ifro/lab.rev
  ```

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
           - 172.16.100.4/24
         nameservers:
           addresses:
             - 8.8.8.8
           search:
             - laboratorio.lan
         routes:
           - to: default
             via: 172.16.100.1
   ```

   - Aplique a configuração:
   ```bash
   sudo netplan apply
   ```

2. **Configuração de DNS:**
   - Edite `/etc/systemd/resolved.conf`:
   ```ini
   [Resolve]
   DNS=172.16.100.2 172.16.100.3 8.8.8.8
   Domains=laboratorio.lan
   ```
   ```bash
   sudo rm /etc/resolv.conf
   ```
   - Reinicie a máquina e verifique o IP, teste internet com `ping laboratorio.lan` e `ping` para o gateway.
   - Desligue a máquina e crie um snapshot.


#### 3.1. Configurar o Apache na máquina WEB

1. **Atualizar o sistema**:
    ```bash
    sudo apt update
    ```

2. **Instalar o Apache2**:
    ```bash
    sudo apt install apache2 -y
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
          ServerName web.laboratorio.lan
          ServerAlias web.laboratorio.lan
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
   Common Name (e.g. server FQDN or YOUR name) []:web.laboratorio.lan
   Email Address []:suporte@laboratorio.lan

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
       ServerAdmin suporte@laboratorio.lan
       ServerName web.laboratorio.lan:443
       DocumentRoot /srv/lab/web
       ErrorLog ${APACHE_LOG_DIR}/web-error.log
       CustomLog ${APACHE_LOG_DIR}/web.log combined

       SSLEngine on
       SSLCertificateFile /etc/apache2/ssl/web.crt
       SSLCertificateKeyFile /etc/apache2/ssl/web.key
   </VirtualHost>

   <VirtualHost *:80>
       RewriteEngine on
       ServerName web.laboratorio.lan
       Options FollowSymLinks
       RewriteCond %{SERVER_PORT} 80
       RewriteRule ^(.*)$ https://web.laboratorio.lan/ [R,L]
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

---

## 5. Configuração do FTP

### 5.1 Configurações na máquina DNS1

1. **Editar o arquivo de zona do BIND**  
   Abra o arquivo de configuração do BIND para editar a zona do domínio `laboratorio.lan`:
   ```bash
   sudo nano /etc/bind/lab/lab.db
   ```

2. **Adicionar as configurações de DNS**  
   Adicione ou edite as seguintes linhas no arquivo de zona:

   ```txt
   web     IN      A       172.16.100.4
   ftp     IN      A       172.16.100.4
   ```

3. **Reiniciar o serviço BIND**  
   Após editar o arquivo, reinicie o serviço BIND para aplicar as mudanças:
   ```bash
   sudo systemctl restart bind9
   ```

4. **Verificar a resolução DNS**  
   Use o comando `dig` para verificar se o servidor FTP (`ftp.laboratorio.lan`) resolve corretamente para o IP `172.16.100.4`:
   ```bash
   dig ftp.laboratorio.lan
   ```
   O retorno esperado deve ser:
   ```txt
   ;; ANSWER SECTION:
   ftp.laboratorio.lan.       604800  IN  A  172.16.100.4
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
   ftp ftp.laboratorio.lan
   ```

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

   Adicione a seguinte linha para permitir o acesso ao diretório `/srv/lab/nfs` da rede `172.16.100.0/24` com permissões de leitura e gravação:
   ```txt
   /srv/lab/nfs 172.16.100.0/24(rw,no_root_squash,sync)
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

**Criar snapshot da máquina WEB**

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
   sudo mkdir -p /nfs/docs
   ```

4. **Montar o compartilhamento NFS**  
   Monte o diretório compartilhado do servidor NFS no diretório de montagem local:
   ```bash
   sudo mount 172.16.100.4:/srv/lab/nfs /nfs/docs
   ```

5. **Verificar a montagem**  
   Verifique se o compartilhamento foi montado corretamente, utilizando o comando `df -h`:
   ```bash
   df -h
   ```

6. **Realizar um teste**  
   Teste o acesso ao compartilhamento, por exemplo, criando um arquivo no diretório montado:
   ```bash
   sudo touch /nfs/docs/teste.txt
   ```

7. **Adicionar ao fstab para montagem automática**  
   Para que o compartilhamento NFS seja montado automaticamente ao iniciar o sistema, edite o arquivo `/etc/fstab`:
   ```bash
   sudo nano /etc/fstab
   ```

   Adicione a seguinte linha ao final do arquivo:
   ```txt
   172.16.100.4:/srv/lab/nfs /nfs/docs nfs defaults 0 0
   ```

8. **Testar a montagem automática**  
   Após editar o `fstab`, faça um teste reiniciando a máquina e verificando se o compartilhamento foi montado automaticamente:
   ```bash
   sudo reboot
   df -h
   ```

**Criar snapshot da máquina UBUNTU**

---

# 7 Configurar o PROXY

## 7.1 Configurar o PROXY na máquina GATEWAY

1. **Atualizar os pacotes da máquina**:
   ```bash
   sudo apt update
   ```

2. **Instalar o Squid (Proxy Server)**:
   ```bash
   sudo apt install squid -y
   ```

3. **Acessar o diretório de configuração do Squid**:
   ```bash
   cd /etc/squid
   ```

4. **Criar um backup do arquivo de configuração original**:
   Para garantir que você tenha uma cópia de segurança, execute o seguinte comando:
   ```bash
   sudo cp squid.conf squid.conf.backup
   ```

5. **Limpar e formatar o arquivo de configuração**:
   O comando `sed` será usado para:
   - Remover todos os comentários (`#` no início das linhas).
   - Remover linhas em branco.
   - Substituir múltiplas quebras de linha seguidas por apenas uma.
   ```bash
   sudo sed -i '/^\s*#/d; /^\s*$/d' squid.conf
   ```

6. **Editar o arquivo de configuração do Squid**:
   Agora, edite o arquivo `squid.conf` para definir as regras de acesso e configurar o proxy conforme necessário:
   ```bash
   sudo nano squid.conf
   ```

   **Exemplo de configurações a serem feitas dentro do arquivo**:

   - **Definir a Rede Interna**:
     No arquivo de configuração, adicione ou modifique as linhas para definir a rede interna.
     ```bash
     acl aula src 172.16.100.0/24
     ```

   - **Permitir o acesso da rede interna**:
     Antes da linha `http_access deny all;`, insira a configuração para permitir o acesso à rede interna:
     ```bash
     # permitindo rede interna
     http_access allow aula
     ```

7. **Salvar a configuração e fechar o editor**:
   Após editar o arquivo conforme necessário, salve e feche o arquivo (no `nano`, pressione `Ctrl + X`, depois `Y` para confirmar e `Enter` para salvar).

8. **Criar um snapshot da máquina GATEWAY**:
   Para garantir que você possa restaurar o sistema caso algo dê errado, crie um snapshot da máquina GATEWAY.

---

## 7.2 Configurar o PROXY na máquina UBUNTU

1. **No navegador Firefox**:
   
   - Abra o Firefox e vá até **Configurações** > **Rede** > **Configurar Rede**.
   
2. **Escolher a configuração manual de proxy**:
   - Selecione a opção **Configuração manual de proxy**.
   
3. **Inserir os dados do Proxy**:
   - **Endereço do Proxy**: Insira o IP do Gateway (por exemplo, `172.16.100.1`).
   - **Porta**: Insira a porta do Squid (geralmente, `3128`).
   
4. **Configuração para HTTPS**:
   - Marque a opção **Usar também para HTTPS** para que o proxy seja utilizado também para conexões HTTPS.

5. **Salvar as configurações**:
   Após inserir os dados corretamente, clique em **OK** ou **Salvar** para aplicar as configurações de proxy.

---

## 7.3 Teste da Configuração do Proxy

1. **Realizar o teste de navegação**:
   Após configurar o proxy, abra o navegador (Firefox) e tente acessar alguns sites para garantir que a navegação está sendo feita corretamente através do Proxy.

2. **Verificar se a máquina Ubuntu está usando o proxy corretamente**:
   - Você pode verificar se o tráfego está passando pelo proxy, observando os logs do Squid na máquina GATEWAY. O log padrão do Squid pode ser encontrado em:
     ```bash
     /var/log/squid/access.log
     ```

3. **Testar a conexão**:
   - Teste a conectividade com o proxy usando o comando `curl`:
     ```bash
     curl --proxy http://172.16.100.1:3128 http://example.com
     ```
   Isso deve retornar a página solicitada, confirmando que o proxy está funcionando corretamente.

---

## 7.4 Criar Snapshot da Máquina Ubuntu

Após a configuração e testes, crie um snapshot da máquina Ubuntu para garantir que você tenha um ponto de recuperação caso necessário.

---

---

# 7.5 Bloquear URLs usando `url_regex` no Squid

Agora que o Squid está configurado e funcionando como proxy, podemos adicionar regras para bloquear acessos a URLs específicas usando expressões regulares (`url_regex`). A configuração será feita no arquivo de configuração do Squid, `squid.conf`.

## 7.5.1 Editar o arquivo `squid.conf`

1. **Abrir o arquivo de configuração do Squid**:
   No diretório `/etc/squid`, abra o arquivo `squid.conf` para edição.
   ```bash
   sudo nano /etc/squid/squid.conf
   ```

2. **Definir as regras de bloqueio de URLs**:
   
   O `url_regex` permite bloquear URLs com base em padrões definidos por expressões regulares. Vamos adicionar uma regra de exemplo para bloquear URLs que contêm uma palavra ou expressão específica (por exemplo, bloquear qualquer URL que tenha "forbidden" nela).

   - **Exemplo de bloqueio de URLs com `url_regex`**:
     Adicione a seguinte linha no arquivo, definindo a expressão regular para bloquear URLs com a palavra "forbidden".
     ```bash
     acl blocked_urls url_regex -i ifro
     ```

   A opção `-i` torna a expressão regular case-insensitive (ignora maiúsculas e minúsculas), ou seja, ela bloqueará "forbidden", "Forbidden", "FORBIDDEN", etc.

3. **Aplicar a regra de bloqueio nas configurações de acesso**:
   
   Agora que a ACL (Access Control List) foi definida, precisamos aplicá-la à política de acesso do Squid. Para bloquear essas URLs, adicione a seguinte linha logo após a configuração da rede interna (`http_access allow aula`):
   ```bash
   http_access deny blocked_urls
   ```

4. **Revisar o fluxo das regras de acesso**:
   
   O arquivo `squid.conf` deve ter uma ordem de regras bem definida. Certifique-se de que as regras de bloqueio são executadas antes da regra geral de negação (que nega todo o tráfego que não corresponde a uma exceção).

   Exemplo de fluxo de regras:
   ```bash
   http_access allow aula
   http_access deny blocked_urls
   http_access deny all
   ```

   O Squid tentará acessar as URLs bloqueadas pela regra `blocked_urls` antes de negar o tráfego por padrão (linha `http_access deny all`).

## 7.5.3 Salvar e fechar o arquivo

Após adicionar as regras de bloqueio no arquivo `squid.conf`, salve e feche o editor. No `nano`, pressione `Ctrl + X`, depois `Y` para confirmar e `Enter` para salvar.

---

---

### 1. **Bloquear uma Faixa de IP para Não Baixar Arquivos ZIP**

Este exemplo mostra como bloquear o download de arquivos com extensão `.zip` para uma faixa de IP específica.

**Passos:**

1. Crie uma ACL para identificar arquivos ZIP:
    ```bash
    acl arquivos_zip url_regex zip
    ```
2. Defina a faixa de IP a ser bloqueada (exemplo: 192.168.0.0/24):
    ```bash
    acl proibido_acesso src 192.168.0.0/24
    ```
3. Bloqueie o acesso aos arquivos ZIP para essa faixa de IP:
    ```bash
    http_access deny proibido_acesso arquivos_zip
    ```

### Exemplo de configuração:
```bash
acl arquivos_zip url_regex zip
acl proibido_acesso src 192.168.0.0/24
http_access deny proibido_acesso arquivos_zip
```

---

### 2. **Bloquear um Site para Todos os Usuários da Rede**

Este exemplo mostra como bloquear um site (por exemplo, o Facebook) para todos os usuários da rede.

**Passos:**

1. Crie uma ACL para identificar o site a ser bloqueado:
    ```bash
    acl site_proibido dstdomain .facebook.com
    ```
2. Bloqueie o acesso a esse site para todos os usuários:
    ```bash
    http_access deny all site_proibido
    ```

### Exemplo de configuração:
```bash
acl site_proibido dstdomain .facebook.com
http_access deny all site_proibido
```

---

### 3. **Controlar o Acesso por Hora**

Este exemplo configura o Squid para bloquear o acesso a um determinado horário para usuários de uma faixa de IP específica (exemplo: `192.168.0.0/24`).

**Passos:**

1. Defina uma ACL para o horário em que o acesso será bloqueado (exemplo: segunda a sexta-feira, das 08:05 às 11:40):
    ```bash
    acl fechado_para_aula time MTWHF 08:05-11:40
    ```
2. Defina uma ACL para a faixa de IP dos usuários (exemplo: `192.168.0.0/24`):
    ```bash
    acl hora_de_aula src 192.168.0.0/24
    ```
3. Bloqueie o acesso durante esse horário para os usuários dessa faixa de IP:
    ```bash
    http_access deny hora_de_aula fechado_para_aula
    ```

### Exemplo de configuração:
```bash
acl fechado_para_aula time MTWHF 08:05-11:40
acl hora_de_aula src 192.168.0.0/24
http_access deny hora_de_aula fechado_para_aula
```

---

### 4. **Liberar o Acesso Somente em um Determinado Horário**

Este exemplo configura o Squid para permitir o acesso a uma faixa de IP específica (exemplo: `192.168.0.0/24`) somente durante um horário determinado.

**Passos:**

1. Defina uma ACL para a faixa de IP dos usuários (exemplo: `192.168.0.0/24`):
    ```bash
    acl usuarios src 192.168.0.0/24
    ```
2. Defina uma ACL para o horário em que o acesso será liberado (exemplo: segunda a sexta-feira, das 11:40 às 13:05):
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

### Exemplo de configuração:
```bash
acl usuarios src 192.168.0.0/24
acl libera_geral time MTWHF 11:40-13:05
http_access allow usuarios libera_geral
http_access deny usuarios
```

---

### 5. **Usar um Arquivo de Texto para Incluir Diversos Parâmetros de Bloqueio**

Se a lista de sites ou usuários a serem bloqueados for muito longa, você pode usar um arquivo externo, como `arquivo_sites.txt`, que contém os sites a serem bloqueados. O exemplo abaixo mostra como configurar isso.

**Passos:**

1. Defina uma ACL para a faixa de IP dos usuários (exemplo: `192.168.0.0/24`):
    ```bash
    acl usuarios src 192.168.0.0/24
    ```
2. Crie uma ACL para carregar a lista de sites proibidos a partir de um arquivo:
    ```bash
    acl sites_proibidos url_regex "/caminho/para/arquivo_sites.txt"
    ```
3. Bloqueie o acesso a esses sites para os usuários dessa faixa de IP:
    ```bash
    http_access deny usuarios sites_proibidos
    ```

### Exemplo de configuração:
```bash
acl usuarios src 192.168.0.0/24
acl sites_proibidos url_regex "/etc/squid/arquivo_sites.txt"
http_access deny usuarios sites_proibidos
```

---

### Considerações Finais:

- **Lembre-se de sempre testar a configuração do Squid após as alterações**:
    ```bash
    sudo squid -k reconfigure
    ```

- **Backup**: Antes de fazer alterações no arquivo de configuração, é sempre recomendável fazer um backup:
    ```bash
    sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.backup
    ```

- **Log**: Se você tiver problemas ou quiser verificar se as regras estão sendo aplicadas corretamente, os logs do Squid geralmente ficam em `/var/log/squid/access.log`.

---

Esse tutorial cobre as configurações para bloquear o acesso a determinados sites, controlar o acesso por horários e utilizar arquivos externos para facilitar a manutenção das configurações do Squid.
